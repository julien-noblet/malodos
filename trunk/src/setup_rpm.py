from distutils.core import setup
setup(
    url='http://sites.google.com/site/malodospage/',
    licence='GPL v3',
    name='MALODOS',
    description='Personal EDM (Scan, describe and manage your personal documents)',
    version='1.2.2',
    author='David GUEZ',
    author_email='guezdav@gmail.com',
    data_files=['resources','locale'],
    packages=['algorithms','data','database','gui','scannerAccess'],
    py_module=['homeDocs','Resources']
)
