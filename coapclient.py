#!/usr/bin/env python
import getopt
import socket
import sys
import functools

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from protobuf.user_pb2 import Users as pbusers
from protobuf.user_pb2 import User as pbuser
from google.protobuf.json_format import MessageToJson


class CoapClient:


    def __init__(self, server_url = '127.0.0.1', server_port = 5683):
        try:
            tmp = socket.gethostbyname(server_url)
            host = tmp
        except socket.gaierror:
            pass
        self._client = HelperClient(server=(server_url, server_port))

    def request(self, method, url, payload = None, resp = None):
        #check if payload given 
        if payload  : payload = payload.SerializeToString()
        else        : payload = b''

        try:
            if method == "GET":
                response = self._client.get(url)
            elif method == "POST":
                response = self._client.post(url, payload)
            elif method == "PUT":
                response = self._client.put(url, payload)
            elif method == "DELETE":
                response = self._client.delete(url)
            #elif op == "OBSERVE":
                #client.observe(path, client_callback_observe)
            else:
                raise AssertionError('Unsupported method of kind : ' + str(method))
        except Exception as e:
            raise AssertionError(e)# TODO add logging
        
        if resp: # did we give an expect response 
            if response.payload: #did we get a response payload
                return resp().FromString(bytes(response.payload, 'utf-8')) # parse the payload into its protobuf representation
        return response
    
    def stop(self):
        self._client.stop()
    
    get     = functools.partialmethod(request, 'GET')
    post    = functools.partialmethod(request, 'POST')
    put     = functools.partialmethod(request, 'PUT')
    delete  = functools.partialmethod(request, 'DELETE')
    observe = functools.partialmethod(request, 'OBSERVE')

def create_user(first_name, last_name, email = "", phone_number="", id = None):
    new_user = pbuser()
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.email = email
    new_user.phone_number = phone_number
    if id:
        new_user.id = id
    return new_user

def get_user_to_delete( id = None):
    new_user = pbuser()
    new_user.first_name =""
    new_user.last_name = ""
    if id:
        new_user.id = id
    return new_user

client = CoapClient()
new_user = create_user("James2", "charlton2", "newemail@test.com", "201234567")
user_to_delete = get_user_to_delete("43bbbfd1-545e-4006-95c0-3b4961e31ec0")
r= client.post('/users/',new_user)
r = client.get('/users/',None,pbusers)
print(MessageToJson(r))
r = client.post('/deleteuser/',user_to_delete)
r = client.get('/users/',None,pbusers)
print(MessageToJson(r))
test = 10

client.stop()