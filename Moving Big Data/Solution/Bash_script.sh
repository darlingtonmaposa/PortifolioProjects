#!/bin/bash
sudo s3fs de-mbd-predict-daniel-opanubi-s3-source /home/ec2-user/s3-drive -o passwd_file=$HOME/.passwd-s3fs,nonempty,rw,allow_other,mp_umask=002,uid=1000,gid=1000 -o url=http://s3.eu-west-1.amazonaws.com,endpoint=eu-west-1,use_path_request_style
python3 /home/ec2-user/s3-drive/Scripts/Python_script.py