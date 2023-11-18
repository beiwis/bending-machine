import cv2
from flask import Flask, render_template, Response
from threading import Thread

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            raise Exception("Could not open video device")
        self.grabbed, self.frame = self.video.read()
        if not self.grabbed:
            raise Exception("Could not read frame from video")
        Thread(target=self.update, args=()).start()

    def update(self):
        while True:
            self.grabbed, self.frame = self.video.read()
            if not self.grabbed:
                print("Could not read frame from video")
                continue

    def read(self):
        return self.frame

app = Flask(__name__)
camera = VideoCamera()

@app.route('/')
def index():
    return render_template('index.html')