from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='flightdelay',
      version="1.0",
      description="project of predicting a flight delay in the US",
      packages=find_packages(),
      install_requires=requirements)
