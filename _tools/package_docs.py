"""Copies the user guide into the plugin for packaging: Plugins/SuperVoxel/Docs/Manual, Markdown without the site's
front matter or writer files. Run from anywhere: python Docs/Site/_tools/package_docs.py [<plugin Docs folder>]."""
import io
import os
import re
import shutil
import sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(SITE))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'Plugins', 'SuperVoxel', 'Docs', 'Manual')
SKIP = {'README.md', '_template.md', 'PUBLISH.md'}

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
count = 0
for root, dirs, files in os.walk(SITE):
    dirs[:] = [d for d in dirs if not d.startswith(('_', '.'))]
    for name in files:
        if not name.endswith('.md') or name in SKIP:
            continue
        src = os.path.join(root, name)
        rel = os.path.relpath(src, SITE)
        text = io.open(src, encoding='utf-8').read()
        text = re.sub(r'\A---\n.*?\n---\n\n?', '', text, flags=re.S)
        text = re.sub(r'^<!-- Status: .* -->\n\n?', '', text, flags=re.M)
        dst = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        io.open(dst, 'w', encoding='utf-8', newline='\n').write(text)
        count += 1
print('copied %d pages to %s' % (count, OUT))
