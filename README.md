This repository contains some utilities written in Python, specifically:
- `batch-download.py` downloads a list of files reading them from a text file. It works with URLs, but can also be used with filenames from any MediaWiki-based website: in this case list can be retrieved using Pywikibot's [`listpages`](https://www.mediawiki.org/wiki/Manual:Pywikibot/listpages.py) with `-format:3` to format it properly and `-cat:"<category name>"`, `-imagesused:"<page title>"` or any other generator/filter.
- `count-days.py` can add/subtract days to a date or compute the difference in days between two dates.
- `fix-wsl.py` edits two files in Pywikibot repository to make it work with Windows Subsystem for Linux.
- `rename-pairs.py` renames all files in given directory reading replacements from a text file.
- `rename-photos.py` renames all photos in given directory basing on taken timestamp.
