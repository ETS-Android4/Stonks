import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error 
from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))

df=pd.read_csv("NSE-TATA.csv")
df.head()

df["Date"]=pd.to_datetime(df.Date,format="%Y-%m-%d")
df.index=df['Date']
from keras.models import Sequential
from keras.layers import LSTM,Dropout,Dense

data=df.sort_index(ascending=True,axis=0)
new_dataset=pd.DataFrame(index=range(0,len(df)),columns=['Date','Close'])

for i in range(0,len(data)):
    new_dataset["Date"][i]=data['Date'][i]
    new_dataset["Close"][i]=data["Close"][i]
    

new_dataset.index=new_dataset.Date
new_dataset.drop("Date",axis=1,inplace=True)

final_dataset=new_dataset.values

train_data=final_dataset[0:987,:]
valid_data=final_dataset[987:,:]


scaler=MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(final_dataset)

x_train_data,y_train_data=[],[]

for i in range(60,len(train_data)):
    x_train_data.append(scaled_data[i-60:i,0])  
    y_train_data.append(scaled_data[i,0]) 
    
x_train_data,y_train_data=np.array(x_train_data),np.array(y_train_data)

x_train_data=np.reshape(x_train_data,(x_train_data.shape[0],x_train_data.shape[1],1))

#Testing the data
inputs_data=valid_data
#inputs_data=inputs_data.reshape(-1,1)
inputs_data=scaler.transform(inputs_data)

print("len of inut",len(inputs_data))
X_test,y_test=[],[]
for i in range(60,inputs_data.shape[0]):
    X_test.append(inputs_data[i-60:i,0])
    y_test.append(scaled_data[i,0])
X_test,y_test=np.array(X_test),np.array(y_test)
X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))

#x_train = x_train.astype('float32') / 255.0
#X_test = X_test.astype('float32') / 255.0

lstm_model=Sequential()
lstm_model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train_data.shape[1],1)))
lstm_model.add(Dropout(0.2))
lstm_model.add(LSTM(units = 50, return_sequences = True))
lstm_model.add(Dropout(0.2))

lstm_model.add(LSTM(units = 50))
lstm_model.add(Dropout(0.2))

lstm_model.add(Dense(1))


lstm_model.compile(loss='mean_squared_error',optimizer='adam' )
lstm_model.fit(x_train_data,y_train_data,epochs=1,batch_size=1,verbose=2)

test_pred = lstm_model.predict(X_test)
#closing_price=scaler.inverse_transform(test_pred)
#print("pred data is ",closing_price)

test_acc= mean_squared_error(y_test,test_pred)
#test2 = lstm_model.evaluate(X_test,y_test)
#print("Eval",test2)
print("MSE =  ",test_acc)
lstm_model.save("model.h5")