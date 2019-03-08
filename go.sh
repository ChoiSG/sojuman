#!/bin/bash

# go
wget https://github.com/ChoiSG/sojuman/raw/master/sojuman
apt-get install -y python-pip3
pip3 install pyAesCrypt
chmod +x sojuman
./sojuman
