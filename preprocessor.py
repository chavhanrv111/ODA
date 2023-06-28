import pandas as pd

def preprocess(df,region_df):
   
    #get only summer olympics data
    df = df[df['Season'] == 'Summer']

    #merge with region_df
    df = df.merge(region_df,on="NOC",how="left")

    #droping dumplicates rows
    df.drop_duplicates(inplace=True)

    #one hot encodeing on medals column

    df = pd.concat((df,pd.get_dummies(df['Medal'])),axis=1)

    return df