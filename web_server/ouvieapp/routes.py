import os
import shutil
import threading
import time
import requests
import json

import xxhash
from flask import render_template, request, redirect, send_file, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename

from ouvieapp import app
from . import s3_funcs as s3f
from . import rebuild_version as rebuild
from . import multithread_utils as mtu

database_endpoints = {
	'ADD_PROJECT': 'http://127.0.0.1:5000/api/v1/add/project',
	'ADD_COMMIT': 'http://127.0.0.1:5000/api/v1/add/commit',
	'RETRIEVE_COMMIT_FILES': 'http://127.0.0.1:5000/api/v1/retrieve/commits',
	'RETRIEVE_PID_FROM_PNAME': 'http://127.0.0.1:5000/api/v1/retrieve/pid'
}

@app.route('/')
def entry_point():
	return 'Hello, world!'

@app.route('/storage')
def storage():
	contents = s3f.list_files('aliu2-first-bucket')
	return render_template('storage.html', contents=contents)



"""
Facilitates cloning of the project
by retrieving the latest version of the project stored on the server

Args:
    user (str): Username
    pname (str): Project name

Returns:
    FileStorage: File as an attatchment
"""
@app.route('/api/v1/clone/project', methods=['GET', 'POST'])
def clone_project():
	try:
		user = request.args['user']
		pname = request.args['pname']
		auth = request.headers['Authorization']
	except:
		return jsonify({'status':"failure", 'code':'OV0000', 'data':['null']})
	PARAMS = {'user':user, 'pname':pname}
	HEADERS = {'Authorization' : auth}
	response = requests.get(url=database_endpoints['RETRIEVE_PID_FROM_PNAME'], params=PARAMS, headers=HEADERS)
	pid = json.loads(response.text)['data']
	version_directory = os.path.join(os.getcwd(), app.config['VERSIONS_FOLDER'], pid[0])
	return send_from_directory(directory=version_directory, filename='current_version.mp4', as_attachment=True)




"""
Facilitates registration of a project
Sends the project information to the database
and to AWS S3

Args:
    user (str): Username
    name (str): Project name
	cfiles (str): File name
	storage (bytes): File as bytes

Returns:
    json: Json response with corresponding status codes
"""
@app.route('/api/v1/add/project', methods=['POST'])
def add_project():
	try:
		user = request.args['user']
		name = request.args['name']
		cfiles = request.args['cfiles']
		storage = request.data
	except:
		return jsonify({'status':"failure", 'code':'OV0000', 'data':['null']})

	# generate id's
	with open('seed', 'r') as seed_file:
		persistent_seed = int(seed_file.readline())
	with open('seed', 'w') as seed_file:
		seed_file.write(str(persistent_seed+1))
	pid = f'pid{xxhash.xxh64(user, seed=persistent_seed).intdigest()}'
	sid = f'sid{xxhash.xxh64(pid, seed=0).intdigest()}'

	# initialize file paths, create server storage directory and save the file
	file_ext = cfiles.split('.')[-1]
	current_version_path = os.path.join(app.config['VERSIONS_FOLDER'], pid)
	file_path = os.path.join(current_version_path, f'current_version.{file_ext}')
	os.mkdir(current_version_path)
	with open(file_path, 'wb') as f:
		f.write(storage)

	# initialize s3 parameters
	object_name = f'{sid}.{file_ext}'
	project_directory = f'{user}/{pid}/snapshots'

	# thread to upload initial commit to s3
	send_to_s3_thread = threading.Thread(
		target=s3f.add_project,
		args=(file_path, object_name, project_directory,),
		daemon=True)

	# thread to create hash file for initial commit
	hash_version_thread = threading.Thread(
		target=mtu.hash_version(file_path, f'{current_version_path}/hashes.txt')
	)

	send_to_s3_thread.start()
	hash_version_thread.start()

	PARAMS = {'user':user, 'name':name, 'pid':pid}
	response = requests.get(url=database_endpoints['ADD_PROJECT'], params=PARAMS)
	if json.loads(response.text)['status'] == 'success':
		PARAMS = {'user':user, 'chash':sid, 'phash':-1, 'pid':pid, 'snap':True, 'cfiles':cfiles}
		response = requests.get(url=database_endpoints['ADD_COMMIT'], params=PARAMS)
	return jsonify({'status': 'success', 'code' : 'OV1111', 'data': [pid, sid]})

	return jsonify({'status': 'failure', 'code' : 'OV0000', 'data' : ['nuill']})




"""
Facilitates adding of commit to a project
Sends commit information to version control history
and to AWS S3

Args:
    user (str): Username
	phash (str): Hash of previous commit
	pid (str): Project ID
	cfiles (str): File name
	storage (bytes): File as bytes

Returns:
    json: Json response with corresponding status codes
"""
@app.route('/api/v1/add/commit', methods=['POST'])
def add_commit():
	try:
		user = request.args['user']
		phash = request.args['phash']
		pid = request.args['pid']
		cfiles = request.args['cfiles']
		storage = request.data
	except:
		return jsonify({'status':'failure', 'code':'OV0000', 'data':['null']})

	num_commits = s3f.get_num_commits(user, pid)
	cid = f'cid{xxhash.xxh64(pid, seed=(num_commits+1)).intdigest()}'

	# commit should always be a zip file and thus you can save it as commit.zip
	file_name = secure_filename('commit.zip')
	file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
	with open(file_path, 'wb') as f:
		f.write(storage)

	# thread to upload zip to s3
	send_to_s3_thread = threading.Thread(
		target=s3f.add_commit,
		args=(user, pid, cid, file_path,),
		daemon=True)

	# thread to build the most recent version
	build_version_thread = threading.Thread(
		target=mtu.build_after_commit,
		args=(user, file_path, app.config['VERSIONS_FOLDER'], pid, cid, cfiles, num_commits),
		daemon=True)

	send_to_s3_thread.start()
	build_version_thread.start()

	PARAMS = {'user':user, 'chash':cid, 'phash':phash, 'pid':pid, 'snap':False, 'cfiles':cfiles}
	response = requests.get(url=database_endpoints['ADD_COMMIT'], params=PARAMS)
	if json.loads(response.text)['status'] == 'success':
		return jsonify({'status': 'success', 'code' : 'OV1111', 'data': [pid, cid]})

	return jsonify({'status': 'failure', 'code' : 'OV0000'})




"""
Reverts to a previous version
by rebuilding from a snapshot
and the latter series of commits

Args:
    user (str): Username
	pid (str): Project ID
	chash (str): Commit ID

Returns:
    json: Json response with corresponding status codes
"""
@app.route('/api/v1/rebuild/version', methods=['GET', 'POST'])
def rebuild_version():
	try:
		user = request.args['user']
		pid = request.args['pid']
		chash = request.args['chash']
	except:
		return jsonify({'status':'failure', 'code':'OV0000', 'data':['null']})

	# retrieve version controlled list of commits
	PARAMS = {
		'user':user,
		'pid':pid,
		'chash':chash}
	response = requests.get(url=database_endpoints['RETRIEVE_COMMIT_FILES'], params=PARAMS)
	commits_in_order = json.loads(response.text)['data']

	# prepare the rebuild
	sid = commits_in_order[0]
	rebuild_folder = app.config['REBUILD_FOLDER']
	s3f.download_snapshot(user, pid, sid, rebuild_folder)

	most_recent = 0
	print('yay')
	if (len(commits_in_order) != 1):
		# rebuild
		for i, cid in enumerate(commits_in_order[1:]):
			print(f'Working on commit: {cid}')
			s3f.download_commit(user, pid, cid, app.config['REBUILD_FOLDER'])
			zip_directory = f'{rebuild_folder}/commit.zip'
			shutil.unpack_archive(zip_directory, f'{rebuild_folder}', 'zip')
			current_version =f'{rebuild_folder}/version{i}.mp4'
			commit_directory = f'{rebuild_folder}/commit'
			output = f'{rebuild_folder}/version{i+1}.mp4'
			rebuild.rebuild_version(current_version, commit_directory, output)
			shutil.rmtree(commit_directory)
			os.remove(zip_directory)
			most_recent = i + 1
	print(most_recent)
	rebuild_dir = os.path.join(os.getcwd(), app.config['REBUILD_FOLDER'])
	return send_from_directory(directory=rebuild_dir, filename=f'version{most_recent}.mp4', as_attachment=True)




"""
Sends the precomputed hashfile for the
most recent version of a project

Args:
	pid (str): Project ID

Returns:
    FileStorage: File as an attatchment
"""
@app.route('/api/v1/retrieve/hashfile', methods=['GET'])
def retrieve_hashfile():
	try:
		pid = request.args['pid']
	except:
		return jsonify({'status':'failure', 'code':'OV0000', 'data':['null']})
	upload_folder = os.path.join(os.getcwd(), app.config['VERSIONS_FOLDER'], pid)
	return send_from_directory(directory=upload_folder, filename='hashes.txt', as_attachment=True)



@app.route('/api/v1/retrieve/project', methods=['GET'])
def retrieve_project():
	if request.method == 'GET':
		user = request.args['user']
		name = request.args['name']
		pid = request.args['pid']
		s3f.retrieve_project('test2.txt')
		return 'Done'



@app.route('/test', methods=['GET', 'POST'])
def test_route():
	if request.method == 'GET':
		# PARAMS = {'user':'omo', 'pid':'pid15052553844805725992', 'chash':'cid6630835625259533444'}
		# response = requests.get(url=database_endpoints['RETRIEVE_COMMIT_FILES'], params=PARAMS)
		# print(json.loads(response.text))
		# commits_in_order = json.loads(response.text)['data']
		# print(commits_in_order)
		print('first')
		threaded = threading.Thread(target=s3f.test, args=('john',), daemon=True)
		threaded.start()
	return 'Done'



# @app.route('/test', methods=['GET', 'POST'])
# def test_route():
# 	if request.method == 'POST':
# 		multi_store = request.files.getlist('file[]')
# 		for storage in multi_store:
# 			file_name = secure_filename(storage.filename)
# 			print(file_name)
# 			file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
# 			storage.save(file_path)
#
# 	return 200


# storage = request.files.getlist('file[]')
# print(storage[0])
# print(storage[1])
# print(storage.read())
# filename = secure_filename(storage.filename)
# file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# storage.save(file_path)
# s3f.add_project(filename, file_path)
# # s3f.add_project('test_folder')
# DATABASE_ADD_PROJECT_API = 'http://127.0.0.1:5000/api/v1/add/project'
# PARAMS = {'user':user, 'name':name, 'pid':5}
# result = requests.get(url=DATABASE_ADD_PROJECT_API, params=PARAMS)
#pid15052553844805725992
#sid16478646992684922427
