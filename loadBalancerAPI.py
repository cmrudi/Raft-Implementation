from bottle import route, run, request
import requests, sys, os, thread, time
from strukturDataLog import Log

# variables

localhost = ''
local_port = ''
local_addr = ''
leader_addr = ''
array_server = []
cpu_availability = 0
timecount = 0
main_log = Log()
term = 1
position = 0 #1 as leader, 2 as follower, 3 as candidate

#thread
def heart_beat():
    global array_server
    global cpu_availability
    global term
    global main_log
    while len(array_server) <= 1:
        print "Waiting for follower"
        time.sleep(1)
        while len(array_server) > 1:
            print "Starting heart beat"
            time.sleep(5)
            max_availability_number = cpu_availability
            max_availability_address = local_addr
            for addr in array_server:
                if (addr != local_addr) :
                    response = get_request('http://'+addr+'/api/heart_beat')
                    if (max_availability_number < int(response.text)):
                        max_availability_number = int(response.text)
                        max_availability_address = addr
            #Enter address which has max availability to local log
            print
            print "Push new log address= "+max_availability_address+"  term= " + str(term)
            print
            main_log.add(max_availability_address,term)
            
            add_log_success = 1
            #Spread log to follower
            for addr in array_server:
                if (addr != local_addr) :
                    response = get_request('http://'+addr+'/api/spread_log/'+max_availability_address+'/'+str(term))
                    if (int(response.status_code) == 200):
                        add_log_success += 1
            print
            print "Number add log success = ", add_log_success
            print "Number Majority = ", len(array_server) / 2 + 1
            print
            if (add_log_success >= len(array_server) / 2 + 1) : 
                #Commit to internal log
                main_log.commit_ip_term(max_availability_address,term)
                #Commit log to follower
                for addr in array_server:
                    if (addr != local_addr) :
                        response = get_request('http://'+addr+'/api/commit_log/'+max_availability_address+'/'+str(term))
                                               

def increment_time():
    global timecount
    global position
    
    while (timecount<10):
        time.sleep(1)
        timecount += 1
    print "timeout"
    position = 3
    thread.start_new_thread(leader_election, () )

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
    global timecount

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
        thread.start_new_thread(increment_time, () )
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

#Leader Election
def leader_election():
    global array_server
    global local_addr
    global term
    global position

    #candidate
    if (position == 3) :
        success_vote = 1
        for addr in array_server:
            if (addr != local_addr) :
                response = get_request('http://'+addr+'/api/vote_leader/'+local_addr+'/'+str(term))
                if (response.text == 'yes'):
                    success_vote += 1
        print "Number success vote = ", success_vote
        print "Number Majority = ", len(array_server) / 2 + 1
        print
        if (success_vote >= len(array_server) / 2 + 1) : 
            position = 1
            print "I am the leader!"
            
    

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
    global timecount
    print
    print "Get Heartbeat from leader, sending availability ", cpu_availability
    timecount = 0
    print
    return str(cpu_availability)
    
#API for catch new log from leader
@route('/api/spread_log/:address/:term')
def index(address, term):
    print
    print "Push new log address= "+address+"  term= " + term
    print
    main_log.add(address,term)
    return 'success'
    
#API for commit log from leader
@route('/api/commit_log/:address/:term')
def index(address, term):
    print
    print "Commit log address= "+address+"  term= " + term
    print
    main_log.commit_ip_term(address,term)
    return 'success'

#API for catch new log from leader
@route('/api/vote_leader/:address/:term')
def index(address, term):
    print
    print "Vote for new leader= "+address+"  term= " + term
    print
    #mekanisme penentuan 'yes' atau 'no'

    return 'yes'




# main

if __name__ == '__main__':
    initialize()
    run(host=localhost, port=local_port)
