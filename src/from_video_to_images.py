
import cv2
def FrameCapture(path):

    video = cv2.VideoCapture("C:\\apps\\opencv\\sources\\samples\\data\\testrun.MOV")
    count = 0
    success = 1

    while success:
        success, image = video.read()
        cv2.imwrite("C:\\apps\\opencv\\sources\\samples\\data\\images\\frame%d.jpg" % count, image)
        #cv2.imwrite('/path/to/destination/image.png', image)
        count += 1
if __name__ == '__main__':
    FrameCapture("C:\\apps\\opencv\\sources\\samples\\data\\vtest.avi")



