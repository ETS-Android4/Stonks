from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import json

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'green21'
app.config['MYSQL_DB'] = 'stonks'

mysql = MySQL(app)


@app.route('/',methods=['GET', 'POST'])
def hell():

    querry1 = request.json
    name = querry1['query']
    print("typeeeee",type(name))
    my_sql_conn = mysql.connect
    #cur = my_sql_conn.cursor()
    #cur.execute(''' SELECT * FROM {} '''.format(name))
    #result = cur.fetchall()


    
    df_nse = pd.read_sql_query(''' SELECT * FROM {} ORDER BY Date DESC LIMIT 60'''.format(name), con=my_sql_conn)

    df_nse["Date"]=pd.to_datetime(df_nse.Date,format="%Y-%m-%d")
    df_nse.index=df_nse['Date']


    data=df_nse.sort_index(ascending=True,axis=0)
    
    new_data=pd.DataFrame(index=range(0,len(df_nse)),columns=['Date','Close'])

    for i in range(0,len(data)):
        new_data["Date"][i]=data['Date'][i]
        new_data["Close"][i]=data["Close"][i]

    new_data.index=new_data.Date
    new_data.drop("Date",axis=1,inplace=True)

    model=load_model("model.h5")

    inputs = new_data.values
    data1 = inputs.tolist()

    scaler=MinMaxScaler(feature_range=(0,1))
    inputs=scaler.fit_transform(inputs)

    inputs=inputs.reshape(1,-1) #one row and as many number of col

    #print("shape is",inputs.shape)
    #print("input after :",inputs)

    X_test=np.array(inputs)

    print("xtest",X_test.shape)

    X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1)) #3 params casue lstm nedds a 3d array of (sample,timesteps,features)
    closing_price=model.predict(X_test)
    closing_price=scaler.inverse_transform(closing_price)
    print("clossing price is",closing_price)
    closing_price=closing_price.tolist()
    print("type  clossing price is",type(closing_price))
    print("type  data is",type(data1))
    result = data1 + closing_price #adding predicted price with the past 60 days price 
    #result= result[::-1] #making it in the ascending order of dates (ie result is reversed)
    lastval = data1[len(data1) - 1]
    result = { 'values' : result,
                'pred' : closing_price,
                'lastval' : lastval }
    jresult = json.dumps(result)
    print(jresult)
    print(type(jresult))
    print("connection secure")
    
    return jresult





if __name__ == "__main__":
    app.run(host="192.168.0.8", port=5000, debug=True )