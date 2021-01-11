from setuptools import setup, find_packages
from io import open

console_scripts = []

console_scripts.append('test1={}.tests:test1'.format(find_packages('src')[0]))
console_scripts.append('test2={}.tests:test2'.format(find_packages('src')[0]))

setup(entry_points={'console_scripts': console_scripts},
      packages=find_packages(where='src'),
      package_dir={'': 'src'})