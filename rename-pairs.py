import argparse, sys, os, os.path, re, copy
'''
This script renames all files in a directory reading replacements from a text
file, where each line should contain string to search and string to replace
separated by comma (or specified character). Arguments:
--dir: directory where files to be renamed are located.
--pairsfile: path of file that contains search-replace couples.
--sep: character that separates string to search and string to replace (default comma).
--swap: 'yes' if file contains replace-search instead of search-replace.
--word: 'yes' if each search should match whole words only; 'left' if it should
match the start of a word; 'right' if it should match the end of a word.

Example:
python rename-pairs.py --dir ~/downloads --pairsfile rename-pairs-sample.txt --word yes
'''

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--dir', default = '')
parser.add_argument('--pairsfile', default = '')
parser.add_argument('--sep', default = ',')
parser.add_argument('--swap', default = 'no')
parser.add_argument('--word', default = 'no')
args = parser.parse_args()
# check inputs
if not args.dir:
    sys.exit('Error: specify directory!')
elif not os.path.isdir(args.dir):
    sys.exit('Error: directory "{}" not found!'.format(args.dir))
elif not os.path.isfile(args.pairsfile):
    sys.exit('Error: file "{}" not found!'.format(args.pairsfile))
else:
    # read search-replace pairs from text file
    pairs = []
    with open(args.pairsfile, 'r') as file:
        for line in file:
            items = line.strip().split(args.sep)
            if args.swap == 'yes':
                pairs.append([items[1], items[0]])
            else:
                pairs.append([items[0], items[1]])
    # get files in directory and rename them
    filenames = os.listdir(args.dir)
    for filename in filenames:
        newfilename = copy.deepcopy(filename)
        filepath = os.path.join(args.dir, filename)
        if os.path.isfile(filepath):
            for pair in pairs:
                regex = pair[0]
                # escape special characters
                regex = regex.replace('-', '\\-').replace('.', '\\.')
                # match words if necessary
                if args.word == 'yes':
                    regex = r'\b{}\b'.format(regex)
                elif args.word == 'left':
                    regex = r'\b{}'.format(regex)
                elif args.word == 'right':
                    regex = r'{}\b'.format(regex)
                newfilename = re.sub(regex, pair[1], newfilename)
            # rename file
            if newfilename != filename:
                os.rename(filepath, os.path.join(args.dir, newfilename))
