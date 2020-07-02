import os
import json
import cv2
import numpy as np
import xxhash
from collections import defaultdict

# create directory structure
try:
	os.makedirs('commit/inserts/frames')
except FileExistsError as exc:
	print(f"{exc}\nCommit file already exists")


def build_commit(local_version, diff_file):
	grouped_inserts = defaultdict(list)
	frame_hashes = {}
	group_counter = 0
	frame_counter = 0
	diff_pointer = 0
	vidcap = cv2.VideoCapture(local_version)
	success, image = vidcap.read()
	with open(diff_file, 'r') as diff_file:
		diff_lines = diff_file.readlines()

	while diff_pointer < len(diff_lines):
		if diff_lines[diff_pointer][0] == '+':
			frame_name = f'frame{frame_counter}.jpg'
			grouped_inserts[group_counter].append(diff_lines[diff_pointer].rstrip())
			frame_hashes[diff_lines[diff_pointer].rstrip()] = frame_name
			cv2.imwrite(f'commit/inserts/frames/{frame_name}', image)
			frame_counter += 1
			success, image = vidcap.read()
			try:
				if diff_lines[diff_pointer+1][0] != '+':
					group_counter += 1
			except:
				pass
		elif diff_lines[diff_pointer][0] == ' ':
			success, image = vidcap.read()
		diff_pointer += 1

	# for group in grouped_inserts.keys():
	# 	print(group)
	# 	for entry in grouped_inserts[group]:
	# 		print(f'\t{entry}')

	# for frame in frame_hashes.keys():
	# 	print(f'{frame}: {frame_hashes[frame]}')
	vidcap.release()
	return grouped_inserts, frame_hashes



if __name__ == '__main__':
	build_commit('test2.mp4', 'diff.txt')
