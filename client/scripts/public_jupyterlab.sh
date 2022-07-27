#!/bin/bash
# NOTE: Need to install jupyterlab and add public key to the server
tmux kill-session -t tunnel
tmux kill-session -t jupyter
tmux new-session -d -s tunnel "ssh -R 8888:localhost:8888 -o ExitOnForwardFailure=yes root@lab.medicar.marcorentap.com"
tmux new-session -d -s jupyter "jupyter lab --no-browser --ip 0.0.0.0 --port 8888 --collaborative --notebook-dir='~'"
