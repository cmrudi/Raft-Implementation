from bottle import route, run, request
import requests
import sys
import os


def search(array,ip):
    for obj in array:
        if (obj==ip):
            return True

    return False

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

#API to join the system
@route('/api/join_system/:ip_addr')
def index(ip_addr):
    server_list = ''
    global array_server
    if not(search(array_server,ip_addr)):
        array_server.append(ip_addr)
        
        for addr in array_server:
			server_list += addr + '_'
			if (addr != leader_host):
				response = request.get('http://'+addr+'api/get_new_server/'+ip_addr)
				print(addr + '-'response )
    return server_list

#API to get new server that join the system    
@route('/api/get_new_server/:ip_addr')
def index(ip_addr):
    array_server.append(ip_addr)
    return 'success'
 
 





def initialize():
    global localhost
    global leader_host
    shell_response = os.popen('ifconfig wlp2s0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    localhost = shell_response.read()
    localhost = localhost[:-1]
    leader_host = sys.argv[1]  
    if (str(localhost) == str(leader_host)):
        print('Initiate Leader')
        array_server.append(localhost)
    else:
		url = 'http://'+ leader_host + ':' + local_port +'/api/join_system/'+localhost
		print(url)
		response = requests.get(url)
		print(response.text);
		array_server = response
		array_server.append(response)

if __name__ == '__main__':
    initialize()
    run(host=localhost, port=local_port)
