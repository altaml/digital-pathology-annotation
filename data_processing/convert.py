import cv2
import argparse
import sys
from pathlib import Path
import logging
from svs_utils import read_svs

logger = logging.getLogger()
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description="Convert svs to specifed format")
parser.add_argument("--path", metavar="src", type=str, help="the path of svs image folder")
parser.add_argument("--format", metavar="to", type=str, help="format to convert to")
parser.add_argument(
    "--output_dir", metavar="dir", type=str, default="converted", help="destination folder"
)
args = parser.parse_args()

input_path = args.path
output_format = args.format
output_path = Path(args.output_dir)
FORMAT_LIST = [".jpg", ".png", ".tiff"]

if output_format not in FORMAT_LIST:
    err_msg = f"Invalid format {output_format}, select from {FORMAT_LIST}"
    logging.error(err_msg)
    raise IOError(err_msg)

if not Path(input_path).is_dir():
    logging.error("The path specified does not exist")
    sys.exit()

if not Path(output_path).is_dir():
    output_path.mkdir(parents=True, exist_ok=True)

for svs_file in Path(input_path).glob("*.svs"):
    img = read_svs(svs_file)
    cv2.imwrite(str(Path(output_path) / (str(svs_file.stem) + str(output_format))), img)
