#!/usr/bin/env python
import socket
import sys
import functools

from coapthon.client.helperclient import HelperClient
from protobuf.user_pb2 import Users as pbusers
from protobuf.user_pb2 import User as pbuser
from protobuf.user_pb2 import UserDetails as pbuserdetails
from protobuf.user_pb2 import UserDelete as pbdeleteuser
from protobuf.user_pb2 import UserUpdate as pbdupdateuser
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
    
    #TODO - check pb response
    def response_success(self, response):
        result = False
        if response:
            result = True
        return result

    get     = functools.partialmethod(request, 'GET')
    post    = functools.partialmethod(request, 'POST')
    put     = functools.partialmethod(request, 'PUT')
    delete  = functools.partialmethod(request, 'DELETE')
    observe = functools.partialmethod(request, 'OBSERVE')
    
class UserService:

    def __init__(self, coapclient):
        self._coap_client = coapclient
    #returns all users from the server in JSON format
    def get_users(self):
        return MessageToJson(self._coap_client.get('/users/',None,pbusers))
    
    #updates a user on the server
    def update_user(self, id, first_name = None, last_name = None, email = None, phone_number = None ):
        user = pbdupdateuser()
        if first_name : user.first_name = first_name
        if last_name : user.last_name = last_name
        if email : user.email = email
        if phone_number : user.phone_number = phone_number
        user.id = id
        return self._coap_client.response_success(self._coap_client.post('/edituser/',user))

    #deletes an existing user if that user exists
    def delete_user_by_id(self, id ):
        delete_user = pbdeleteuser()
        delete_user.id = id
        return self._coap_client.response_success(self._coap_client.post('/deleteuser/',delete_user))

    def create_user(self, first_name, last_name, email = None, phone_number = None ):
        user = pbuserdetails()
        if first_name : user.first_name = first_name
        if last_name : user.last_name = last_name
        if email : user.email = email
        if phone_number : user.phone_number = phone_number
        return self._coap_client.response_success(self._coap_client.post('/users/',user))