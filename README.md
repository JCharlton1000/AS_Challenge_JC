# AS_Challenge_JC
CoAP based Client and Server demo in python using protobuf messages

## Notes


## Protobuf 

For an explanation of protobuf please see:
https://developers.google.com/protocol-buffers


in order to define new messages you must compile the protobuf complier and generate new *_pb2.py files.

This youtube video shows the instructions on acheiving this
https://www.youtube.com/watch?v=EAFK-tN_yaw

## CoAP

I have chosen to use CoAP (Constrained application protocol) as it is VERY light and designed for resource constrained devices (you can run it on embedded devices). 
CoAP meets the requirements for the challenge as it runs over UDP and uses a REST model. CoAP also feels VERY similar to HTTP.

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

## Usage

First run *coapserver.py*. If you pass no arguments to specify an IP and PORT then it will assume localhost (127.0.0.1) on PORT 5683. You should see the following output on the command line:   

CoAP Server start on 127.0.0.1:5683  
['/', '/deleteuser', '/users']

Run demo.py to see demonstation of adding, deleting and editing users on the server from the client.  
coapclient_cli.py can be used to send specific requests through the command line to the server 
example:  
    $ python3 coapclient_cli.py -o GET -p 'coap://127.0.0.1:5683/users/'

### delete user
POST to /deleteuser/ where the payload contains a *UserDelete* protobuf message containg the ID of the user to delete
 
### Edit a user
POST to /edituser/ where the payload contains a *UserUpdate* protobuf message containing the ID of the user to update along with any new fields

### Add a new user
POST to /users/ where the payload contains a *user* protobuf message

### Get all users
GET to /users/  where the server returns a *users* protobuf message which is a list of all the users


## known issues

1. The server responds with an INTERNAL_SERVER_ERROR response to any POST 
