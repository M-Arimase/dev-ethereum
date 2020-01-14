from redis_func import *

r, docker_id = login()
push_bash(r, 'test_bash.sh', [2])

# r = login()
# r.set('bash_2', '#!/bin/sh\necho -e \'dfs\' >> log.txt')
# print(r.get('bash_1').decode('utf-8'))
# props = get_props(r)
# print(props)

# write_log('first log', r, local_only = True)
# write_log('second log', r, fatal_error = True)