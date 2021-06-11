import cv2
import argparse
import sys
from pathlib import Path
import logging
from svs_utils import read_svs

logger = logging.getLogger()
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='Convert svs to specifed format')
parser.add_argument(
    '--path', metavar='src', type=str, help='the path of svs image folder'
)
parser.add_argument('--format', metavar='to', type=str, help='format to convert to')
parser.add_argument('--extract', dest='feature', action='store_true')
parser.add_argument(
    '--output_dir',
    metavar='dir',
    type=str,
    default='converted',
    help='destination folder',
)
args = parser.parse_args()

input_path = args.path
output_format = args.format
output_path = Path(args.output_dir)
thumbnail = not args.feature
FORMAT_LIST = ['.jpg', '.png', '.tiff']

if output_format not in FORMAT_LIST:
    err_msg = f'Invalid format {output_format}, select from {FORMAT_LIST}'
    logging.error(err_msg)
    raise IOError(err_msg)

if not Path(input_path).is_dir():
    logging.error('The path specified does not exist')
    sys.exit()

if not Path(output_path).is_dir():
    logging.info(f'Created {output_path}')
    output_path.mkdir(parents=True, exist_ok=True)


for svs_file in Path(input_path).glob('*.svs'):
    img_list, thumbnail = read_svs(svs_file, thumbnail_only=thumbnail)
    # Save thumbnail
    thumbnail = _run_histogram_equalization(thumbnail)

    output_file = str(
        Path(output_path) / (svs_file.stem + '_thumbnail' + str(output_format))
    )
    cv2.imwrite(output_file, thumbnail)
    logging.info(f'Thumbnail saved at {output_file}.')
