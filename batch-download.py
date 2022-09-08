import argparse, os, os.path, sys, hashlib, urllib.parse, wget
'''
This script downloads a list of files reading them from text file, where each
line should be structured as following:
- If line contains only an URL, file is downloaded keeping its name.
- If line contains an URL and a string separated by comma, file is downloaded
using that string as name: comma is default character but it can be changed
using --sep argument.
It is possible to use names of files from a MediaWiki-based website instead of
URLs: in that case it is necessary to provide base URL of files contained in
that wiki. To do this create a file named batch-download-wikis.txt located in
same directory of this script, where each line should contain base URL of files
and a short identifier for that wiki. Do note that base URL is referred to
actual file and not to the page that contains its preview with a description:
for example Wikimedia Commons URL is not https://commons.wikimedia.org/wiki,
but instead https://upload.wikimedia.org/wikipedia/commons.

Arguments:
--file: path (absolute or relative) of text file that lists files to download.
--sep: character that separates URL (or wiki file name) and destination file name.
--spaces: 'yes' if underscores in file name should be replaced by spaces.
--wiki: short name of wiki (see batch-download-wikis.txt for examples).
--dest: destination folder (is created automatically if it doesn't exist).
--retry: number of times a single file can be retried (default 4).
--overwrite: 'yes' if existing files should be overwritten.

Examples:
python batch-download.py --file list.txt --spaces yes --dest ~/downloads
python batch-download.py --wiki wikipedia --dest 'Banteay Srei'
'''
# download a file and return True/False if successful/failed
def download(url, destfile):
    # sometimes wget.download works better, sometimes wget from console is
    # better, so I often switch lol
    try:
        #wget.download(url, destfile)
        os.system(f'wget {url} -O "{destfile}"')
        downloaded = True
    except:
        downloaded = False
    if not os.path.isfile(destfile):
        downloaded = False
    elif os.path.getsize(destfile) == 0:
        os.unlink(destfile)
        downloaded = False
    return downloaded

# manage download and retries
def trydownload(url, destfile, maxretries = 2):
    downloaded = False
    count = 0
    while downloaded == False and count <= maxretries:
        downloaded = download(url, destfile)
        count += 1
    return downloaded

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--file', default = 'files.txt')
parser.add_argument('--sep', default = ',')
parser.add_argument('--spaces', default = 'no')
parser.add_argument('--wiki', default = '')
parser.add_argument('--dest', default = 'downloads')
parser.add_argument('--retry', default = 4, type = int)
parser.add_argument('--overwrite', default = 'no')
args = parser.parse_args()

if __name__ == '__main__':
    # check that input file exists
    if not os.path.isfile(args.file):
        sys.exit(f'Error: file "{args.file}" not found!')
    # create destination directory if not exists
    if not os.path.isdir(args.dest):
        os.mkdir(args.dest)
    # read from input file
    with open(args.file, 'r') as file:
        lines = file.read().splitlines()
    tot = len(lines)
    count = 0
    numdigits = len(str(tot)) # used to print output
    # search for text file with wiki URLs
    wikisfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'batch-download-wikis.txt')
    if os.path.isfile(wikisfile):
        getbaseurl = {}
        with open(wikisfile, 'r') as file:
            for line in file:
                url, wiki = line.strip().split(' ')
                getbaseurl.update({wiki: url})
    else:
        # default wiki list
        getbaseurl = { 'wikipedia': 'https://upload.wikimedia.org/wikipedia/commons' }
    # check that wiki is recognized if provided
    if args.wiki:
        baseurl = getbaseurl.get(args.wiki, '')
        if not baseurl:
            sys.exit(f'Error: wiki "{args.wiki}" not recognized!')
    # loop over files to download them
    for line in lines:
        count += 1
        if args.wiki:
            # get file URL and set dest file name
            if args.sep in line:
                file, destfile = line.split(args.sep)
            else:
                file = line
                destfile = line
            file = file.replace(' ', '_').replace('?', '%3F')
            md5 = hashlib.md5(file.encode()).hexdigest()
            url = '/'.join([baseurl, md5[0], md5[0:2], file])
        else:
            # set dest file name
            if args.sep in line:
                url, destfile = line.split(args.sep)
            else:
                url = line
                destfile = urllib.parse.unquote(url.split('/')[-1])
                if args.spaces == 'yes':
                    destfile = destfile.replace('_', ' ')
        # add path to dest file and output file
        destfile = os.path.join(args.dest, destfile)
        errorsfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'batch-download-errors.txt')
        # check if dest file already exists
        if os.path.isfile(destfile):
            if args.overwrite != 'yes':
                if not os.path.isfile(errorsfile):
                    mode = 'w'
                else:
                    mode = 'a'
                with open(errorsfile, mode) as file:
                    file.write(f'{url} skipped\n')
                continue
        # proceed to download
        downloaded = trydownload(url, destfile, args.retry)
        # check if download was successful or failed
        if downloaded == False:
            print(f' File {count} of {tot} failed to download')
            if not os.path.isfile(errorsfile):
                mode = 'w'
            else:
                mode = 'a'
            with open(errorsfile, mode) as file:
                file.write(f'{url} failed\n')
        else:
            print(f' File {count} of {tot} downloaded successfully')
