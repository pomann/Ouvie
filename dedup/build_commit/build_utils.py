import os
import json
import cv2
import numpy as np
import xxhash
from collections import defaultdict, namedtuple


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
			frame_name = f'frame{frame_counter}.png'
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

	with open('commit/inserts/grouped_inserts.json', 'w+') as grouped_inserts_file:
		grouped_inserts_json = json.dumps(grouped_inserts)
		grouped_inserts_file.write(grouped_inserts_json)

	with open('commit/inserts/frame_hashes.json', 'w+') as frame_hashes_file:
		frame_hashes_json = json.dumps(frame_hashes)
		frame_hashes_file.write(frame_hashes_json)

	return grouped_inserts, frame_hashes



def hash_version(version_path, hash_output_path):
	vidcap = cv2.VideoCapture(version_path)

	with open(hash_output_path, 'w+') as local_hash_file:
		success, frame = vidcap.read()
		while success:
			local_hash_file.write(f'{xxhash.xxh64(frame).digest()}\n')
			success, frame = vidcap.read()

	vidcap.release()

# This myers_diff algorithm has been adapted from adamnew123456 at GitHub Gist (10/02/2020)
# Please see here for the original implementation:
#	https://gist.github.com/adamnew123456/37923cf53f51d6b9af32a539cdfa7cc4
def myers_diff(a_lines, b_lines):
	"""
	An implementation of the Myers diff algorithm.
	See http://www.xmailserver.org/diff2.pdf
	"""
	Keep = namedtuple('Keep', ['line'])
	Insert = namedtuple('Insert', ['line'])
	Remove = namedtuple('Remove', ['line'])
	Frontier = namedtuple('Frontier', ['x', 'history'])
	frontier = {1: Frontier(0, [])}

	def one(idx):
		return idx - 1

	a_max = len(a_lines)
	b_max = len(b_lines)
	for d in range(0, a_max + b_max + 1):
		for k in range(-d, d + 1, 2):
			go_down = (k == -d or (k != d and frontier[k - 1].x < frontier[k + 1].x))
			if go_down:
				old_x, history = frontier[k + 1]
				x = old_x
			else:
				old_x, history = frontier[k - 1]
				x = old_x + 1
			history = history[:]
			y = x - k
			if 1 <= y <= b_max and go_down:
				history.append(Insert(b_lines[one(y)]))
			elif 1 <= x <= a_max:
				history.append(Remove(a_lines[one(x)]))
			while x < a_max and y < b_max and a_lines[one(x + 1)] == b_lines[one(y + 1)]:
				x += 1
				y += 1
				history.append(Keep(a_lines[one(x)]))
			if x >= a_max and y >= b_max:
				return history, Keep, Insert
			else:
				frontier[k] = Frontier(x, history)

	assert False, 'Could not find edit script'


def run_myers_diff(remote_hashfile, local_hashfile, output_file):
	with open(remote_hashfile) as remote_contents:
		remote_lines = [line.rstrip() for line in remote_contents]

	with open(local_hashfile) as local_contents:
		local_lines = [line.rstrip() for line in local_contents]

	with open(output_file, 'w+') as output_file:
		diff, Keep, Insert = myers_diff(remote_lines, local_lines)
		for elem in diff:
			if isinstance(elem, Keep):
				output_file.write(' ' + elem.line + '\n')
			elif isinstance(elem, Insert):
				output_file.write('+' + elem.line + '\n')
			else:
				output_file.write('-' + elem.line + '\n')
