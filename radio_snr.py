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

