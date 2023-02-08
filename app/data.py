from os import getenv
import pandas as pd
from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient

class Database:
    '''
    Interfaces with MongoDB to store, retrieve, and manipulate data from MonsterLab.
    '''

    def __init__(self):
        '''
        Initializes the database class, loads the .env data,
        connects to MongoDB for TLS, identifies "Bandersnatch" as MongoDB data for collection.
        '''
        load_dotenv()
        database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["Bloomtech"]
        self.collection = database["Bandersnatch"]

    def seed(self, amount):
        '''
        Seeds the number of monster instances (amount) into the MongoDB database.
        '''
        documents = []
        for i in range(amount):
            documents.append(Monster().to_dict())

        self.collection.insert_many(documents)

    def reset(self):
        '''
        Deletes all documents from the database.
        '''
        self.collection.delete_many({})

    def count(self) -> int:
        '''
        Returns the number count of documents in the database.
        '''
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        '''
        Gets the cursor to all documents, converts cursor to list of dictionaries.
        Returns the database as a Pandas DataFrame.
        '''
        cursor = self.collection.find()
        documents = list(cursor)
        df = pd.DataFrame(documents)
        return df

    def html_table(self) -> str:
        '''
        Creates an HTML table to display data from the database, adding header titles and row count.
        '''
        df = self.dataframe()
        df = df.drop(df.columns[0], axis=1)
        data = df.to_dict(orient="records")
        table = "<table>"
        table += "<tr><th></th><th>Name</th><th>Type</th><th>Level</th><th>Rarity</th><th>Damage</th>" \
                 "<th>Health</th><th>Energy</th><th>Sanity</th><th>Timestamp</th></tr>"
        for index, item in enumerate(data):
            table += "<tr>"
            table += "<td>" + str(index) + "</td>"
            for value in item.values():
                table += "<td>" + str(value) + "</td>"
            table += "</tr>"
        table += "</table>"
        return table
