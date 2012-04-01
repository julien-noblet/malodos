#from distutils.core import setup
from setuptools import setup , find_packages

setup(
    url='http://sites.google.com/site/malodospage/',
    license='GPL v3',
    install_requires=['sane','PIL','wx','pyenchant'],
    name='MALODOS',
    description='Personal EDM (Scan, describe and manage your personal documents)',
    version='1.2.2',
    author='David GUEZ',
    author_email='guezdav@gmail.com',
    packages=['algorithms','database','data','gui','scannerAccess'],
    scripts = ['homeDocs.py'],
    package_data = { '..':['*.txt'] , 'locale':['*'] , '../resources':['*'] }
)
