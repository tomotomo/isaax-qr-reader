from flask import Flask, Response
from pyzbar import pyzbar
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime

import numpy as np
import cv2
import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.5)

app = Flask(__name__)

@app.route('/stream')
def stream():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
	       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def get_frame():
    camera.capture(rawCapture, format="bgr", use_video_port=True)
    frame = rawCapture.array
    process_frame(frame)
    ret, jpeg = cv2.imencode('.jpg', frame)
    rawCapture.truncate(0)

    return jpeg.tobytes()


