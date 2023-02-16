from datetime import datetime
import joblib
import numpy as np
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier


class Machine:
    '''
    A machine learning model using Random Forest Classifier.
    '''

    def __init__(self, df: DataFrame):
        '''
        Initializes the machine learning model with the DataFrame.
        '''
        self.name = "Random Forest Classifier"
        self.target = df["Rarity"]
        self.features = df.drop(columns=["Rarity"])
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.model = RandomForestClassifier()
        self.model.fit(self.features, self.target)

    def __call__(self, pred_basis: DataFrame):
        '''
        Makes a prediction based on the DataFrame.
        '''
        probability = self.model.predict_proba(pred_basis)
        prediction = self.model.predict(pred_basis)[0]
        confidence = np.max(probability, axis=1)
        return prediction, confidence

    def save(self, filepath):
        '''
        Saves the machine learning model to a filepath using joblib.
        '''
        joblib.dump(self, filepath)

    @staticmethod
    def open(filepath):
        '''
        Opens a machine learning model from a filepath using joblib.
        '''
        obj = joblib.load(filepath)
        return obj

    def info(self, name, timestamp):
        '''
        Returns a formatted string of information about the model: name, and timestamp.
        '''
        return f"Base Model: {self.name}<br/>Timestamp: {self.timestamp}"