from flask import Flask, flash, render_template, request, redirect
import subprocess
import os
import time

app = Flask(__name__)
app.debug = True


@app.route('/', methods = ['GET', 'POST'])
def index():
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return render_template('app.html', vol=vol, input=input, filter=filter)

@app.route('/wifi')
def wifi():
    wifi_ap_array = scan_wifi_networks()

    return render_template('wifi.html', wifi_ap_array = wifi_ap_array)

@app.route('/manual_ssid_entry')
def manual_ssid_entry():
    return render_template('manual_ssid_entry.html')

@app.route('/save_credentials', methods = ['GET', 'POST'])
def save_credentials():
    ssid = request.form['ssid']
    wifi_key = request.form['wifi_key']
    create_wpa_supplicant(ssid, wifi_key)
    os.system('bash /tmp/wifi.tmp')
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return redirect('/')

@app.route("/volume2", methods = ['GET', 'POST'])
def volume2():
    if request.method == 'POST':
        a = request.form["c"]
        create_file(a)
        os.system('mpc volume $(cat /root/vol)> /dev/null 2>&1')
        with open("/root/filter", "r") as f:
             filter = f.read()
        with open("/root/vol", "r") as f:
             vol = f.read()
        with open("/root/input", "r") as f:
             input = f.read()
        return redirect('/')
    else:
        with open("/root/vol", "r") as f:
            vol = f.read()
            return vol

@app.route("/volume", methods = ['GET', 'POST'])
def volume():
    if request.method == 'POST':
        a = request.form["a"]
        create_file(a)
        os.system('mpc volume $(cat /root/vol)> /dev/null 2>&1')
        with open("/root/filter", "r") as f:
                filter = f.read()
        with open("/root/vol", "r") as f:
                vol = f.read()
        with open("/root/input", "r") as f:
                input = f.read()
        return redirect('/')
    else:
        with open("/root/vol", "r") as f:
            vol = f.read()
            return vol

@app.route('/input', methods = ['GET', 'POST'])
def input():
    input = request.form["input"]
    if input == "S1":
         os.system('amixer cset numid=2 0 >/dev/nul')
         os.system('echo "(1)" > /root/input')
    if input == "S2":
         os.system('amixer cset numid=2 1 >/dev/nul')
         os.system('echo "(2)" > /root/input')
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return redirect('/')

@app.route('/test', methods = ['GET', 'POST'])
def test():
    test = request.form["test"]
    if test == "sound":
        os.system('bash /root/test')
    if test == "net":
        os.system('bash /root/net')
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return redirect('/')

@app.route('/filter', methods = ['GET', 'POST'])
def filter():
    filter = request.form["filter"]
    if filter == "nos":
        os.system('amixer cset numid=5 1 >/dev/nul')
        os.system('echo "(Nos)" > /root/filter')
    if filter == "slow":
        os.system('amixer cset numid=5 0 >/dev/nul')
        os.system('amixer cset numid=4 1 >/dev/nul')
        os.system('echo "(Slow)" > /root/filter')
    if filter == "fast":
        os.system('amixer cset numid=5 0 >/dev/nul')
        os.system('amixer cset numid=4 0 >/dev/nul')
        os.system('echo "(Fast)" > /root/filter')
    if filter == "min-phase":
        os.system('amixer cset numid=5 0 >/dev/nul')
        os.system('amixer cset numid=4 2 >/dev/nul')
        os.system('echo "(M-F)" > /root/filter')
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return redirect('/')

@app.route('/power')
def power():
    return render_template('power.html')

@app.route('/reboot', methods = ['GET', 'POST'])
def reboot():
    os.system('bash -c "sleep 1; reboot"&')
    return redirect('/')

@app.route('/poweroff', methods = ['GET', 'POST'])
def poweroff():
    os.system('bash -c "sleep 1; poweroff"&')
    return redirect('/')

@app.route('/prev', methods = ['GET', 'POST'])
def prev():
    os.system('mpc prev')
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return redirect('/')

@app.route('/play', methods = ['GET', 'POST'])
def play():
    os.system('mpc toggle')
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return redirect('/')

@app.route('/stop', methods = ['GET', 'POST'])
def stop():
    os.system('mpc stop')
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return redirect('/')

@app.route('/next', methods = ['GET', 'POST'])
def next():
    os.system('mpc next')
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return redirect('/')

######## FUNCTIONS ##########

def create_file(a):

    temp_conf_file = open('/root/vol', 'w')
    temp_conf_file.write('' + a + '')
    temp_conf_file.close

def scan_wifi_networks():
    iwlist_raw = subprocess.Popen(['iwlist','wlan0','scan'], stdout=subprocess.PIPE)
    ap_list, err = iwlist_raw.communicate()
    ap_array = []

    for line in ap_list.decode('utf-8').rsplit('\n'):
        if 'ESSID' in line:
            ap_ssid = line[27:-1]
            if ap_ssid != '':
                ap_array.append(ap_ssid)

    return ap_array

def create_wpa_supplicant(ssid, wifi_key):

        os.system('nmcli con add ifname wlan0 type wifi ssid ' + ssid + ' wifi-sec.key-mgmt wpa-psk wifi-sec.psk ' + wifi_key + ' ')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)
