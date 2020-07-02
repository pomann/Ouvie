############################
# Made by: Roman Prochazka #
# Student number: 15711579 #
# Date: 28/01/2020         #
############################

from pymongo import MongoClient

class OuvieDB:

    # Connects to mongoDB, default localhost, 27017
    def __init__(self, ip='localhost', port=27017):
        self.client = MongoClient()
        self.client = MongoClient(ip, port)
        
        # Databse for user credentintals
        self.db = self.client.credentials
        self.details = self.db.details
        
        # Database for user files
        self.db_files = self.client.dbFiles
