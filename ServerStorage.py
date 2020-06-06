from protobuf.user_pb2 import Users as pbusers
from protobuf.user_pb2 import User as pbuser
from protobuf.user_pb2 import UserDelete as pbdeleteuser
from protobuf.user_pb2 import UserUpdate as pbdupdateuser
from protobuf.user_pb2 import UserDetails as pbuserdetails
import uuid

#this class manages the storage of the users in memory - however this may NOT be thread safe and needs checking
class UserStorage():
    def __init__(self, name="" ):
        self.name = name
        self.users = pbusers()

    def get_users(self):    
        return self.users.SerializeToString()
        
    #when given a new user if an ID is given then this is used to update an existing user if exists.
    #if no ID is given then a new user is created and an ID auto generated.
    #if an ID is given but no match found then a new user is still created and a new ID given (TBD)
    def add_user(self,user):
        result = False
        user_details = pbuserdetails()
        user_details.MergeFromString(bytes(user, 'utf-8'))
        id_provided = False

        if not self.user_exists(user_details):
            #have we been given an id - if so look for it
            # if hasattr(userpb, "id"):
            #     id_provided = True
            #     exists, existing_user = self.get_user_by_id(user_details.id)
            #     if exists:
            #         # this user already exists
            #         return False
            new_user = self.users.people.add()
            new_user.UserDetails.MergeFromString(bytes(user, 'utf-8'))
            # sanitze input
            new_user.UserDetails.first_name = new_user.UserDetails.first_name.capitalize()
            new_user.UserDetails.last_name = new_user.UserDetails.last_name.capitalize()
            #assign a new ID if one wasnt given
            if not id_provided : new_user.id = str(uuid.uuid4())
            result= True
        return result
    
    #
    def remove_user(self, remove):
        result = False
        user_to_delete = pbdeleteuser()
        user_to_delete.MergeFromString(bytes(remove, 'utf-8'))
        result, user = self.get_user_by_id(user_to_delete.id)
        if result : result = self.remove_user_by_id(user.id)
        return result
    
    def edit_user(self, user):
        result = False
        userpb = pbdupdateuser()
        userpb.MergeFromString(bytes(user, 'utf-8'))

        result, existing_user = self.get_user_by_id(userpb.id)
        if result:
            if hasattr(userpb, "first_name"): existing_user.UserDetails.first_name = userpb.first_name
            if hasattr(userpb, "last_name"): existing_user.UserDetails.last_name = userpb.last_name
            if hasattr(userpb, "email"): existing_user.UserDetails.email = userpb.email
            if hasattr(userpb, "phone_number"): existing_user.UserDetails.phone_number = userpb.phone_number
        return result
    
    # this is a slow approach - this should be reconsidered
    def remove_user_by_id(self, id):
        result = False
        for index, person in enumerate(self.users.people):
            if person.id == id:
                del self.users.people[index]
                result = True
                break
        return result

    def get_user_by_id(self, id):
        success = False
        i =0
        for index, person in enumerate(self.users.people):
            if person.id == id:
                success = True
                i = index
                break
        return success, self.users.people[i] if success else None
    
    def user_id_exists(self, id):
        result = False
        for person in self.users.people:
            if person.id == id:
                result = True
                break
        return result
    
    def user_exists(self, user):
        result = False
        for existing_user in self.users.people:
            if existing_user.UserDetails.email == user.email:
                result = True
                break
        return result

    #TODO
    def search_users(self, user):
        result = False
        for person in self.users.people:
            if person.id == id:
                result = True
                break
        return result
