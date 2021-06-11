from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    reqs = f.read()

setup(
    name='digital-pathology-annotation',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs.strip().split('\n'),
    author='AltalML',
    description='package_description',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/altaml/digital-pathology-annotation',
    classifiers=['Programming Language :: Python :: 3.6'],
    test_suite='pytest',
)
