import sys,json
import numpy as np
from sklearn.externals import joblib

data = {"data":[0,2,0,100,1,100,10000]
    }
data = np.array(data['data'])
sav = joblib.load('./mel_hp.ml')
pred = sav.predict(data.reshape(1,-1))
result = int(round(pred[0],0))
result_a = format(abs(result),',')
print(result_a)
