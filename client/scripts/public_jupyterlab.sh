#!/bin/bash
# NOTE: Need to install autossh, jupyterlab and add public key to the server
tmux new-session -d -s tunnel "autossh -R 8888:localhost:8888 root@lab.medicar.marcorentap.com"
tmux new-session -d -s jupyter "jupyter lab --no-browser --ip 0.0.0.0 --port 8888 --collaborative --notebook-dir='~'"
