from redis_func import *
import json
import os
import sys

verbose = True

def write_file_upd(log):
	if verbose:
		print(log)
	key = 'updater_' + time.strftime("%Y%m%d", time.localtime())
	file = os.path.join(locallog_dir, key+'.log')
	log += ' [' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']'
	write_file(file, log+'\n', 'a+')

def get_old_props():
	try:
		file = os.path.join(props_dir, 'props.cfg')
		data = {}
		with open(file, 'r') as f:
			data = json.load(f)
		return data
	except:
		return {}

def PropUpdate(r):
	old_props = get_old_props() 
	if 'prop_version' in old_props:
		server_ver = float(r.get('prop_version'))
		if server_ver <= float(old_props['prop_version']):
			return

	props = get_props(r)
	key = 'ver_' + str(docker_id)
	r.set(key, props['prop_version'])

	try:
		file = os.path.join(props_dir, 'props.cfg')
		with open(file, 'w+') as f:
			json.dump(props, f)
		write_file_upd('Update finished. version=' + props['prop_version'])
	except:
		log = '[Warning] File writing failed, new properties may not be updated rightly. Please check your config in parameters.py'
		write_file_upd(log)

def BashUpdate(r):
	key = 'bash_' + str(docker_id)
	bashno = 0

	while True:
		bsh = r.rpop(key)
		if bsh == None:
			break
		bsh = bsh.decode('utf8')
		if bsh == '':
			break

		try:
			filename = time.strftime("%Y%m%d_%H%M%S_", time.localtime()) + str(bashno) + '.sh'
			file = os.path.join(bash_dir, filename)
			with open(file, 'w+') as f:
				f.write(bsh)

			# osx
			val = os.system('bash ' + str(file))

			write_file_upd('Bash executed. value=' + str(val) + ' file=\'' + file + '\'')

		except:
			log = '[Warning] Bash executing failed. Please check your config in parameters.py'
			write_file_upd(log)

		bashno += 1

if __name__ == '__main__':
	r, docker_id = login()
	PropUpdate(r)
	BashUpdate(r)

