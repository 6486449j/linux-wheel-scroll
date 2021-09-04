import os, time, re, subprocess
from pymouse import PyMouse

interval = 0.5
applications = "google-chrome|ms-edge-bin|yesplaymusic"
wheel_speed = 2

def GetWindowClass():
    p = subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    window_id = 0
    for line in p.stdout.readlines():
        m = re.match('^.*window id # (.*)$', str(line))
        if(m != None):
            window_id = m.group(1)
            break

    p2 = subprocess.Popen(["xprop", "-id", str(window_id), "WM_CLASS"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    window_class = ""
    for line in p2.stdout.readlines():
        m = re.match('WM_CLASS\(STRING\) = "([\w-]*)".*', str(line))
        if(m != None):
            window_class = m.group(1)
            break
    
    return window_class

mouse = PyMouse()

while True:
    window_class = GetWindowClass()
    print(window_class)
    m = re.match(applications, window_class)
    p = subprocess.Popen(["cat", "/tmp/libinput_discrete_deltay_multiplier"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    s = ""
    for line in p.stdout.readline():
        s = s + line.split("\n")[0]
    print("now:" + s)

    if(m != None):
        if(float(s) != wheel_speed):
            os.popen("echo " + str(wheel_speed) + " > /tmp/libinput_discrete_deltay_multiplier")
            mouse.scroll(wheel_speed)
            print(str(wheel_speed))
    else:
        os.popen("echo " + "1" + " > /tmp/libinput_discrete_deltay_multiplier")
        #mouse.scroll(1)
        print(1)
    time.sleep(interval)
