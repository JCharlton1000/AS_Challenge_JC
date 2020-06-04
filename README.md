# AS_Challenge_JC
CoAP based Client and Server demo in python using protobuf messages

#Notes



#Installation
Please use Python 3.6


1.  Please create a virtual environment first:

    Install with:       $  apt-get install python3-venv
    Create virtual environment with: $ python3 -m venv env
    Activate virtual environment:  $ source env/bin/activate

2.  Install required packages:
    $ pip3 install 0r requirements.txt

3.  Apply Patch ( this is a temporary work around and will be removed):

    $ patch -u env/lib/python3.6/site-packages/coapthon/serializer.py -i serialzer.patch 