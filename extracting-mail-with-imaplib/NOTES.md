# Python3 on macOS in 2018

- use system 2.7
- use Docker
- use brew
    + requires Xcode


curl > miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

bash ./miniconda.sh

create new shell

$ conda create -n lilbub ipdb
Fetching package metadata ...........

PackageNotFoundError: Packages missing in current channels:

  - ipdb

conda create -n lilbub
source activate lilbub
conda install -c conda-forge ipdb

$ which python
/Users/johnmitchell/miniconda3/envs/lilbub/bin/python
$ python --version
Python 3.6.4

$ conda install -c conda-forge imapclient
Fetching package metadata .............
Solving package specifications: .

UnsatisfiableError: The following specifications were found to be in conflict:
  - imapclient -> mock ==1.3.0 -> funcsigs 0.4 -> python 2.6*
  - python 3.6*

$ pip install imapclient
Collecting imapclient
  Downloading IMAPClient-2.0.0-py2.py3-none-any.whl (74kB)
    100% |████████████████████████████████| 81kB 1.2MB/s
Requirement already satisfied: six in /Users/johnmitchell/miniconda3/envs/lilbub/lib/python3.6/site-packages (from imapclient)
Installing collected packages: imapclient
Successfully installed imapclient-2.0.0

