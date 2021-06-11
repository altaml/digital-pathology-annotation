# Digital Pathology project

## Data processing module
This module has a converter script that takes a folder with svs images and converts it into specified format.
### Usage
#### Docker
To run tests
```
docker build -t dpatho
docker run -i -t dpatho
```
#### Local
To install locally in conda enviornments
```
pip install -r requirements.txt
conda install pixman=0.36.0
python data_processing/convert.py --path <SOURCE_FOLDER> --format .png --output_dir <DESTINATION_FOLDER>
```