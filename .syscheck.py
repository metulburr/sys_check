import subprocess, os

#gksu gedit /etc/bash.bashrc

RESET = '\x1b[0m'
START = '\x1b[31m'

def twocmd(cmd, arg, search=None):
    proc = subprocess.Popen([cmd, arg], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = proc.communicate()[0]
    stdout = stdout.decode()
    
    stdout = stdout.split('\n')
    
    if search == None:
        return stdout[0]
    
    for index in stdout:
        if search in index:
            item = index
            break
    return item


cpu = twocmd('cat', '/proc/cpuinfo', 'model name')
cpu = cpu[cpu.find(':')+2:]

bit = twocmd('getconf', 'LONG_BIT')
kern = twocmd('uname', '-r')

desc  = twocmd('cat', '/etc/lsb-release', 'DESCRIPTION')
desc = desc[desc.find('='):].strip('=').strip('"')

code = twocmd('cat', '/etc/lsb-release', 'CODENAME')
code = code[code.find('='):].strip('=')

core = twocmd('cat', '/proc/cpuinfo', 'siblings')
core = core[core.find(':')+2:]

ram = twocmd('free', '-m', 'Mem')
allram = []
for word in ram.split():
    allram.append(word)
#used_ram = allram[2]
total_ram = allram[1]

ram = twocmd('free', '-m', 'buffers/cache')
allram = []
for word in ram.split():
    allram.append(word)
used_ram = allram[2]


part = twocmd('df', '-h', 'dev')
allpart = []
for word in part.split():
    allpart.append(word)
used_part = allpart[2][:-1]
total_part = allpart[1][:-1]


try:
	try:
	    desk = os.environ['XDG_CURRENT_DESKTOP']
	except KeyError:
	    desk = os.environ['DESKTOP_SESSION']
except:
	desk = 'None'



print(START,'DISTRIBUTION:', RESET, desc, code)
print(START,'     DESKTOP:',RESET, desk)
print(START,'        USER:',RESET, os.environ['USER'])
print(START,'      KERNAL:',RESET, kern)
print(START,'         BIT:',RESET, bit)
print(START,'         CPU:',RESET, cpu, '[{}] Core'.format(core))
print(START,'   PARTITION:',RESET, used_part + ' / ' + total_part + ' GB')
print(START,'         RAM:',RESET, used_ram + ' / ' + total_ram + ' MB')
print()


