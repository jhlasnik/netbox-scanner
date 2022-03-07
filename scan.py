import yaml, sys
from icmplib import multiping, NameLookupError
from dns import resolver, reversename, exception

try:
    with open(r'addresses.yml') as var_file:
       addresses = yaml.load(var_file, Loader=yaml.FullLoader)
except yaml.parser.ParserError:
  sys.exit('\nError: A YAML Parser Error was detected, check your variable file syntax.\n')
except  FileNotFoundError:
  sys.exit('\nError: The required variable file: addresses.yml could not be found, it is required to be located in the same directory as the file.\n')
except:
  sys.exit('\nError: An error occured while trying to import the YAML variable file.\n')

print(addresses)

results=multiping(addresses, count=2, interval=0.5, timeout=2, concurrent_tasks=50, privileged=False)

alive=[]
dead=[]
for host in results:
    if host.is_alive:
        try:
            qname = reversename.from_address(host.address)
            answer = resolver.resolve(qname, 'PTR')
            alive.append(str(answer[0]))
        except resolver.NXDOMAIN:
            alive.append(host.address)
        
    else:
        try:
            qname = reversename.from_address(host.address)
            answer = resolver.resolve(qname, 'PTR')
            dead.append(str(answer[0]))
        except resolver.NXDOMAIN:
            dead.append(host.address)

for host in alive:
    print(f'Alive: {host}')

print('################################')

for host in dead:
    print(f'Dead: {host}')