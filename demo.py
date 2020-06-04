from coapclient import CoapClient
import json

# this file is for demo purposes only 
# RUN the server first!


client = CoapClient()
#create a bunch of new users
client.create_update_user("James", "Charlton", "newemail@test.com", "01778123451")
client.create_update_user("Steve", "surname", "newemail2@test.com", "01778123452")
client.create_update_user("Peter", "wiggle", "newemail3@test.com", "01778123453")
client.create_update_user("George", "foobar", "newemail4@test.com", "01778123454")
client.create_update_user("Gary", "johnson", "newemail5@test.com", "01778123455")

#read back all the registeres users
all_users = client.get_users()

#spit it out to cli
print(all_users)

#convert it to python
data = json.loads(all_users)

# just grab the first item id
id_to_delete = data["people"][0]["id"]

#delete that user
client.delete_user(id_to_delete)

#read back all the registeres users
all_users = client.get_users()

#spit it out to cli
print(all_users)

client.stop()