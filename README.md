# AS_Challenge_JC
CoAP based Client and Server demo in python using protobuf messages

## Notes


## Protobuf 
in order to define new messages you must compile the protobuf complier and generate new *_pb2.py files
This youtube video shows the instructions on acheiving this
https://www.youtube.com/watch?v=EAFK-tN_yaw


## Installation
Please use Python 3.6


1.  Please create a virtual environment first:
    Install with:       $  apt-get install python3-venv
    Create virtual environment with: $ python3 -m venv env
    Activate virtual environment:  $ source env/bin/activate

2.  Install required packages:
    $ pip3 install -r requirements.txt

3.  Apply Patch ( this is a temporary work around and will be removed):

    $ patch -u env/lib/python3.6/site-packages/coapthon/serializer.py -i serialzer.patch 



## known issues

1. The server responds with an INTERNAL_SERVER_ERROR response to any POST 
2. The message type sent to deleteuser/ should bechanged to a different protobuf message that just contains the ID