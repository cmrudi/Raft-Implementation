import multiprocessing, sys, os



if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print
        print "Use following command: python test_nodes.py <number_node>"
        print
        print "Example python test_nodes.py 5"
        print
        sys.exit()

    shell_response = os.popen('ifconfig wlp2s0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    localhost = shell_response.read()
    localhost = localhost[:-1]

    leader_port = '5000'
    leader_addr = localhost + ':' + leader_port 

    n = sys.argv[1]

    command = ''
    for i in range(5, int(n)+5):
        print
        print i
        print
        if (i == int(n)+4):
            command += 'xterm -T NODE'+ localhost +':'+ str((i)*1000) +' -e python loadBalancerAPI.py ' + leader_addr + ' ' + str((i)*1000) + ' & python cpu_usage.py ' + str((i)*1000)
        else:
            command += 'xterm -T NODE'+ localhost +':'+ str((i)*1000) +' -e python loadBalancerAPI.py ' + leader_addr + ' ' + str((i)*1000) + ' & python cpu_usage.py ' + str((i)*1000) + ' & '

    print command
    shell_response = os.popen(command)

