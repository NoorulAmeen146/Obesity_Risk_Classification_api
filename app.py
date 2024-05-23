from flask import Flask, request, jsonify
import pickle
import subprocess
import sys

app = Flask(__name__)

@app.route('/')
def index():
    # return '<h1> Hello World, I\'m back! </h1>'
    return '<h1>Hello, This is an api for Obesity Risk Classification Inference!</h1>'

@app.route('/predict', methods=['POST'])
def predict():
    try:
        subprocess.run([sys.executable,'-m','pip','install','pandas', 'numpy', 'scikit-learn','--quiet'])
        print('installation successfull')
    except:
        return "installation failed"
    try:
        import pandas as pd
        import sklearn
    except:
        return "import failed"
    with open('model.pkl','rb') as file:
        model = pickle.load(file)
    
    data = request.get_json(force=True)
    
    column_names = ['Age', 'Height', 'Weight', 'family_history_with_overweight', 'FAVC',
       'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC',
       'Gender_Female', 'Gender_Male']
    
    df = pd.DataFrame([data['feature']],columns=column_names)
    prediction = model.predict(df)
    target_col_map = {
        0:'Insufficient_Weight',
        1:'Normal_Weight',
        2:'Overweight_Level_I',
        3:'Overweight_Level_II',
        4:'Obesity_Type_I',
        5:'Obesity_Type_II',
        6:'Obesity_Type_III'
    }
    output = {'prediction': target_col_map[int(prediction[0])]}

    return jsonify(output)