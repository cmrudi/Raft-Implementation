import psutil, time, requests, os


local_port = '5000'

shell_response = os.popen('ifconfig wlp2s0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
localhost = shell_response.read()
localhost = localhost[:-1]

while 1:
    avail_mem = str(psutil.virtual_memory().available*100/psutil.virtual_memory().total);
    print("Memory= "+avail_mem+ " %")
    time.sleep(5)
    requests.get('http://'+localhost+':'+local_port+'/api/internal_availablity/'+str(avail_mem))

