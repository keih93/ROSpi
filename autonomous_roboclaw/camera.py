from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2

class CameraThread:
    def __init__(self, camera):
        self.rawCapture = PiRGBArray(camera, size= camera.resolution)
        self.stopped = False
        self.camera = camera
        self.stream = camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)
        for f in self.stream:
            self.frame = f.array
            self.rawCapture.truncate(0)
            return
    
    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self
 
    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.stream.release()
                self.rawCapture.close()
                self.camera.close()
                return

            for f in self.stream:
                # grab the frame from the stream and clear the stream in
                # preparation for the next frame
                self.frame = f.array
                self.rawCapture.truncate(0)

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True