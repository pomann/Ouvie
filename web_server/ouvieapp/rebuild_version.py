import os
import json
import cv2
import numpy as np
import xxhash
from collections import defaultdict

def rebuild_version(current_version, commit_directory, output):
	# load in diff file contents, grouped inserts contents and frame hashes contents
	diff_file_path = f'{commit_directory}/diff.txt'
	grouped_inserts_path = f'{commit_directory}/inserts/grouped_inserts.json'
	frame_hashes_path = f'{commit_directory}/inserts/frame_hashes.json'
	frames_path = f'{commit_directory}/inserts/frames'

	with open(diff_file_path, 'r') as diff_file_contents:
		diff_lines = diff_file_contents.readlines()

	with open(grouped_inserts_path, 'r') as grouped_inserts_json:
		grouped_inserts = json.load(grouped_inserts_json)

	with open(frame_hashes_path, 'r') as frame_hashes_json:
		frame_hashes = json.load(frame_hashes_json)

	# create capture object for current versioni and writer object for next version
	current_version = cv2.VideoCapture(current_version)
	success, frame = current_version.read()
	width  = current_version.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = current_version.get(cv2.CAP_PROP_FRAME_HEIGHT)
	size = (int(width), int(height))
	next_version = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'mp4v'), 25, size)

	diff_pointer = 0
	insert_counter = 0

	while diff_pointer < len(diff_lines):
		print(diff_lines[diff_pointer])
		if diff_lines[diff_pointer][0] == '-':
			# print('delete')
			success, frame = current_version.read()
			diff_pointer += 1

		elif diff_lines[diff_pointer][0] == '+':
			# print('insert')
			inserts = grouped_inserts[str(insert_counter)]
			for insert in inserts:
				print(insert)
				frame_name = frame_hashes[insert]
				frame_path = f'{frames_path}/{frame_name}'
				frame = cv2.imread(frame_path)
				next_version.write(frame)
				diff_pointer += 1
			if success:
				next_version.write(frame)
				success, frame = current_version.read()
				diff_pointer += 1
			insert_counter += 1

		else:
			# print('keep')
			next_version.write(frame)
			success, frame = current_version.read()
			diff_pointer += 1


if __name__ == '__main__':
	rebuild_version('test2.mp4', 'commit2')

# width  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
# height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
# size = (int(width), int(height))
# out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, size)
