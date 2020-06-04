import time
from coapthon import defines

from coapthon.resources.resource import Resource
from protobuf.user_pb2 import Users as pbusers
from protobuf.user_pb2 import User as pbuser



class Users(Resource):
    def __init__(self, users, name="UsersResource", coap_server=None):
        super(Users, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = ''
        #self.resource_type = "rt1"
        self.content_type = 65000
        self.users = users
        #self.interface_type = "if1"

    def render_GET(self, request):
        self.payload = self.users.SerializeToString()
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    # TODO: extra checking needed
    def render_POST(self, request):
        new_user = self.users.people.add()
        new_user.MergeFromString(bytes(request.payload, 'utf-8'))
        #assign a new ID
        new_user.id = len(self.users.people)
        #self._coap_server.add_resource(self.path +"/"+ str(new_user.id), Users())
        return True

    def render_DELETE(self, request):
        return True

class DeleteUser(Resource):
    def __init__(self, users, name="DeleteUserResource", coap_server=None):
        super(DeleteUser, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = ''
        self.content_type = 65000
        self.users = users
        self.deleted_users = pbusers()

    def render_GET(self, request):
        self.payload = self.deleted_users.SerializeToString()
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    # TODO: extra checking needed
    def render_POST(self, request):
        user_to_remove = pbuser()
        new_user = self.users.people.add()
        new_user.MergeFromString(bytes(request.payload, 'utf-8'))
        #assign a new ID
        new_user.id = len(self.users.people)
        return True

    def render_DELETE(self, request):
        return True