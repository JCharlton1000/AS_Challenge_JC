from protobuf.user_pb2 import Users as pbusers
from protobuf.user_pb2 import User as pbuser
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
        userpb = pbuser()
        userpb.MergeFromString(bytes(user, 'utf-8'))
        #have we been given an id - if so look for it
        if hasattr(userpb, "id"):
            result, existing_user = self.get_user_by_id(userpb.id)
            if result:
                #update an existing user using the given ID
                existing_user.MergeFromString(bytes(user, 'utf-8'))
            else:
                new_user = self.users.people.add()
                new_user.MergeFromString(bytes(user, 'utf-8'))
                new_user.id = str(uuid.uuid4())
                result= True
        else: # no id given so its a new user
            new_user = self.users.people.add()
            new_user.MergeFromString(bytes(user, 'utf-8'))
                #assign a new ID
                #new_user.id = len(self.users.people) # TODO this is not good - it's just an index for now
            new_user.id = str(uuid.uuid4())
            result= True
        return result
    
    #
    def remove_user(self, user):
        result = False
        userpb = pbuser()
        userpb.MergeFromString(bytes(user, 'utf-8'))
        """ for index, person in enumerate(self.users.people):
            person = person
            result = True """
        result, user = self.get_user_by_id(userpb.id)
        result = self.remove_user_by_id(userpb.id)
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

    # the left user fields is compared to the right - so if the right contains more fields these are ignored
    # this needs reworking for a btter comparison - a comparison could be made by serializing both but this is not
    # a good approach as protobufs can contain extra fields
    def is_same(self, user_l, user_r):
        result = False
        for descriptor in user_l.descriptor.fields:
            test+1
        return result
