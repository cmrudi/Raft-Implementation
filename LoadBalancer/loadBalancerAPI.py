from bottle import route, run, request
import requests, sys, os, thread, time

# variables

localhost = ''
local_port = ''
local_addr = ''
leader_addr = ''
array_server = []
cpu_availability = 0


#thread
def heart_beat():
    global array_server
    while len(array_server) <= 1:
        print "heart beat"
        time.sleep(1)
        while len(array_server) > 1:
            time.sleep(5)
            for addr in array_server:
                if (addr != localhost) :
                    response = get_request('http://'+addr+':'+local_port+'/api/heart_beat')
                    
# functions
def search(array,ip):
    for obj in array:
        if (obj==ip):
            return True

    return False

def initialize():
	
    if (len(sys.argv) != 3) :
		print "Plese use following command: Python loadBalancerAPI <current_leader_address> <your_port>"
		print "example python loadBalancerAPI.py 192.168.199.1:5000 4000"
		sys.exit()
	
    global localhost
    global local_port
    global leader_addr
    global local_addr
    shell_response = os.popen('ifconfig wlp2s0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    localhost = shell_response.read()
    localhost = localhost[:-1]
    leader_addr = sys.argv[1]
    local_port = sys.argv[2]
    local_addr = localhost + ':' + local_port
    if (str(local_addr) == str(leader_addr)):
        print
        print('Initiate Leader')
        print
        array_server.append(local_addr)
        thread.start_new_thread(heart_beat, () )
    else:
        response = get_request('http://'+ leader_addr +'/api/join_system/'+local_addr)

        # put response in an array_search
        address = response.text # ip addresses
        panjang = len(address)
        i = 0
        ip = ''
        while (i<panjang):
            c = address[i]
            if not(c=='_'):
                ip += c
            else:
				array_server.append(ip)
				ip = ''
            i = i+1
        print
        print "Current Server in System : ",array_server
        print

def get_request(url):
    print
    print "GET Request to ", url
    response = requests.get(url)
    print "Response -> Status: ", response.status_code,' Text: ', response.text
    print
    return response
    

# route

@route('/api/search_prime/:prime_nth')
def index(prime_nth):
    r = requests.get('https://github.com/cmrudi')
    return '<b>Hello %s!</b>' % prime_nth
    
@route('/api/catch_request/:name')
def index(name):
    return '<b>Hellosss %s!</b>' % name

#API to join the system --Already Tested
@route('/api/join_system/:ip_addr')
def index(ip_addr):
    server_list = ''
    global array_server
    if not(search(array_server,ip_addr)):
        array_server.append(ip_addr)
        
        for addr in array_server:
			server_list += addr + '_'
			if (addr != leader_addr and addr != ip_addr):
				response = request.get('http://'+addr+'api/get_new_server/'+ip_addr)
				print(addr + '- '), response
	
    print
    print "Current Server in System : ",array_server
    print
    return server_list

#API to get new server that join the system    
@route('/api/get_new_server/:ip_addr')
def index(ip_addr):
    array_server.append(ip_addr)
    return 'success'
    
#API to get internal cpu availability percentage --Already Tested
@route('/api/internal_availability/:percentage')
def index(percentage):
    global cpu_availability
    cpu_availability = percentage
    print
    print "Update CPU Availability to ",cpu_availability,"%"
    print
    return 'success'
    
#API to get heartbeat from leader and send cpu availability
@route('/api/heart_beat')
def index():
    global cpu_availability
    print
    print "Get Heartbeat from leader, sending availability ", cpu_availability
    print
    return cpu_availability


# main

if __name__ == '__main__':
    initialize()
    run(host=localhost, port=local_port)
