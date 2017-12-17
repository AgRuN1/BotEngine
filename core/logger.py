def log_info(msg):
	log_file = open('log/info.txt', 'a')
	log_file.write(str(msg)+"\n")
	log_file.close()

def log_error(msg):
	log_file = open('log/error.txt', 'a')
	log_file.write(str(msg)+"\n")
	log_file.close()