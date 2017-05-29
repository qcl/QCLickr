#!/bin/bash

PYDISTUTILS_FILENAME='.pydistutils.cfg'
PYDISTUTILS_BACKUP_FILENAME='.pydistutils.cfg.qclickr.backup'
WORKAROUND_FILENAME='pydistutils.cfg'
REQUIRED_PACKAGE_LIST_FILENAME='requirements.txt'
INSTALL_TARGET_DIRNAME='lib'

if [ -f "$HOME/$PYDISTUTILS_FILENAME" ]
then
    echo "$HOME/$PYDISTUTILS_FILENAME found, create a backup."
    mv $HOME/$PYDISTUTILS_FILENAME $HOME/$PYDISTUTILS_BACKUP_FILENAME
else
    echo "$HOME/$PYDISTUTILS_FILENAME not found."
fi

echo "copy workaround setting for using homebrew python and pip"
cp ./$WORKAROUND_FILENAME $HOME/$PYDISTUTILS_FILENAME
echo "install required python packages"
pip install -r ./$REQUIRED_PACKAGE_LIST_FILENAME -t ./$INSTALL_TARGET_DIRNAME

if [ -f "$HOME/$PYDISTUTILS_BACKUP_FILENAME" ]
then
    echo "restore original $PYDISTUTILS_FILENAME"
    mv $HOME/$PYDISTUTILS_BACKUP_FILENAME $HOME/$PYDISTUTILS_FILENAME
else
    echo "remove $HOME/$PYDISTUTILS_FILENAME"
    rm $HOME/$PYDISTUTILS_FILENAME
fi

