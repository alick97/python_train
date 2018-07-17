#!/bin/bash

WORKSPACE=$PWD

if [ ! -d "${WORKSPACE}/venv" ];then
   virtualenv -p /usr/bin/python3 --no-site-package venv
fi
. venv/bin/activate
# exit virtual environment run cmd 
## deactivate
