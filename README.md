# oauth-emu
This project is designed to emulate OAuth 2.0 and to a large extent the cloud view engine:

    - OAuth 2.0 flow simulation 
    - Cloud View Engine, emulates interactions with a cloud service provider
# Installation
Make sure you have python installed & git:

    - make a folder that houses code and virtual environment: mkdir oauth-emu
    - get the source code : git clone https://github.com/lnyemba/oauth-emu.git oauth-emu/src
    - create virtual environment: virtualenv oauth-emu/sandbox
    - enable the virtual environment : source oauth-emu/sandbox/bin/activate
    - install dependencies : sh oauth-emu/src/required.sh
# Execution
From the command line, the application will run on port 8080 and can optionally be placed behind an http-proxy :

    - activate virtual environment is active (if need be) : source oauth-emu/sandbox/bin/activate
    - set root tree : export PYTHONPATH=oauth-emu/src
    - run the application : python oauth-emu/src/index.py [/http-proxy-context]

**TODO**
We have to make sure the port number is configurable

The cloud View Engine powers 3-launchpad media player mobile (android) and desktop (javafx)
