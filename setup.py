from setuptools import setup

setup(
    name='snapmgr',
    version='0.1',
    author='Hu shao',
    author_email='menthlo@hotmail.com',
    description='snapmgr is a tool manage EC2 snapshots',
    license='GPLv3+',
    packages=['shotty'],
    url='https://github.com/menthlo/snapshotanalyzer-30000',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points={
    'console_scripts': [
        'shotty=shotty.shotty:cli',
    ],
},

)
