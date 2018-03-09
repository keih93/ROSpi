"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
   
    name='RaspberryPiROS-Car',  # Required
    version='0.1',  # Required
    description='Autonomous Driving with Roboclaw',  # Required
    long_description='',  # Optional
    url='https://github.com/benasdfasdf/RosPi',
    author='Theurer L., Meier M., Büscher B.',
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['Adafruit-GPIO==1.0.3',
                      'Adafruit-PCA9685==1.0.1',
                      'Adafruit-PureIO==0.2.1',
                      'pkg-resources==0.0.0',
                      'pyserial==3.4',
                      'RPi.GPIO==0.6.3',
                      'smbus2==0.2.0',
                      'spidev==3.2'
                      ],
)