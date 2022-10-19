
import logging


def create_features(df_stock, nlags=10):
    df_resampled = df_stock.copy()
    lags_col_names = []
    for i in range(nlags + 1):
        df_resampled['lags_' + str(i)] = df_resampled['close'].shift(i)
        lags_col_names.append('lags_' + str(i))
    df = df_resampled[lags_col_names]
    df['SMA30'] = df['lags_1'].rolling(15).mean()  
    print(df)
    df = df.dropna(axis=0)

    return df


def create_X_Y(df_lags):
    X = df_lags.drop('lags_0', axis=1)
    Y = df_lags[['lags_0']]
    return X, Y

def sma30(df_features):
    #print(df_features)
    df_features['SMA10'] = df_features['lags_1'].rolling(10).mean()
    preds = df_features['SMA30']
    #print('preds')
    #print(preds)
    return preds 
    
class Stock_model_Baseline():

    def __init__(self, data_fetcher):
        self.log = logging.getLogger()
        self.lr = sma30
        self._data_fetcher = data_fetcher
        self.log.warning('here')
        
    def fit(self, X, Y=None):
        data = self._data_fetcher(X)
        df_features = create_features(data)
        df_features, Y = create_X_Y(df_features)
        self.lr(df_features)
        return self


    def predict(self, X, Y=None):
        print(X)
        data = self._data_fetcher(X, last=True)
        #print(data)
        df_features = create_features(data)
        #print(df_features)
        df_features, Y = create_X_Y(df_features)
        #predictions = self.lr(df_features)
        predictions = df_features['SMA30']      
        print(predictions)

        #return predictions.flatten()[-1]
        return round(predictions[-1],2)