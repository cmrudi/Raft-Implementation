class Log_element:
    def __init__(self, num, com):
        self.num = num # number
        self.com = com # commited

def print_log(log):
# print everything in the log
	for obj in log:
		print obj.num, obj.com

def add(log,new_number):
# adding a number request
	log.append(Log_element(new_number,False))

def commit(log):
# commit the last value
	log[len(log)-1].com = True

def commit_num(log, num_request):
# commit the latest that has num element numRequest
	i = len(log)-1
	while (i>=0):
		if ((log[i].num == num_request) and (log[i].com == False)):
			log[i].com = True
			break
		else:
			i = i-1

def uncommit(log):
# uncommit the last value
	log[len(log)-1].com = False

def uncommit_num(log, num_request):
# uncommit the latest that has num element numRequest
	i = len(log)-1
	while (i>=0):
		if ((log[i].num == num_request) and (log[i].com == True)):
			log[i].com = False
			break
		else:
			i = i-1

def check_number(log, num_request):
# check if there exist the num_request
	for obj in log:
		if obj.num==num_request:
			return True

	return False

def get_commit(log, num_request):
# get the commit element of the latest num_request
	i = len(log)-1
	while (i>=0):
		if (log[i].num == num_request):
			return log[i].com
		else:
			i = i-1



# main (debuging)
log = []

add(log,5)
commit(log)
add(log,30)
add(log,38)
add(log,18)
add(log,18)
add(log,18)
add(log,20)
add(log,20)
add(log,30)
add(log,38)
add(log,18)
# commit(log)
add(log,20)
add(log,30)
add(log,38)
add(log,1277)

commit_num(log,18)
commit_num(log,18)
commit_num(log,18)
uncommit_num(log,18)

log[1].num = 40

print check_number(log,18)
print get_commit(log,18)

print_log(log)

print len(log)

x = 17
y = 25
z = 0
print z
