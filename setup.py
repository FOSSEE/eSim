# Always prefer setuptools over distutils
from setuptools import setup, find_namespace_packages

'''
Created for packaging and distributing of python projects
Makes it easier to get an overview of the project and dependencies
Also needed for `Read the docs` installation and creating autodocs
Needed to define the module structure, look up `Modules` for python
'''
setup(
    name='eSim',
    version='2.2.0',
    author='FOSSEE',
    author_email='contact-esim@fossee.in',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    license='GNU GPL LICENSE',
    description='Useful circuit simulation library',
    long_description=open('README.md').read(),
)
