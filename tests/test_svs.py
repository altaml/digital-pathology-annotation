from data_processing.svs_utils import read_svs
from pathlib import Path
import os
import cv2
import numpy as np


def test_svs_reader_reads():
    file_path = Path('tests') / 'sample_data' / 'small.svs'
    _, img = read_svs(file_path)
    assert len(img.shape) == 3
    assert img.shape == (16, 16, 3)


def test_conversion_script_jpg():
    os.system(
        'python data_processing/convert.py --path tests/sample_data --format .jpg --output_dir converted'
    )
    image_file = Path('converted') / 'small_thumbnail.jpg'
    assert image_file.is_file()
    read_back = cv2.imread(str(image_file))
    assert read_back.shape == (16, 16, 3)
    h, w, c = read_back.shape
    black_pixel_percent = np.sum(np.int32(read_back == 0)) / (h * w * c)
    assert black_pixel_percent < 0.2
    image_file.unlink()
    Path('converted').rmdir()


def test_conversion_script_png():
    os.system(
        'python data_processing/convert.py --path tests/sample_data --format .png --output_dir converted'
    )
    image_file = Path('converted') / 'small_thumbnail.png'
    assert image_file.is_file()
    read_back = cv2.imread(str(image_file))
    assert read_back.shape == (16, 16, 3)
    h, w, c = read_back.shape
    black_pixel_percent = np.sum(np.int32(read_back == 0)) / (h * w * c)
    assert black_pixel_percent < 0.2
    image_file.unlink()
    Path('converted').rmdir()


def test_high_rez():
    if (Path('tests') / 'high_rez').is_dir():
        os.system(
            'python data_processing/convert.py --path tests/high_rez --format .png --output_dir converted --extract'
        )
        output_path = Path('converted')
        image_files_list = list(output_path.glob('*.png'))
        assert len(image_files_list) == 3
        img_list = [str(x) for x in Path('converted').glob('*.png')]
        assert ['_thumbnail,png' in x for x in img_list]
        assert ['1,png' in x for x in img_list]
        assert ['0,png' in x for x in img_list]
