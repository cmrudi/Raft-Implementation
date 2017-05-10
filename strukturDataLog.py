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
		print "Print Log"
		print
		for obj in self.log_elem:
			print obj.ip, obj.term, obj.com
		print
		print

	def add(self,new_ip, term):
	# adding a number request
		self.log_elem.append(Log_element(new_ip, term,False))

	def replace_last_log(self,new_ip, term):
		length = len(self.log_elem) -1;
		self.log_elem[int(lenth)] = Log_element(new_ip, term, False)



	def recovery(self, new_ip, term, idx):
		self.log_elem[int(idx)] = Log_element(new_ip, term, True)

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
		i = len(self.log_elem)-1
		while (i>=0):
			if (self.log_elem[i].com == True):
				return self.log_elem[i].ip
			else:
				i = i-1
		return 'None'


	def get_log_length(self):
		return len(self.log_elem)

	def get_log_address(self, idx):
		return self.log_elem[idx].ip

	def get_log_term(self, idx):
		return self.log_elem[idx].term

	def get_log_commit(self, idx):
		return self.log_elem[idx].com





