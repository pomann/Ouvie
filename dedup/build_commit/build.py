import os
import shutil
import requests
import build_utils as bcu
import sys


def main(local_version, user, phash, pid, cfiles):

	web_server_endpoints = {
		'GET_HASHFILE': 'http://127.0.0.1:5001/api/v1/retrieve/hashfile',
		'POST_COMMIT': 'http://127.0.0.1:5001/api/v1/add/commit'
	}

	try:
		os.makedirs('commit/inserts/frames')
	except FileExistsError as exc:
		print(f"{exc}\nCommit file already exists")
		shutil.rmtree('commit')
		os.makedirs('commit/inserts/frames')

	if os.path.exists('commit.zip'):
		os.remove('commit.zip')

	if os.path.exists('local_hashfile.txt'):
		os.remove('local_hashfile.txt')

	if os.path.exists('remote_hashfile.txt'):
		os.remove('remote_hashfile.txt')

	#
	# # retrieve remote hashfile
	PARAMS = {'pid':pid}
	response = requests.get(url=web_server_endpoints['GET_HASHFILE'], params=PARAMS)
	with open('remote_hashfile.txt', 'wb+') as f:
		f.write(response.content)
	#
	# # build local hashfile
	bcu.hash_version(local_version, 'commit/local_hashfile.txt')
	#
	# # generate diff file
	bcu.run_myers_diff('remote_hashfile.txt', 'commit/local_hashfile.txt', 'commit/diff.txt')
	#
	# # build commit directory
	bcu.build_commit(local_version, 'commit/diff.txt')
	#
	# # zip commit directory
	zipped_commit = shutil.make_archive('commit', 'zip', 'commit')

	# ready post data
	upload_file = open(zipped_commit, 'rb')
	PARAMS = {
		'user':user,
		'phash':phash,
		'pid':pid,
		'cfiles':cfiles
		}
	#
	# # send commit to web server
	response = requests.post(url=web_server_endpoints['POST_COMMIT'], params=PARAMS, data=upload_file)

	# cleanup
	shutil.rmtree('commit')
	if os.path.exists('commit.zip'):
		os.remove('commit.zip')
	if os.path.exists('local_hashfile.txt'):
		os.remove('local_hashfile.txt')
	if os.path.exists('remote_hashfile.txt'):
		os.remove('remote_hashfile.txt')




if __name__ == '__main__':
	user = sys.argv[1]
	fileName = sys.argv[2]
	pid, cid = "", ""

	with open('.ouvie/oConf.txt', 'r') as f:
		i = 0
		for line in f.readlines():
			line = line.strip('\n')

			# Pid on the first line
			if (i == 0):
				pid = line.split(':')[1]
			else:
				cid = line.split(':')[1]
			
			i += 1
	
	main(fileName, user,  cid, pid, fileName)
