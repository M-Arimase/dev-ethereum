import redis
import time
import os
from parameters import *

# need to update (/proc/self/cgroup)
def get_dockerid(r):
	num_docker = int(r.get('num_docker').decode('utf-8'))
	docker_id = num_docker + 1
	r.set('num_docker', str(docker_id))
	return docker_id

def login():
	alloc_dockerid = False
	if not os.path.exists('docker_id'):
		alloc_dockerid = True
	else:
		with open('docker_id', 'r') as f:
			docker_id = f.readline()
			if docker_id == '':
				alloc_dockerid = True

	r = redis.Redis(host=redis_host, port=redis_port, db=0, password=redis_pwd)
	
	if alloc_dockerid:
		docker_id = get_dockerid(r)
		with open('docker_id', 'w') as f:
			f.write(str(docker_id))

	key = 'login_' + str(docker_id)
	r.set(key, time.time())
	return r

def get_keys(r):
	return r.keys('prop_*')

def get_props(r):
	keys = get_keys(r)
	values = r.mget(keys)
	# convert bytes into str
	props = {k.decode('utf-8'):v.decode('utf-8') for (k, v) in zip(keys, values)}
	return props

def write_log(log, r, fatal_error = False, local_only = False):
	# log: [id][WARNING/ERROR] log [time]
	txt  = '[' + str(docker_id) + ']'
	txt += '[' + ('ERROR' if fatal_error else 'WARNING') + ']'
	txt += ' ' + log + ' '
	txt += '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']'
	
	key = 'logs_' + str(docker_id) + '_' + time.strftime("%Y%m%d", time.localtime())
	
	# sync to redis
	if not local_only:
		r.lpush(key, txt)

	file = os.path.join(locallog_dir, key+'.log')
	write_file(file, txt+'\n', 'a+')

def write_file(file, txt, mode='a+'):
	try:
		with open(file, mode) as f:
			f.write(txt)
	except:
		print('[Warning] Local file \'' + file + '\' writing failed. Please check your config in parameters.py')

def push_bash(r, file, docker_list):
	with open(file, 'r') as f:
		bsh = f.read()
		print(bsh)
		for did in docker_list:
			key = 'bash_' + str(did)
			r.lpush(key, bsh)
		print('Bash pushing finished.\n')

