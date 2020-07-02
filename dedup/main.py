import cv2
import numpy as np
import glob
import xxhash


# This method is used to obtain the video's framerate
# print(vidcap.get(cv2.CAP_PROP_FPS))


def iterate_video(video_file):
	vidcap = cv2.VideoCapture(video_file)
	success, image = vidcap.read()
	while success:
		success, image = vidcap.read()


def jump_to_frame(video_file):
	vidcap = cv2.VideoCapture(video_file)
	# print(cv2.CAP_PROP_POS_FRAMES)
	frame_num = 15
	vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_num-1)
	success, image = vidcap.read()
	cv2.imwrite('captured_frame.jpg', image)


def compare_two_frames(frame1, frame2):
	# initially just make sure that the sizes and layers are the same
	if frame1.shape == frame2.shape:
		# subtracts each corresponding pixel value, including each channel
		diff = cv2.subtract(frame1, frame2)
		# split the differences into three channels, (blue, green, red)
		b, g, r = cv2.split(diff)

		# if there are any non-zero values after subtraction then they aren't equal
		if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
			return True
	return False


def hash_frame(frame):
	h = xxhash.xxh64()
	h.update(frame)
	return h.digest()


def capture_video_and_write_to_images(video_file):
	vidcap = cv2.VideoCapture(video_file)
	success, image = vidcap.read()
	# only captures the first 50 frames, for editing purposes
	i = 0
	while success:
		cv2.imwrite(f'frame{i}.jpg', image)
		success, image = vidcap.read()
		i+=1
		if i == 75:
			break


def write_to_video_from_images(path_to_images_folder):
	img_array = []
	i = 0
	# for filename in glob.glob('*.jpg'):
	# using glob jumbles the video frames
	while i < 75:
		filename = f'frame{i}.jpg'
		print(filename)
		img = cv2.imread(filename)
		height, width, layers = img.shape
		size = (width,height)
		img_array.append(img)
		i += 1

	out = cv2.VideoWriter('test2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, size)

	for i in range(len(img_array)):
		out.write(img_array[i])
	out.release()


def create_local_hash_file(video_file):
	h = xxhash.xxh64()
	vidcap = cv2.VideoCapture(video_file)

	with open('local_hashed2.txt', 'w+') as local_hash_file:
		success, frame = vidcap.read()
		while success:
			h.update(frame)
			local_hash_file.write(f'{h.digest()}\n')
			success, frame = vidcap.read()



if __name__ == '__main__':
	create_local_hash_file('test2.mp4')
