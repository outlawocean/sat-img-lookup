import argparse
import os
from populate_spreadsheet import main

parser = argparse.ArgumentParser()
parser.add_argument("spreadsheet", help="Path to the spreadsheet file.")
parser.add_argument("--images", "-i", action="store_true", default=False, help="Additionally download images and save to folder.")
parser.add_argument("--folder", "-f", default="./download/", help="The folder when the downloaded images will go if saving. Default is ./download/")
parser.add_argument("--output", "-o", default="<timestamp>", help="The name for the output file. Default is current_file_name_<timestamp>.ext")
parser.add_argument("--zoom", "-z", default="16.5", help="The zoom level for the images. Default is 16.5.")
parser.add_argument("--marker", "-m", action="store_true", default=False, help="Add a marker to the image at the coordinates.")

args = parser.parse_args()

options = {}
options['spreadsheet_file_name'] = os.path.abspath(args.spreadsheet)
options['save_images'] = args.images
options['download_folder'] = args.folder
options['output'] = args.output
options['zoom'] = args.zoom
options['marker'] = args.marker

if __name__ == "__main__":
    main(options)
