from pathlib import Path

from setuptools import setup

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='PyGorse',
      version='0.4.3',
      description='Python SDK for gorse recommender system',
      packages=['gorse'],
      install_requires=['requests>=2.14.0'],
      long_description=long_description,
      long_description_content_type='text/markdown'
      )
