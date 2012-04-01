# ...
# ModuleFinder can't handle runtime changes to __path__, but win32com uses them
try:
    # py2exe 0.6.4 introduced a replacement modulefinder.
    # This means we have to add package paths there, not to the built-in
    # one.  If this new modulefinder gets integrated into Python, then
    # we might be able to revert this some day.
    # if this doesn't work, try import modulefinder
    try:
        import py2exe.mf as modulefinder
    except ImportError:
        import modulefinder
    import win32com, sys
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    for extra in ["win32com.shell"]: #,"win32com.mapi"
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    # no build path setup, no worries.
    pass

from distutils.core import setup
import py2exe
from glob import glob
import sys
sys.path.append("H:\\homeDoc\\src\\dist\\Microsoft.VC90.CRT")
data_files = [("Microsoft.VC90.CRT", glob(r'H:\homeDoc\src\dist\Microsoft.VC90.CRT\*.*'))]
setup(
    url='http://sites.google.com/site/malodospage/',
    license='GPL v3',
    install_requires=['PIL','wxpython','pyenchant'],
    name='MALODOS',
    description='Personal EDM (Scan, describe and manage your personal documents)',
    version='1.2.2',
    author='David GUEZ',
    author_email='guezdav@gmail.com',
    packages=['algorithms','database','data','gui','scannerAccess'],
    classifiers=['Topic :: Office/Business','Operating System :: Microsoft :: Windows','Operating System :: POSIX','Programming Language :: Python','Development Status :: 5 - Production/Stable','Intended Audience :: End Users/Desktop','License :: OSI Approved :: GNU Affero General Public License v3'],
    data_files=data_files,
    windows=['homeDocs.py']
)
