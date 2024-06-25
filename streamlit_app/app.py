import streamlit as st
import requests
import json
import pandas as pd

st.subheader('This is a slider')
st.subheader('')
col1, col2,col3 = st.columns([0.45,0.1,0.45],gap='medium')
with col1:
    age = st.number_input(label='Age',step=1,min_value=0) #
    height = st.text_input(label='Height') # 
    gender = st.selectbox('Gender',options=['Female','Male']) # 
    favc = st.selectbox(label='Frequent Consumption of High Caloric Food',options=['Yes','No']) # 
    ncp = st.number_input(label='Number of Main meals',step=1,max_value=5,min_value=0) # 
    smoke = st.selectbox(label='Smoking', options=['No','Yes']) # 
    scc = st.selectbox(label='Monitoring Calories consumption?', options=['No','Yes']) # 
    tue = st.number_input(label='Time using Technological Devices',step=0.5,min_value=0.0,max_value=24.0) #
    
with col3:
    weight = st.number_input(label='Weight (kg)',step=0.5,min_value=0.0) # 
    height_metric = st.selectbox(label='Units of Measurement (Height)',options=['Meter (m)', 'Feet & Inches (ft & in)']) # 
    family_history = st.selectbox(label='Any Family member with Over Weight?',options=['Yes','No']) # 
    fcvc = st.selectbox(label='Vegetable Intake', options=['Less','Moderate','High']) # 
    caec = st.selectbox(label='Consumption of Food between Meals',options=['Less','Moderate','High','No']) # 
    ch20 = st.number_input(label='Consumption of Water Daily (in Ltr)',step=0.25,min_value=0.0) # 
    faf = st.selectbox(label='Physical Activity Frequency', options=['Less','Moderate','High']) # 
    calc = st.selectbox(label='Alcohol Consumption',options=['No','Yes']) #

st.text('')
st.text('')
scol1,scol2,scol3 = st.columns([0.41, 0.35, 0.24],gap='large')
with scol2:
    submit =  st.button(label='Submit',type='primary')

if submit:
    print('came here 1')
    if height_metric == 'Feet & Inches (ft & in)':
        print('came here 2')
        if "'" not in height:
            print('came here 3')
            st.write('Please enter your height in feet\'inches format. Ex: 5\'8, 4\'9 etc.')
        else:
            feet_to_meter = 0.3048
            inch_to_meter = 0.0254
            height_values = height.split("'")
            first_part_value = int(height_values[0]) * feet_to_meter
            second_part_value = int(height_values[1]) * inch_to_meter
            height = first_part_value + second_part_value
    else:
        height = int(height)

    favc = 0 if favc=='Yes' else 1
    fcvc = 1 if fcvc=='Less' else 2 if fcvc=='Moderate' else 3
    caec = 0 if caec=='Less' else 1 if caec=='Moderate' else 2 if caec == 'High' else 3
    smoke = 1 if smoke == 'Yes' else 0
    
    scc = 1 if scc=='Yes' else 0
    if gender.lower() == 'female':
        gender_female = 1
        gender_male = 0
    else:
        gender_female = 0
        gender_male = 1
    family_history = 0 if family_history == "Yes" else 1
    faf = 0 if faf == "Less" else 1 if faf=="Moderate" else 2
    calc = 0 if calc == "Yes" else 1

    # st.write('Details submitted successfully!')

    data = {'feature':[age,height,weight,family_history,
                       favc,fcvc,ncp,caec,smoke,ch20,
                       scc,faf,tue,calc,gender_female,
                       gender_male]}
    data_json = json.dumps(data)
    response = requests.post(url = "https://obesity-risk-classification-api.onrender.com/predict",
                             data=data_json)
    if response.status_code == 200:
        prediction = response.json()['prediction']
        st.write(f"{prediction}")
        categories = ['Under_Weight','Normal_Weight','Overweight_Level_I','Overweight_Level_II','Obesity_Type_I',
                      'Obesity_Type_II','Obesity_Type_III']
        catg_df = pd.DataFrame(categories,index=range(1,len(categories)+1),columns=['Weight_Categories'])
        def highlight_value(value):
            color = 'background-color: cyan' if value['Weight_Categories'] == prediction else ''
            return [color]
        catg_df = catg_df.style.apply(highlight_value,axis=1)

        st.dataframe(catg_df)
    else:
        st.write(f'Error Occured!!! Please Try Again.')

