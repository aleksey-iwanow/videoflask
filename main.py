import subprocess
import urllib.request
from test import *
from flask import Flask, render_template, Response
from camera import VideoCamera
from datetime import datetime

app = Flask(__name__)

video_stream = VideoCamera()


def get_info():
    try:
        IP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    except Exception as error:
        IP = socket.gethostname()
    try:
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell=True)
        cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
        temp = subprocess.check_output(cmd, shell=True)
        info = [f"IP: {str(IP)}",
                str(CPU, 'utf-8'),
                str(MemUsage, 'utf-8'),
                str(Disk, 'utf-8'),
                f"Temp: {str(temp, 'utf-8')}"]
    except Exception as error:
        info = [f'IP: {IP}',
                "CPU",
                "MemUsage",
                "Disk",
                f"time: {datetime.now()}"]
    return info


@app.route('/update_data', methods=['GET'])
def update_data():
    data = "<br/>".join([a for a in get_info()])
    return data


@app.route("/")
def index():
    return render_template("index.html", info=get_info())


@app.route("/code")
def code():
    return render_template("code.html")


@app.route('/reboot')
def reboot():
    print("reboot now")
    return ""


@app.route('/click-left')
def click_left():
    application.clicked(1)
    return ""


@app.route('/click-up')
def click_up():
    application.clicked(2)
    return ""


@app.route('/click-run')
def click_run():
    application.clicked(3)
    return ""


@app.route('/click-down')
def click_down():
    application.clicked(4)
    return ""


@app.route('/click-right')
def click_right():
    application.clicked(5)
    return ""


@app.route('/display1-yes')
def display1_yes():
    if application.active_display1:
        application.off_display1()
        print(application.active_display1)
    return ""


@app.route('/display1-no')
def display1_no():
    if not application.active_display1:
        application.on_display1()
        print(application.active_display1)
    return ""


@app.route('/display2-yes')
def display2_yes():
    if application.active_display2:
        application.off_display2()
        print(application.active_display2)
    return ""


@app.route('/display2-no')
def display2_no():
    if not application.active_display2:
        application.on_display2()
        print(application.active_display2)
    return ""


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_stream), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)