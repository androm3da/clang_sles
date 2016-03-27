#!/bin/bash -ex

sudo zypper install -y gcc47-c++ libxml2-devel ncurses-devel

vt=$(mktemp)
sed -e 's/unsigned int new/unsigned int new__/g' /usr/include/linux/vt.h ${vt}
sudo mv ${vt} /usr/include/linux/vt.h
