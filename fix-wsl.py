'''
This script edits two files in Pywikibot directory to make it work with WSL. No
argument is required, it just needs to be launched in Pywikibot directory.
Source (with little changes because Pywikibot has changed since then):
https://stackoverflow.com/questions/32760041/pywikibot-how-to-handle-user-config-py-owned-by-someone-else/62986377#62986377
'''
file1 = 'pywikibot/config.py'
with open(file1, 'r') as file:
    text = file.read()
text = text.replace('if not OSWIN32 and _fileuid not in [os.getuid(), 0]:', 'if not OSWIN32 and _fileuid not in [os.getuid(), 0] and False:')
text = text.replace('elif OSWIN32 or _filemode & 0o02 == 0:', 'elif OSWIN32 or _filemode & 0o02 == 0 or True:')
with open(file1, 'w') as file:
    file.write(text)

file2 = 'pywikibot/tools/__init__.py'
with open(file2, 'r') as file:
    text = file.read()
if not '#os.chmod(filename, mode)' in text:
    text = text.replace('os.chmod(filename, mode)', '#os.chmod(filename, mode)')
    with open(file2, 'w') as file:
        file.write(text)
