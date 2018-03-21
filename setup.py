import sys

from setuptools import setup, find_packages

sys.path.append('./test')

setup(name='medusa',
      version='0.0.1',
      description='Medusa Brain',
      url='https://github.com/prokosna/medusa',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'medusa = src.medusa:main'
          ]
      })
