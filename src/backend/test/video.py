# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response
import cv2
import base64
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()

        if not success:
            break

        buffer = cv2.imencode('.jpg', frame)[1]
        pic_str = base64.b64encode(buffer).decode()

        img_data = base64.b64decode(pic_str)
        nparr = np.fromstring(img_data, np.uint8)
        imp_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        ret, buffer = cv2.imencode('.jpg', imp_np)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0')