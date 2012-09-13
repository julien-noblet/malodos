#!/bin/sh

V=$1
7z a '-xr!*svn*' '-xr!*branches*' '-xr!*build*' '-xr!*dist*' '-xr!*pyc' '-xr!*~' '-xr!.*' malodos-$V.7z trunk
zip -r malodos-$V.zip trunk -x \*branches\* \*.svn\* \*.pyc\* \*build\* \*dist\* \*~ trunk\/.\*
