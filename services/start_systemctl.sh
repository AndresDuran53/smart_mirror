#!/bin/bash

sudo systemctl stop checkTv.service
sudo systemctl stop tempChecker.service

sudo systemctl disable checkTv.service
sudo systemctl disable tempChecker.service

sudo cp checkTv.service /etc/systemd/system/
sudo cp tempChecker.service /etc/systemd/system/

sudo systemctl enable checkTv.service
sudo systemctl enable tempChecker.service

sudo systemctl enable checkTv.service
sudo systemctl enable tempChecker.service
