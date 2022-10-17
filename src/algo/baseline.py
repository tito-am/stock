import logging

def create_features(df_stock, nwindow=30):
    df_resampled = df_stock.copy()
    #nwindow_col_names = []
    
    df_resampled['SMA30'] = df_clean['close'].rolling(nwindow).mean()#a voir, il faut pas shifter?
    
    df = df_resampled['SMA30']
    print(df)
    df = df.dropna(axis=0)
    
    return df

def tagger_sma30(row):
    if row['SMA30']<row['lag_0']:
        return 'Sell'
    else:
        return 'Buy'

def baseline(df):
    df['pred'] = df.apply(tagger_sma30 ,axis=1) 
    

def create_X_Y(df_lags):
    X = df_lags.drop('close', axis=1)
    Y = df_lags[['close']]
    return X, Y



    

   


for ticker in list_ticker_snp_500:
    df = si.get_data(ticker)
    
    for lag in range(0,1):
        df[f'lag_{lag}'] = df['close'].shift(lag)

    df['next'] = df['close'].shift(-1)

    df['out'] = df.apply(tagger ,axis=1)
    
    columns = [f'lag_{lag}' for lag in reversed(range(0,1))]
    columns+=['next']
    columns+=['out']

    df_clean = df[columns]
    
    df_clean['SMA30'] = df_clean['lag_0'].rolling(30).mean()
    
    df_clean = df_clean.dropna(axis=0) #pred à faire

    df_clean['pred'] = df_clean.apply(tagger_sma30 ,axis=1)
    
    k = balanced_accuracy_score(df_clean.out,df_clean.pred)
    
    perf.append(k)

class Stock_model(BaseEstimator, TransformerMixin):
    
    def __init__(self, data_fetcher):
        self.log = logging.getLogger()
        self.lr = baseline()
        self._data_fetcher = data_fetcher
        self.log.warning('here')

    def fit(self, X, Y=None):
        data = self._data_fetcher(X)
        df_features = create_features(data)#juste effacer ce qui est de trop
        df_features, Y = create_X_Y(df_features)
        self.lr(df_features)
        return self

    def predict(self, X, Y=None):
        print(X)
        data = self._data_fetcher(X, last=True)
        print(data)
        df_features = create_features(data)
        print(df_features)
        df_features, Y = create_X_Y(df_features)
        predictions = self.lr(df_features)

        return predictions.flatten()[-1]