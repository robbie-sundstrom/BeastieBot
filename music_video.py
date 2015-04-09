import cv2
import numpy as np

class createVideo:
	"""
	Creates a music video
	"""
	def __init__(self, video=0):
		self.cap = cv2.VideoCapture(video)

		fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
		self.out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

	def saveVideo(self):
		# while self.success:
		# 	self.success,image = self.cap.read()
		# 	cv2.imwrite("frame%d.jpg" % self.count, image)     # save frame as JPEG file
		# if cv2.waitKey(10) == 27:                     # exit if Escape is hit
		# 	self.success = False
		# self.count += 1
		while(self.cap.isOpened()):
			ret, frame = self.cap.read()
			if ret==True:

			# write the flipped frame
				self.out.write(cv2.flip(frame,0))

				cv2.imshow('frame',frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			else:
				break
		self.cap.release()
		self.out.release()
		cv2.destroyAllWindows()

	def destroy(self):
		"""
		Ends the video recording
		"""
		self.cap.release()
		cv2.destroyAllWindows()

# video = createVideo()
# video.saveVideo()




# cap = cv2.VideoCapture(0)

# # Define the codec and create VideoWriter object
# fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
# out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret==True:

#         # write the flipped frame
#         out.write(cv2.flip(frame,0))

#         cv2.imshow('frame',frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break

# # Release everything if job is finished
# cap.release()
# out.release()
# cv2.destroyAllWindows()
video = createVideo()
video.saveVideo()