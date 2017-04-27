import multiprocessing, sys, os



if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print
        print "Use following command: python run.py <current_leader_address> <your_port>"
        print
        print "Example python run.py 192.168.199.1:5000 4000"
        print
        sys.exit()

    

    port = sys.argv[2]

    leader_address = sys.argv[1]

    shell_response = os.popen('xterm -e python loadBalancerAPI.py ' + leader_address + ' ' + port + '& xterm -e python cpu_usage.py ' + port)



