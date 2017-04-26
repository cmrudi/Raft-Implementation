class Log_element:
	def __init__(self, num, com):
		self.num = num # number
		self.com = com # commited
class Log:
	def __init__(self):
		self.log_elem = []
	
	def print_log(self):
	# print everything in the log
		for obj in self.log_elem:
			print obj.num, obj.com

	def add(self,new_number):
	# adding a number request
		self.log_elem.append(Log_element(new_number,False))

	def commit(self):
	# commit the last value
		self.log_elem[len(self.log_elem)-1].com = True

	def commit_num(self, num_request):
	# commit the latest that has num element numRequest
		i = len(self.log_elem)-1
		while (i>=0):
			if ((self.log_elem[i].num == num_request) and (self.log_elem[i].com == False)):
				self.log_elem[i].com = True
				break
			else:
				i = i-1

	def uncommit(self):
	# uncommit the last value
		self.log_elem[len(self.log_elem)-1].com = False

	def uncommit_num(self, num_request):
	# uncommit the latest that has num element numRequest
		i = len(self.log_elem)-1
		while (i>=0):
			if ((self.log_elem[i].num == num_request) and (self.log_elem[i].com == True)):
				self.log_elem[i].com = False
				break
			else:
				i = i-1

	def check_number(self, num_request):
	# check if there exist the num_request
		for obj in self.log_elem:
			if obj.num==num_request:
				return True

		return False

	def get_commit(self, num_request):
	# get the commit element of the latest num_request
		i = len(self.log_elem)-1
		while (i>=0):
			if (self.log_elem[i].num == num_request):
				return self.log_elem[i].com
			else:
				i = i-1



# main (debuging)
cpu_log = Log()
cpu_log.add(5)
cpu_log.commit()

"""
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
"""
