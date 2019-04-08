#!/bin/sh

echo 'Removing setup files in main directory'
cd ..
sudo rm -rf build/
sudo rm -rf dist/
sudo rm -rf pyinflect.egg-info/
rm -f setup.pyc 


