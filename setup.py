from setuptools import setup, find_packages
from typing import List
NAME= "housing_predictor"
VERSION="0.0.1"
AUTHOR = "Sherin Thomas"
DESC = "This project is to predict housing prices in the US"
PACKAGES = ['housing']
REQ_FILE_NAME = "requirements.txt"

def get_required_list()->List[str]:
    """
    This function return a list of all the packages that need to be installed for the project to run
    """
    with open(REQ_FILE_NAME) as file:
        return file.readlines()

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESC,
    packages=find_packages(),
    install_requires = get_required_list()

)



