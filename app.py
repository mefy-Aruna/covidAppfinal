import numpy as np
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import pickle
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model = pickle.load(open('RFCovidModel.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if("text" == "M"):
        text = 1
    else:
        text =0
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    
    prediction = model.predict(final_features)
    prediction=model.predict_proba(final_features)
    
    alpha=0.70
    beta=0.70
   # finalProb=
    for i in prediction:
     # print("list: i is:",i)
      if i[1] > alpha and i[1]> i[0]:
        ele =i[1]
       # print("positive")
        add=1
        finalProb=add
        #finalLabelProb.append(add)
    
      elif i[0]>beta and i[0]>i[1]:
       # print("negative")
        add=0
        finalProb= add
        #finalLabelProb.append(add)
      else:
        #print("abstention incurred")
        add=2
        ##remove prob with target as 2
        finalProb=add
    output=[]

    output.append(finalProb)
    output.append(prediction[0])
    #output = finalProb
    #also display output from 'prediction' variable

    return render_template('index1.html', prediction_text1='Patient is (positive(1) or negative(0)= {}'.format(output[0]),prediction_text2='              Probabilities:{} '.format(output[1]))
    

if __name__ == "__main__":
    app.run(debug=True)
