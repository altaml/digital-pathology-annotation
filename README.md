# Digital Pathology project

## Data processing module
This module has a converter script that takes a folder with svs images and converts it into specified format.
Depending on the arguments (if `--extract` is set) to the script, the script would generate one thumbnail file that has a snapshot of the entire slide. It also generates a series of files of tissues at maximum resolution.
### Usage
#### Docker
To run tests.
```
docker build -t dpatho
docker run -i -t dpatho
```
The last test would run only if there is the svs file at 40x stored in the folder `tests/high_rez`. Download svs file from NAS and put it here (`mkdir tests/high_rez` if needed) to make it work.
#### Local
To install locally in conda enviornments
```
pip install -r requirements.txt
conda install pixman=0.36.0
python data_processing/convert.py --path <SOURCE_FOLDER> --format .png --output_dir <DESTINATION_FOLDER> --extract
```