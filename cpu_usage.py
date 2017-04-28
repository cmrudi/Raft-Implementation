#class for sending get Request of memory availability percentage to node

import psutil, time, requests, os, sys


local_port = ''

shell_response = os.popen('ifconfig wlp2s0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
localhost = shell_response.read()
localhost = localhost[:-1]

if (len(sys.argv) != 2) :
    print "Plese use following command: Python cpu_usage.py <your_port>"
    print "example python cpu_usage.py 5000"
    sys.exit()
local_port = sys.argv[1]

while 1:
    time.sleep(5)

    # get cpu_usage percentage
    avail_mem = str(psutil.virtual_memory().available*100/psutil.virtual_memory().total);
    print
    print
    print "Memory= "+avail_mem+ " %"
    url = 'http://'+localhost+':'+local_port+'/api/internal_availability/'+str(avail_mem)
    print "GET Request to ", url
    response = requests.get(url)
    print "Response -> Status: ", response.status_code,' Text: ', response.text

