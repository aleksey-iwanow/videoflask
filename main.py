import subprocess
import urllib.request

from flask import Flask, request, render_template, Response, jsonify
from camera import VideoCamera

app = Flask(__name__)

video_stream = VideoCamera()


def get_info():
    IP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    try:
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell=True)
        cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
        temp = subprocess.check_output(cmd, shell=True)
        info = [f'IP: {IP}', CPU, MemUsage, Disk, f'Temperature: {temp}']
    except Exception as error:
        info = [f'IP: {IP}', "CPU", "MemUsage", "Disk", "temp"]
    return info


@app.route("/")
def index():
    return render_template("index.html", info=get_info())


@app.route('/reboot-yes')
def reboot_yes():
    print("Hello")
    return "nothing"


@app.route('/reboot-no')
def reboot_no():
    print("Hello2")
    return "nothing"


@app.route('/display-yes')
def display_yes():
    p = subprocess.run("python /usr/bin/display.py", shell=True)
    return "nothing"


@app.route('/display-no')
def display_no():
    print("Hello2")
    return "nothing"


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