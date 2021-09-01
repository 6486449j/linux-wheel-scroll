import os, time, re, subprocess

def GetWindowClass():
    p = subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    window_id = 0
    for line in p.stdout.readlines():
        m = re.match('^.*window id # (.*)$', str(line))
        if(m != None):
            window_id = m.group(1)
        break
    #print(window_id)

    p2 = subprocess.Popen(["xprop", "-id", str(window_id), "WM_CLASS"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    window_class = ""
    for line in p2.stdout.readlines():
        m = re.match('WM_CLASS\(STRING\) = "([\w-]*)".*', str(line))
        if(m != None):
            window_class = m.group(1)
    
    return window_class

while True:
    window_class = GetWindowClass()
    print(window_class)
    if(window_class == "google-chrome"):
        os.popen("echo 2 > /tmp/libinput_discrete_deltay_multiplier")
        print(2)
    else:
        os.popen("echo 1 > /tmp/libinput_discrete_deltay_multiplier")
        print(1)
    time.sleep(0.5)
