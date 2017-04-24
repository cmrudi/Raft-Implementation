from bottle import route, run, request
import requests
import sys
import os


localhost = ''
leader_host = ''
local_port = '5000'
array_server = []

@route('/api/search_prime/:prime_nth')
def index(prime_nth):
    r = requests.get('https://github.com/cmrudi')
    return '<b>Hello %s!</b>' % localhost
    
@route('/api/catch_request/:name')
def index(name):
    return '<b>Hellosss %s!</b>' % name

@route('/api/join_system/:ip_addr')
def index(ip_addr):
    global array_server
    array_server.append(ip_addr)
    return '<b>Hello %s!</b>' % ip_addr





def initialize():
	
	
    global localhost
    global leader_host
    shell_response = os.popen('ifconfig wlp2s0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    localhost = shell_response.read()
    localhost = localhost[:-1]
    leader_host = sys.argv[1]  
    if (str(localhost) == str(leader_host)):
        print('Initiate Leader')
    else:
		url = 'http://'+ leader_host + ':' + local_port +'/api/join_system/'+localhost
		print(url)
		response = requests.get(url)
		print(response);

if __name__ == '__main__':
    initialize()
    run(host=localhost, port=local_port)
