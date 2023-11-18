import cv2
from flask import Flask, render_template, Response
from threading import Thread

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.grabbed, self.frame = self.video.read()
        Thread(target=self.update, args=()).start()

    def update(self):
        while True:
            self.grabbed, self.frame = self.video.read()

    def read(self):
        return self.frame

app = Flask(__name__)
camera = VideoCamera()

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.read()
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')  # certificate and key files
    app.run(host='0.0.0.0', debug=True, ssl_context=context)