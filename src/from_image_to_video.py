import cv2
import os

image_folder = 'C:\\apps\\opencv\\sources\\samples\\data\\images'
video_name = 'C:\\apps\\opencv\\sources\\samples\\data\\testvideo.mp4'

frame = cv2.imread(os.path.join(image_folder, 'frame0.jpg'))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, -1, 24, (width,height))

for i in range(0, 130):
    video.write(cv2.imread(os.path.join(image_folder, 'frame'+str(i)+'.jpg')))
    
cv2.destroyAllWindows()
video.release()
