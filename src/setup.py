__author__ = "ilausuch"
__date__ = "$12-jun-2017 20:22:40$"

from setuptools import setup, find_packages

setup (
       name='CacheServer',
       version='1.0',
       packages=find_packages(),

       # Declare your packages' dependencies here, for eg:
       install_requires=['pyev>0.9','flask>0.12.2'],

       # Fill in these to make your Egg ready for upload to
       # PyPI
       author='Ivan Lausuch',
       author_email='ilausuch@gmail.com',

       summary='Cache server with multiple banks of cache',
       url='',
       license='MIT',
       long_description='Long description of the package',

       # could also include long_description, download_url, classifiers, etc.

  
       )