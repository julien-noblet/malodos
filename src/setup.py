from distutils.core import setup
import py2exe
from glob import glob
import sys
sys.path.append("H:\\homeDoc\\src\\dist\\Microsoft.VC90.CRT")
data_files = [("Microsoft.VC90.CRT", glob(r'H:\homeDoc\src\dist\Microsoft.VC90.CRT\*.*'))]
setup(
    data_files=data_files,
    console=['homeDocs.py']
)
