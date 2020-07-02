import unittest
import cv2
import xxhash


class TestBuild(unittest.TestCase):

	def test_num_of_hashes_equal_to_frames(self):
		number_of_frames = 0
		vidcap = cv2.VideoCapture('test.mp4')
		success, image = vidcap.read()
		while success:
			success, image = vidcap.read()
			number_of_frames+=1
		vidcap.release()
		with open('hashes.txt') as hash_file:
			number_of_hashes = len(hash_file.readlines())
		self.assertEqual(number_of_frames, number_of_hashes)

	def test_num_of_added_frames_equal_to_num_of_adds_in_diff(self):
		num_of_frames = len([frame for frame in os.listdir('commit/inserts/frames') if os.path.isfile(frame)])
		num_of_additions = 0
		with open('commit/diff.txt', 'r') as diff_file:
			for line in diff_file.readlines():
				if line[0] == '+':
					num_of_additions += 1
		self.assertEqual(num_of_frames, num_of_additions)

	




if __name__ == '__main__':
	unittest.main()
