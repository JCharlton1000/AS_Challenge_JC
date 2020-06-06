import time
from coapthon import defines

from coapthon.resources.resource import Resource




class Users(Resource):
    def __init__(self, users, name="UsersResource", coap_server=None):
        super(Users, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = ''
        #self.resource_type = "rt1"
        self.content_type = 65000
        self.user_storage = users
        #self.interface_type = "if1"

    def render_GET(self, request):
        self.payload = self.user_storage.get_users()
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    # TODO: extra checking needed
    def render_POST(self, request):
        self.user_storage.add_user(request.payload)
        return True

    def render_DELETE(self, request):
        return True

class DeleteUser(Resource):
    def __init__(self, users, name="DeleteUserResource", coap_server=None):
        super(DeleteUser, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = ''
        self.content_type = 65000
        self.user_storage = users
        from protobuf.user_pb2 import Users as pbusers
        self.deleted_users = pbusers()

    def render_GET(self, request):
        self.payload = self.deleted_users.SerializeToString()
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    # TODO: extra checking needed
    def render_POST(self, request):
        self.user_storage.remove_user(request.payload)
        return True

    def render_DELETE(self, request):
        return True


class EditUser(Resource):
    def __init__(self, users, name="EditUserResource", coap_server=None):
        super(EditUser, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = ''
        self.content_type = 65000
        self.user_storage = users

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    # TODO: extra checking needed
    def render_POST(self, request):
        self.user_storage.edit_user(request.payload)
        return True

    def render_DELETE(self, request):
        return True