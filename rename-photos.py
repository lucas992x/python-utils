import argparse, os, sys
from datetime import datetime
from pillow_heif import register_heif_opener
from PIL import Image

"""
This script renames all photos in given directory using the timestamp at which they
were taken; it is based on https://gist.github.com/JohnBra/77159d4070e60c46fc8dbbfef42467a9
with some improvements.

Arguments:
--dir: directory where photos are located,
--format: naming format to use (default "%Y%m%d_%H%M%S", see
https://docs.python.org/3/library/datetime.html#format-codes for further info).
--prefix: prefix to add to all photos when renaming them (optional).
--suffix: suffix to add to all photos when renaming them (optional).
--test: "no" to rename files, otherwise they are not modified.
"""


# get timestamp at which a photo was taken, returns a datetime variable
def get_photo_timestamp_taken(file_path, timestamp_format):
    # check file extension
    file_ext = os.path.splitext(file_path)[1].lower()
    valid_extensions = [".png", ".jpg", ".jpeg", ".heic"]
    if file_ext not in valid_extensions:
        print(f"Unsupported extension for file {file_path}")
        return None
    # open image
    register_heif_opener()
    image = Image.open(file_path)
    # check extension and use appropriate tool to extract metadata
    if file_ext == ".heic":
        metadata = image.getexif()
    else:
        metadata = image._getexif()
    image.close()
    # check if metadata was extracted successfully
    if metadata is None:
        print(f"EXIF metadata not found in file {file_path}")
        return None
    # check if date is present in extracted metadata
    if 36867 in metadata.keys():
        date_taken = metadata[36867]
    elif 306 in metadata.keys():
        date_taken = metadata[306]
    else:
        print(f"Date not found in file {file_path}")
        return None
    # get datetime at which image was taken
    date_taken = datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
    # convert datetime to string with desired format
    timestamp_string = date_taken.strftime(timestamp_format)
    return timestamp_string, file_ext


# main function
def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="")
    parser.add_argument("--format", default="%Y%m%d_%H%M%S")
    parser.add_argument("--prefix", default="")
    parser.add_argument("--suffix", default="")
    parser.add_argument("--test", default="yes")
    args = parser.parse_args()
    # check that specified directory exists
    if not args.dir:
        args.dir = os.getcwd()
    elif not os.path.isdir(args.dir):
        sys.exit(f"Directory not found: {args.dir}")
    # get all files in folder
    dir_files = sorted([i for i in os.listdir(args.dir) if os.path.isfile(i)])
    for file_name in dir_files:
        # try to extract data from file
        file_path = os.path.join(args.dir, file_name)
        photo_data = get_photo_timestamp_taken(file_path, args.format)
        # if data was extracted, process file
        if photo_data:
            timestamp_taken, file_ext = photo_data
            new_name = f"{args.prefix}{timestamp_taken}{args.suffix}{file_ext}"
            print(f'"{file_name}"      >      "{new_name}"')
            # only rename files if specified by argument
            if args.test == "no":
                os.rename(file_path, os.path.join(args.dir, new_name))


# invoke main function
if __name__ == "__main__":
    main()
