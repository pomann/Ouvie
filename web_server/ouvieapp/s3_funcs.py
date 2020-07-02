import boto3
import time

OUVIE_BUCKET = 'ouvie-bucket'

def list_files(bucket):
	s3 = boto3.resource('s3')
	bucket_instance = s3.Bucket(bucket)
	contents = []

	for file in bucket_instance.objects.all():
		contents.append(file.key)

	return contents


def upload_file(file_name):
	object_name = file_name
	s3_client = boto3.client('s3')
	response = s3_client.upload_file(file_name, bucket, object_name)

	return response


def add_project(file_path, object_name, project_directory):
	s3_client = boto3.client('s3')
	try:
		s3_client.upload_file(file_path, OUVIE_BUCKET, f'{project_directory}/{object_name}')
		print('Success')
		return 'Success'
	except:
		return 'Failure'


def retrieve_project(filename):
	s3 = boto3.resource('s3')
	output = f'working_cache/test2.txt'
	s3.Bucket(OUVIE_BUCKET).download_file(f'working_cache/{filename}', output)


def get_num_commits(user, pid):
	s3 = boto3.client('s3')
	num_snapshots = len(s3.list_objects(Bucket=OUVIE_BUCKET, Prefix=f'{user}/{pid}/snapshots/')['Contents'])
	try:
		num_commits = len(s3.list_objects(Bucket=OUVIE_BUCKET, Prefix=f'{user}/{pid}/commits/')['Contents'])
	except:
		num_commits = 0
	return (num_snapshots+num_commits)


def add_commit(user, pid, cid, file_path):
	s3_client = boto3.client('s3')
	try:
		s3_client.upload_file(file_path, OUVIE_BUCKET, f'{user}/{pid}/commits/{cid}.zip')
		print('Added commit')
		return 'Success'
	except:
		return 'Failure'


def add_snapshot(user, pid, sid, file_path):
	s3_client = boto3.client('s3')
	try:
		s3_client.upload_file(file_path, OUVIE_BUCKET, f'{user}/{pid}/snapshots/{sid}.mp4')
		print('Added snapshot')
		return 'Success'
	except:
		return 'Failure'


def download_snapshot(user, pid, sid, rebuild_directory):
	s3 = boto3.resource('s3')
	object_name = f'{user}/{pid}/snapshots/{sid}.mp4'
	output_file = f'{rebuild_directory}/version0.mp4'
	s3.Bucket(OUVIE_BUCKET).download_file(object_name, output_file)


def download_commit(user, pid, cid, rebuild_directory):
	s3 = boto3.resource('s3')
	object_name = f'{user}/{pid}/commits/{cid}.zip'
	output_file = f'{rebuild_directory}/commit.zip'
	s3.Bucket(OUVIE_BUCKET).download_file(object_name, output_file)


def download_file(file_name, bucket):
	s3 = boto3.resource('s3')
	output = f'working_cache/{file_name}'
	s3.Bucket(bucket).download_file(file_name, output)

	return output
