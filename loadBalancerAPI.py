
from bottle import route, run, request
import requests, sys, os, thread, time
from strukturDataLog import Log
from get import Get
from random import randint
import traceback

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
election = False
T = 40
election_timeout = randint(T,2*T)
hasVoted = False
onRecovery = False

#thread
def heart_beat():
    global array_server
    global cpu_availability
    global term
    global main_log
    global leader_addr
    global local_addr
    global position

    try:
        while len(array_server) <= 1:
            if (term==1):
                print "Waiting for follower, you have 20 seconds"
                time.sleep(20)
        while len(array_server) > 1 and position == 1:
            leader_addr = local_addr
            print_log("Starting heart beat")
            time.sleep(5)
            max_availability_number = cpu_availability
            max_availability_address = local_addr
            for addr in array_server:
                if (addr != local_addr) :
                    url = 'http://'+addr+'/api/heart_beat/'+str(term);
                    print "Get Request to ", url
                    response = get_request('http://'+addr+'/api/heart_beat/'+str(term))
                    if (max_availability_number < int(response.text)):  
                        max_availability_number = int(response.text)
                        max_availability_address = addr
            #Enter address which has max availability to local log
            #print_log("Push new log address= "+max_availability_address+"  term= " + str(term)) 
            
            main_log.add(max_availability_address,term)
            
            add_log_success = 1
            #Spread log to follower

            while (add_log_success < len(array_server) / 2 + 1 ):
                time.sleep(2)
                add_log_success = 1
                idx = 0
                last_address = '0'
                last_term = 1

                if (main_log.get_log_length() > 1):
                    idx = main_log.get_log_length() - 1
                    last_address = main_log.get_log_address(idx)
                    term = main_log.get_log_term(idx)

                for addr in array_server:
                    if (addr != local_addr) :
                        response = get_request('http://'+addr+'/api/spread_log/'+max_availability_address+'/'+str(term)+'/'+str(idx)+'/'+last_address+'/'+str(last_term))
                        if (response.text == 'success'):
                            add_log_success += 1
                        

                #print_log("Number add log success = " +  str(add_log_success))
                #print_log("Number Majority = " + str(len(array_server) / 2 + 1))

                if (add_log_success >= len(array_server) / 2 + 1) : 
                    #Commit to internal log
                    main_log.commit_ip_term(max_availability_address,term)
                    #main_log.print_log()
                    #Commit log to follower
                    for addr in array_server:
                        if (addr != local_addr) :
                            response = get_request('http://'+addr+'/api/commit_log/'+max_availability_address+'/'+str(term)+'/'+str(idx))
        

    except Exception:
        print traceback.format_exc()

#used by follower to recover log
def recovery():
    print_log('Start Recovery')
    global main_log
    global onRecovery
    fit = False
    idx = 0;
    length = 2;
    while not fit and idx < length :
        response = get_request('http://'+leader_addr+'/api/get_log/'+str(idx))
        print_log(response);
        term, address, length = (response.text).split("-")
        main_log.add(address,term)
        main_log.commit_ip_term(address,term)
        main_log.print_log()
        idx = idx + 1;
        if (idx == length):
            fit = True;
            onRecovery = False;
    print_log("Check out from log recovery loop")
                                               

def increment_time():
    global timecount
    global position
    global election
    global election_timeout 

    while (position!=1):

        while (timecount<election_timeout):
            time.sleep(1)
            if not (election):
                timecount += 1
            # print timecount
        print_log("election timeout = " + str(election_timeout))
        position = 3 # candidate
        election = True

        while (election):
            pass


# functions
def search(array,ip):
    for obj in array:
        if (obj==ip):
            return True

    return False

def follower():
    while (position!=1) :
        # do nothing
        pass
    thread.start_new_thread(heart_beat, () )

def print_log(log):
    print
    print log
    print

def initialize():
    
    if (len(sys.argv) < 3) :
        print "Plese use following command: Python loadBalancerAPI <current_leader_address> <your_port>"
        print "example python loadBalancerAPI.py 192.168.199.1:5000 4000"
        sys.exit()
    
    global localhost
    global local_port
    global leader_addr
    global local_addr
    global timecount
    global position

    shell_response = os.popen('ifconfig wlp2s0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    localhost = shell_response.read()
    localhost = localhost[:-1]
    leader_addr = sys.argv[1]
    local_port = sys.argv[2]
    local_addr = localhost + ':' + local_port
    if (str(local_addr) == str(leader_addr)):
        position = 1 # leader
        print_log("Initiate Leader")
        array_server.append(local_addr)
        thread.start_new_thread(heart_beat, () )
    elif (len(sys.argv) == 4):
        print_log("Server Hidup Kembali")
        if (sys.argv[3] == 'restart'):
            thread.start_new_thread(increment_time, () )
            thread.start_new_thread(leader_election, () )
            thread.start_new_thread(follower, () )
    else:
        print_log("Start Follower")
        time.sleep(2)
        position = 2 # follower
        response = get_request('http://'+ leader_addr +'/api/join_system/'+local_addr)
        thread.start_new_thread(increment_time, () )
        thread.start_new_thread(leader_election, () )
        
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
        #print
        #print "Current Server in System : ",array_server
        #print
        thread.start_new_thread(follower, () )
        

#Leader Election
def leader_election():
    global array_server
    global local_addr
    global term
    global position
    global term
    global hasVoted
    global election
    global timecount

    while (position != 1) :
        while not(election) or (position!=3):
            pass

        # condition = timeout
        hasVoted = False
        # election has started 

        term += 1
        if not(hasVoted):
            success_vote = 1 # vote for thyself
            hasVoted = True
        print len(array_server)
        for addr in array_server:
            print 'ke' + addr
            if (addr != local_addr) :
                print 'kirim rikues dari' + addr
                response = get_request('http://'+addr+'/api/vote_leader/'+local_addr+'/'+str(term))
                if (response.text == 'yes'):
                    success_vote += 1
        print "Number success vote = ", success_vote
        print "Number Majority = ", len(array_server) / 2 + 1
        print
        timecount = 0

        if (success_vote >= len(array_server) / 2 + 1) : 
            print "I am the leader!"
            position = 1
        else : position = 2 # back to follower
        election = False

    # tell the followers through api
    for addr in array_server:
        if ((addr != local_addr) and (addr != leader_addr)) :
            response = get_request('http://'+addr+'/api/make_me_leader/'+local_addr+'/'+str(term))
            # if (response.text == 'ok'):

def get_request(url):
    try:
        #print
        #print "GET Request to ", url
        response = requests.get(url)
        #print "Response -> Status: ", response.status_code,' Text: ', response.text
        #print
        return response
    except requests.exceptions.RequestException as e:
        # raise e
        print
        print "============="
        print "Request GAGAL"
        print "============="
        print
        if "heart_beat" or "spread_log" or "commit_log" or "vote_leader" in url :
            return Get()
    

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
                print "New Server Join Success"
                print
                print
                print
                print
                response = get_request('http://'+addr+'/api/get_new_server/'+ip_addr)
                print(addr + '- '), response
            else:
                print "New Server Join Failed"
                print
                print
                print
                print
    
    print
    print "Current Server in System : ",array_server
    print
    return server_list

#API to get new server that join the system    
@route('/api/get_new_server/:ip_addr')
def index(ip_addr):
    global array_server
    print
    print
    print
    print "New server join system, address ",ip_addr
    print
    print
    print
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
@route('/api/heart_beat/:_term')
def index(_term):
    #handling old leader
    global local_addr
    global leader_addr
    if (local_addr == leader_addr) :
        leader_addr = ''
        position = 2

    global array_server
    global cpu_availability
    global timecount
    print
    print "Get Heartbeat from leader, sending availability ", cpu_availability
    print array_server
    timecount = 0
    print
    return str(cpu_availability)
    
#API for catch new log from leader
@route('/api/spread_log/:address/:term/:idx/:last_address/:last_term')
def index(address, term, idx, last_address, last_term):
    #print_log("Push new log address= "+address+"  term= " + term)
    global main_log
    global onRecovery
    idx = int(idx)
    if (idx != 0):
        if (main_log.get_log_length() == idx):
            if (main_log.get_log_term(idx - 1) == last_term and main_log.get_log_address(idx - 1) == last_address):
                main_log.add(address,term)
                return 'success'
            else:
                return 'failed'
        else:
            #print main_log.print_log()
            # print "Leader Log at idx=",idx-1,"  last_term=",last_term,"   last_address=",last_address
            # print "Curren Log at idx=",idx-1,"  last_term=",main_log.get_log_term(idx - 1),"   last_address=",main_log.get_log_address(idx - 1)
            if (onRecovery == False):
                onRecovery = True;
                thread.start_new_thread(recovery, () )
            return 'failed'
    else:
        main_log.add(address,term)
        return 'success'


    
#API for commit log from leader
@route('/api/commit_log/:address/:term/:idx')
def index(address, term, idx):
    #print_log("Commit log address= "+address+"  term= " + term)
    global main_log
    idx = int(idx)
    if (main_log.get_log_length() == idx):
        if (main_log.get_log_term(idx) == term and main_log.get_log_address(idx) == address):
            main_log.commit_ip_term(address,term)
            #main_log.print_log()
            return 'success'
        else:
            return 'failed';
    else:
        return 'failed';


#API for catch new log from leader
@route('/api/vote_leader/:address/:req_term')
def index(address, req_term):
    global term
    global election
    global hasVoted
    global election_timeout
    global timecount
    global T

    timecount = 0
    election_timeout = randint(T,2*T)
    election = True

    # mekanisme penentuan 'yes' atau 'no'
    # no: term t  atau lebih besar dari request
    # yes: term lebih kecil dari term request
    if ((term<int(req_term) )and not(hasVoted)) :
        print
        print "Vote for new leader= " + address + "  term= " + req_term
        print
        election = False
        hasVoted = True
        return 'yes'
    else :
        election = False
        return 'no'


#API for catch Leading announcment
@route('/api/make_me_leader/:address/:req_term')
def index(address, req_term):
    global term
    global election
    global leader_addr
    global hasVoted
    global election

    election = False
    hasVoted = False
    position = 2
    
    return 'ok'


#API for get log from leader for recovery
@route('/api/get_log/:idx')
def index(idx):
    global main_log
    main_log.print_log()
    idx = int(idx)
    length = main_log.get_log_length()
    return str(main_log.get_log_term(idx)) + '-' + str(main_log.get_log_address(idx)) + '-' + str(length)

#Request N (number) by Client, routing to lowest CPU usage IP
@route('/:prime_nth')
def index(prime_nth):
    global main_log
    global local_addr
  
    #last committed IP, with max availability usage of CPU
    freeIp = main_log.get_last_ip()

    #No committed IP, run the worker directly
    if (freeIp == 'None') :
        response = get_request('http://localhost:13337/'+str(prime_nth))
        return response.text;


    #the current node is the IP
    if (freeIp == local_addr) :
        response = get_request('http://localhost:13337/'+str(prime_nth))
        return response.text;

    #Directing route to the free IP, not the current node
    else :
        response = get_request('http://'+freeIp+'/api/worker_request/'+str(prime_nth))        
        return response.text;

#Directing to Worker
@route('/api/worker_request/:prime_nth')
def index(prime_nth):
    global local_addr
  
    response = get_request('http://localhost:13337/'+str(prime_nth))
    return response.text;

# main
if __name__ == '__main__':
    initialize()
    run(host=localhost, port=local_port)
