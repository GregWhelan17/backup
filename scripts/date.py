from  datetime import datetime
import re

now=datetime.now().strftime('%Y%m%d-%H%M%S')
print(now)

files=[
    '/pvcs/sdfs/asfasfa/asfasf',
    '/pvcs/a/asasf/asfasfa/fsasth',
    '/pvcs/yukjgj/gkjgjf/gyitfjgcc/fgf'
]

for file in files:
    a=file.replace('/pvcs', now)
    print(f'{file} - {a}')

for new in [e.replace('/pvcs', now) for e in files]:
    print(new)
    