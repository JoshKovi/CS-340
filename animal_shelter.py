#Python Library file for CRUD interaction with AAC database
from pymongo import MongoClient
from bson.objectid import ObjectId

#This is used for authentication as it was the only way I could get it to
#work without hardcoding username and password
from urllib.parse import quote_plus

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
        #quote_plus allows username and password to be passed correctly to
        #start client session
        self.client = MongoClient('mongodb://%s:%s@localhost:37046/?authMechanism=DEFAULT&authSource=AAC'%(quote_plus(username), quote_plus(password)))
        #Sets the database to be worked in
        self.database = self.client['AAC']

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        '''if dictionary len is > 0 the data is inserted and returns true
        otherwise false is returned (raising exception stops return of false)'''
        if len(data) > 0:
            #self.database.animals.insert(data)  # data should be dictionary   
            return (self.database.animals.insert(data) != None)
        else:
            #raise Exception("Nothing to save, because data parameter is empty")
            return False

# Create method to implement the R in CRUD. 
    def read_one(self, data): 
        '''Returns the first found entry for the specified data
        raises exception if data is empty dictionary (allowing a DB dump)
        or if the cursor has no data (nothing was found)'''
        if len(data) <=0:
            raise Exception("Must enter a search term to return value")
            
        cursor = self.database.animals.find_one(data)
        
        if cursor == None:
            raise Exception("No data found in read_one")
            
        return cursor
    def read_all(self, data):
        '''Returns the cursor of entries for the specified data
        raises exception if data is empty dictionary (allowing a DB dump)
        or if the cursor has no data (nothing was found)'''
        
        '''Assignment requires database dump so this is commented out
        if len(data) <=0:
            raise Exception("Must enter a search term to return value")
        '''
        cursor = self.database.animals.find(data)
        
        if cursor.count() == 0:
            raise Exception("No data found in read_all")
            
        return cursor
    
    def update(self, search_dic, data_input):
        '''Used to update documents, an input dictionary will be used to update any required
        fields. The dictionary is formatted {field_name: field_value, field_name2:field_value2}, 
        the search_dict is also input in the same manner'''
        search_results = {}
        list_of_keys = []
        for x in self.read_all(search_dic):
            search_results[x['_id']] = x
            list_of_keys.append(x['_id'])

        if(len(list_of_keys) > 1):
            '''Placeholder for later functionality like update_all function'''
            raise Exception("Multiple Values found, please narrow search")

        self.database.animals.update(search_dic, {'$set': data_input})
        return self.database.animals.find_one(search_dic)
    
    def delete(self, search_dic):
        '''Used to delete documents, Uses the search dictionary to that end
        The dictionary is formatted {field_name: field_value, field_name2:field_value2}'''
        search_results = {}
        list_of_keys = []
        for x in self.read_all(search_dic):
            search_results[x['_id']] = x
            list_of_keys.append(x['_id'])

        if(len(list_of_keys) > 1):
            '''Placeholder for later functionality like update_all function'''
            raise Exception("Multiple Values found, please narrow search")
        
        self.database.animals.delete_one(search_dic)
        if(self.database.animals.find_one(search_dic)!=None):
            raise Exception("Something went wrong, please try again")
        return search_results[list_of_keys[0]]
    
               
               
    
    