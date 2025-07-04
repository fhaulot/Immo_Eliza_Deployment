import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class Preprocessing : 

    def __init__(self):
        pass

    def read_csv(self, df, path):
        """
        Reading the cleaned_data csv file
        """
        df = pd.read_csv(path)
        print(df.info())
        return df
    
    def drop_columns(self, df):
        """
        Drop specified columns from the DataFrame.
        """
        Col_to_drop = ["id", "url", 'locality', "MunicipalityCleanName", "price_square_meter", "hasGarden", "type", "region"]
        cleaned_columns = df.drop(columns=Col_to_drop, axis=0)
        print(cleaned_columns.info())
        return cleaned_columns
    
    def ordinal_building_condition(self, df):
        condition_order = {"AS_NEW": 1, "GOOD": 2, "JUST_RENOVATED": 3,
        "TO_RENOVATE": 4, "TO_BE_DONE_UP": 5, "TO_RESTORE": 6}
        df['encoded_condition'] = df['buildingCondition'].map(condition_order)
        df.drop(columns=['buildingCondition'], inplace=True)
        return df
    
    def ordinal_epc_score(self, df) :
        """
        Perform ordinal encoding for the column of epc score using a mapping
        """
        epc_order = {"A" : 1, "B" : 2, "C" : 3, "D" : 4, "E" : 5, "F" : 6, "G" : 7}
        df['encoded_epc'] = df['epcScore'].map(epc_order)
        df.drop(columns=['epcScore'], inplace=True)
        return df
    
    def categorical_encode(self, df):
        """
        Perform categorical encoding on specified columns.
        """
        df_encoded = pd.get_dummies(df, columns=["province", "subtype"], drop_first=True)
        bool_cols = df_encoded.select_dtypes(include=["bool"]).columns
        df_encoded[bool_cols] = df_encoded[bool_cols].astype(int)
        return df_encoded
    
    def postcode_geo(self, df):
        """
        Add geographical coordinates (latitude and longitude) to the DataFrame based on postcodes.
        """
        df_postcode = pd.read_csv(r'C:\Users\fhaul\Documents\GitHub\Immo_Eliza_Regression\belgian-cities-geocoded (1).csv')
        df_postcode = df_postcode.astype({'postCode': 'int64'})
        # df_postcode.info()
        df
        df = pd.merge(df, df_postcode[['postCode', 'lat', 'lng']], on='postCode', how='left')
        df = df.drop(columns=["postCode"], axis=1)
        return df
    
