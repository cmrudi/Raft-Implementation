import multiprocessing, sys, os

def worker(file):
    os.system("python "+file)



if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print "Plese use following command: Python run_all.py <current_leader_address> <your_port>"
        print "example python run_all.py 192.168.199.1:5000 4000"

    shell_response = os.popen('ifconfig wlp2s0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    localhost = shell_response.read()
    localhost = localhost[:-1]

    port = sys.argv[2]

    leader_address = sys.argv[1]

    path = os.getcwd()
    files = [path+"/loadBalancerAPI.py "+leader_address+" "+port, path+"/cpu_usage.py "+port]
    for file in files:
        process = multiprocessing.Process(target=worker(file))
        process.start()



