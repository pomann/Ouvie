import os
import shutil

import xxhash
import cv2
import numpy as np

from . import s3_funcs as s3f
from . import rebuild_version as rebuild


def build_after_commit(user, zipped_commit_file_path, versions_path, pid, cid, cfiles, num_commits):
	# build latest version
	shutil.unpack_archive(zipped_commit_file_path, f'{versions_path}/{pid}/commit', 'zip')
	current_version = f'{versions_path}/{pid}/current_version.mp4'
	commit_directory = f'{versions_path}/{pid}/commit'
	output_file = f'{versions_path}/{pid}/newer_version.mp4'
	current_hashfile = f'{versions_path}/{pid}/hashes.txt'
	next_hashfile = f'{versions_path}/{pid}/commit/local_hashfile.txt'
	rebuild.rebuild_version(current_version, commit_directory, output_file)
	os.rename(next_hashfile, current_hashfile)

	# clean up build
	os.remove(current_version)
	os.rename(output_file, current_version)
	shutil.rmtree(f'{versions_path}/{pid}/commit')

	# check if current version should be a snapshot
	if ((num_commits+1)%5) == 0:
		print('Adding snapshot...')
		sid = f'sid{xxhash.xxh64(pid, seed=(num_commits+1)).intdigest()}'
		# send the snapshot to s3
		s3f.add_snapshot(user, pid, sid, current_version)
		# record the snapshot in the version control database
		PARAMS = {'user':user, 'chash':sid, 'phash':cid, 'pid':pid, 'snap':True, 'cfiles':cfiles}
		result = requests.get(url=database_endpoints['ADD_COMMIT'], params=PARAMS)
	return "Success"


def hash_version(version_path, hash_output_path):
	print('Hashing version...')
	vidcap = cv2.VideoCapture(version_path)

	with open(hash_output_path, 'w+') as local_hash_file:
		success, frame = vidcap.read()
		while success:
			local_hash_file.write(f'{xxhash.xxh64(frame).digest()}\n')
			success, frame = vidcap.read()
	vidcap.release()
