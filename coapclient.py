#!/usr/bin/env python
import socket
import sys
import functools

from coapthon.client.helperclient import HelperClient
from protobuf.user_pb2 import Users as pbusers
from protobuf.user_pb2 import User as pbuser
from google.protobuf.json_format import MessageToJson


class CoapClient:


    def __init__(self, server_url = '127.0.0.1', server_port = 5683):
        try:
            tmp = socket.gethostbyname(server_url)
            server_url = tmp
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
    
    #returns all users from the server in JSON format
    def get_users(self):
        return MessageToJson(self.get('/users/',None,pbusers))
    
    #creates a new user on the server if no existing ID is given, else updates a user if ID matches existsing
    def create_update_user(self, first_name, last_name, email = "", phone_number="", id = None):
        user = pbuser()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        if id:
            user.id = id
        return self.post('/users/',user)

    #deletes an existing user if that user exists
    def delete_user(self, id ):
        user = pbuser()
        user.first_name =""
        user.last_name = ""
        user.id = id
        return self.post('/deleteuser/',user)
    
    get     = functools.partialmethod(request, 'GET')
    post    = functools.partialmethod(request, 'POST')
    put     = functools.partialmethod(request, 'PUT')
    delete  = functools.partialmethod(request, 'DELETE')
    observe = functools.partialmethod(request, 'OBSERVE')
