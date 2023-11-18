from flask import Flask, render_template, Response, make_response
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.after_request
def after_request(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')  # certificate and key files
    app.run(host='0.0.0.0', debug=True, ssl_context=context)
