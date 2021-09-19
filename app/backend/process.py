import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, render_template, Response, jsonify, request, Blueprint, session
from camera import VideoCamera
from score import get_score

process = Blueprint('process', __name__)

video_camera = None
global_frame = None

category = session["category"]


@process.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@process.route('/')
def index():
    return render_template('index.html')

@process.route('/modules')
def elements():
    return render_template('modules/modules.html')

@process.route('/quiz')
def quiz():
    return render_template('quiz.html')

@process.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@process.route('/pose', methods=['GET', 'POST'])
def pose():
    global category
    """Video streaming"""
    category = request.form.get('detect')
    return render_template('pose.html')

@process.route('/update', methods=['GET', 'POST'])
def update_score():
    return render_template('score.html', score=get_score(category))