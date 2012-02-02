#!/bin/sh

if [ $# -lt 1 ]
then
    lng=fr_FR
else
    lng=$1
fi
echo Compiling messages for language $lng
msgfmt -o locale/$lng/LC_MESSAGES/malodos.mo locale/$lng/LC_MESSAGES/malodos.po
