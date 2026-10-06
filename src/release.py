"""Incrémente la version du cache dans sw.js (japonais-vNN) après un build."""
import re, os
p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sw.js')
s = open(p).read()
m = re.search(r'japonais-v(\d+)', s)
n = int(m.group(1)) + 1
open(p, 'w').write(re.sub(r'japonais-v\d+', f'japonais-v{n}', s))
print('cache ->', f'japonais-v{n}')
