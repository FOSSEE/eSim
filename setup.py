from setuptools import setup, find_namespace_packages, Command  # Always prefer setuptools over distutils

'''
Created for packaging and distributing of python projects
Makes it easier to get an overview of the project and dependencies
Also needed for `Read the docs` iinstallation and creating autodocs
Needed to define the module structure, look up `Modules` for python
'''
setup(
    name='eSim',
    version='1.1.3',
    author='Fossee',
    author_email='info@fossee.in',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    license='LICENSE',
    description='Useful circuit simulation library',
    long_description=open('README.md').read(),
)