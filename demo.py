from coapclient import CoapClient, UserService

import json

# this file is for demo purposes only 
# RUN the server first!


client = CoapClient()
user_service = UserService(client)

#create a bunch of new users
user_service.create_user("james", "charlton", "newemail@test.com", "01778123451")
user_service.create_user("Steve", "surname", "newemail2@test.com", "01778123452")
user_service.create_user("Peter", "wiggle", "newemail3@test.com", "01778123453")
user_service.create_user("George", "foobar", "newemail4@test.com", "01778123454")
user_service.create_user("Gary", "johnson", "newemail5@test.com", "01778123455")

#read back all the registeres users and print them out
all_users = user_service.get_users()
print(all_users)

#convert it to python
data = json.loads(all_users)

# just grab the first item id for deletion after
id_to_delete = data["people"][0]["id"]
#grab the second for modification
user_to_modify = data["people"][1]["UserDetails"]
user_id_to_modify = data["people"][1]["id"]
#delete the first user
user_service.delete_user_by_id(id_to_delete)

#read back all the registeres users and print them out
all_users = user_service.get_users()
print(all_users)

#update the second user "steve" to a different email address and phone number
user_service.update_user(user_id_to_modify, None, None, "supersteve@steve.com", "98765432100" )


#read back all the registeres users and print them out
all_users = user_service.get_users()
print(all_users)

client.stop()