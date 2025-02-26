import streamlit as st
import pickle
import pandas as pd

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

model_files = {
    'Random Forest': 'models/random_forest.pkl',
    'Logistic Regression': 'models/logistic_regression.pkl',
    'SVM': 'models/svm.pkl'
}

st.title('IPL Win Predictor')

selected_model_name = st.selectbox('Select a Machine Learning Model', list(model_files.keys()))
selected_model_file = model_files[selected_model_name]
pipe = pickle.load(open(selected_model_file, 'rb'))

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

selected_city = st.selectbox('Select host city', sorted(cities))
target = st.number_input('Target', min_value=0)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score', min_value=0)
with col4:
    overs = st.number_input('Overs completed', min_value=0.0, step=0.1)
with col5:
    wickets_out = st.number_input('Wickets out', min_value=0, max_value=10)

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - int(overs * 6)
    wickets_left = 10 - wickets_out
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
    required_strike_rate = (runs_left / wickets_left) * 100 if wickets_left > 0 else 0
    current_strike_rate = (score / wickets_out) * 100 if wickets_out > 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr],
        'required_strike_rate': [required_strike_rate],
        'current_strike_rate': [current_strike_rate]
    })

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    st.header(f"{batting_team} - {round(win * 100)}%")
    st.header(f"{bowling_team} - {round(loss * 100)}%")

    st.write(f"Balls Left: {balls_left}")
    st.write(f"Required Strike Rate: {required_strike_rate:.2f}")
    st.write(f"Current Strike Rate: {current_strike_rate:.2f}")
    st.write(f"Wickets Left: {wickets_left}")
