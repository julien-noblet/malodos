#!/bin/sh

if [ $# -lt 1 ]
then
    lng=fr_FR
else
    lng=$1
fi
echo Creating messages for language $lng
xgettext $(find . -name '*.py' -and -not -name TextCtrlAutoComplete.py -and -not -path '*font*' -and -not -name '*fpdf*') -j -o locale/$lng/LC_MESSAGES/malodos.po
poedit locale/$lng/LC_MESSAGES/malodos.po