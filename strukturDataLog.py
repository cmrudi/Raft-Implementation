# data structure and data type

class Log_element:
	def __init__(self, ip, term, com):
		self.ip = ip # ip address
		self.term = term # term
		self.com = com # commited

class Log:
	def __init__(self):
		self.log_elem = []
	
	def print_log(self):
	# print everything in the log (untuk debugging)
		for obj in self.log_elem:
			print obj.ip, obj.term, obj.com

	def add(self,new_ip, term):
	# adding a number request
		self.log_elem.append(Log_element(new_ip, term,False))

	def commit(self):
	# commit the last value
		self.log_elem[len(self.log_elem)-1].com = True

	def commit_ip_term(self, ip, term):
	# commit the latest that has num element numRequest
		i = 0
		while (i<len(self.log_elem)):
			if ((self.log_elem[i].ip == ip) and (self.log_elem[i].term == term) and (self.log_elem[i].com == False)):
				self.log_elem[i].com = True
				break
			else:
				i = i+1

	def uncommit(self):
	# uncommit the last value
		self.log_elem[len(self.log_elem)-1].com = False

	def uncommit_ip_term(self, ip, term):
	# uncommit the latest that has num element numRequest
		i = 0
		while (i<len(self.log_elem)):
			if ((self.log_elem[i].ip == ip) and (self.log_elem[i].term == term) and (self.log_elem[i].com == True)):
				self.log_elem[i].com = False
				break
			else:
				i = i+1

	def check_ip(self, ip):
	# check if there exist the num_request
		for obj in self.log_elem:
			if (obj.ip == ip):
				return True

		return False

	def get_commit(self, ip, term):
	# get the commit element of the latest num_request
		i = len(self.log_elem)-1
		while (i>=0):
			if (self.log_elem[i].ip == ip) and (self.log_elem[i].term == term):
				return self.log_elem[i].com
			else:
				i = i-1

	def get_last_ip(self):
		return self.log_elem[len(self.log_elem)-1].ip
	def get_log_length(self):
		return len(self.log_elem)

	def get_log_address(self, idx):
		return self.log_elem[idx].ip

	def get_log_term(self, idx):
		return self.log_elem[idx].term

	def get_log_commit(self, idx):
		return self.log_elem[idx].com

# main (debuging)
"""
log = Log()

log.add("ip1",30)
log.add("ip2",38)
log.add("ip3",18)
log.add("ip2",18)
log.add("ip1",18)
log.add("ip4",20)
log.add("ip5",20)
log.add("ip6",30)
log.add("ip7",38)
log.add("ip8",18)
# commit(log)
log.add("ip1",20)
log.add("ip2",30)
log.add("ip8",38)
log.add("ipip",1277)

log.commit_ip_term("ip1",18)
log.commit_ip_term("ip3",18)
log.commit_ip_term("ip",18)

# log[1].num = 40

# print log.check_number(18)
# print log.get_commit(18)

log.print_log()
"""
