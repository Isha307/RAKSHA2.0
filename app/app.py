import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, render_template, Response, jsonify, request
from backend.camera import VideoCamera
from backend.score import get_score

app = Flask(__name__)

video_camera = None
global_frame = None

category = 'Hammer Strike'


@app.route('/record_status', methods=['POST'])
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/modules')
def elements():
    return render_template('modules.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pose', methods=['GET', 'POST'])
def pose():
    global category
    """Video streaming"""
    category = request.form.get('detect')
    return render_template('pose.html')

@app.route('/update', methods=['GET', 'POST'])
def update_score():
    return render_template('score.html', score=get_score(category))

if __name__ == '__main__':
    app.run(debug=True, threaded=True)