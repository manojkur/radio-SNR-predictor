import numpy as np
import pandas as pd

def get_long(ls):
    # Do you belive in magic?
    res = 20.0 * float(ord(ls[0]) - ord('a')) + 2.0 * float(int(ls[1])) - 180
    if len(ls) >= 3:
        res += (5.0/60.0) * float(ord(ls[2]) - ord('a') + 0.5)
    return res

def get_lat(ls):
    # More magic
    res = 10.0*(ord(ls[0])-ord('a'))+int(ls[1])-90
    if len(ls) >= 3:
        res += (1.0/60.0)*2.5*(ord(ls[2])-ord('a')+0.5)
    return res

def grid_to_coordinates(sq):
    if len(sq) == 6 or len(sq) == 4:
        long, lat= sq[::2].lower(), sq[1::2].lower()
        return (get_lat(lat), get_long(long))
    return None

def fix_sunspot_dataframe(df):
    #sunspot dataframe conditioning
    df.columns=['year','month','day','days','number of sunspots','std','number of observations','divinitive']
    df.index=df.year
    for i in range(1818,2018):
        df=df.drop(i)
    df.index=df.month
    for i in range(1,12):
        if i!=3:
            df=df.drop(i)
    df.index=np.linspace(1,df.shape[0],df.shape[0])
    #changing date (y/m/d) to days since epoch and getting rid of old date columns
    df['days'] = (pd.to_datetime(df.iloc[:,0:3])-pd.Timestamp(0)).dt.days
    df=df.drop(['year','day','month'],axis=1)
    return df

def sunspot_addition(df,sunspot_df):
    #matching dates between dataframes then appending correct number of sunspot numbers per day
    df['sunspots']=0
    for i in range(df.shape[0]):
        for j in range(sunspot_df.shape[0]):
            if df.iloc[i,16] == sunspot_df.iloc[j,0]:
                x=sunspot_df.iloc[j,1]
                df.iloc[i,18]=x
    return df

def preprocess_data(df):
    r_coords = df['reporter_grid'].apply(grid_to_coordinates).apply(pd.Series)
    df['rx_lat'] = r_coords.iloc[:,0]
    df['rx_long'] = r_coords.iloc[:,1]
    t_coords = df['tx_grid'].apply(grid_to_coordinates).apply(pd.Series)
    df['tx_lat'] = t_coords.iloc[:,0]
    df['tx_long'] = t_coords.iloc[:,1]
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['day'] = (df['timestamp'] - pd.Timestamp(0)).dt.days
    df['hour'] = df['timestamp'].dt.hour
    df = df.drop(['reporter_grid', 'tx_grid', 'timestamp'], axis=1)
    return df
