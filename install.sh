#!/bin/bash

sudo apt update
sudo apt install python3-pip -y
sudo pip3 install pipenv
pipenv install # Assumes you are cd'd into AES-Encryption/ (This might take a moment)
pipenv shell # Exit virtual env with 'exit'