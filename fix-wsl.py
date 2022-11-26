import sys, os.path
'''
This script edits two files in Pywikibot directory to make it work with WSL; it
is idempotent, i.e. executing it multiple times is the same as executing it
once. It can be launched without arguments when executed in pywikibot directory,
or passing it pywikibot directory's path. Examples:

python fix-wsl.py /mnt/d/pywikibot
python /mnt/d/python/fix-wsl.py

Credit: https://stackoverflow.com/questions/32760041/pywikibot-how-to-handle-user-config-py-owned-by-someone-else/62986377#62986377
'''
# get paths of files
if len(sys.argv) > 1:
    file1 = os.path.join(sys.argv[1], 'pywikibot', 'config.py')
    file2 = os.path.join(sys.argv[1], 'pywikibot', 'tools', '__init__.py')
else:
    file1 = os.path.join('pywikibot', 'config.py')
    file2 = os.path.join('pywikibot', 'tools', '__init__.py')
# edit file1
with open(file1, 'r') as file:
    text = file.read()
text = text.replace('if not OSWIN32 and _fileuid not in [os.getuid(), 0]:', 'if not OSWIN32 and _fileuid not in [os.getuid(), 0] and False:')
text = text.replace('elif OSWIN32 or _filemode & 0o02 == 0:', 'elif OSWIN32 or _filemode & 0o02 == 0 or True:')
with open(file1, 'w') as file:
    file.write(text)
# edit file2
with open(file2, 'r') as file:
    text = file.read()
if not '#os.chmod(filename, mode)' in text:
    text = text.replace('os.chmod(filename, mode)', '#os.chmod(filename, mode)')
    with open(file2, 'w') as file:
        file.write(text)
