#from distutils.core import setup
from setuptools import setup , find_packages , findall
from os import listdir
from os.path import splitext

txt_files = listdir('.')
txt_files = [ i for i in txt_files if splitext(i)[1] == '.txt' ]
setup(
    url='http://sites.google.com/site/malodospage/',
    license='GPL v3',
    install_requires=['PIL','wxpython','pyenchant'],
    name='MALODOS',
    description='Personal EDM (Scan, describe and manage your personal documents)',
    version='1.2.2',
    author='David GUEZ',
    author_email='guezdav@gmail.com',
    packages=['src/algorithms','src/database','src/data','src/gui','src/scannerAccess'],
    scripts = ['src/homeDocs.py'],
    classifiers=['Topic :: Office/Business','Operating System :: Microsoft :: Windows','Operating System :: POSIX','Programming Language :: Python','Development Status :: 5 - Production/Stable','Intended Audience :: End Users/Desktop','License :: OSI Approved :: GNU Affero General Public License v3'],
    data_files = [ ('',txt_files) , ('resources',findall('resources')),('src/locale',findall('src/locale')) ]
)
