import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import random


st.set_page_config(page_title='IPL Win Predictor', layout='wide')
st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
        }
        .stButton > button {
            background-color: #ff4b4b;
            color: white;
            font-size: 18px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title('🏏 IPL Win Predictor')
st.markdown("### Predict the probability of a team's victory based on match conditions")

teams = {
    'Chennai Super Kings': [
        'MS Dhoni', 'Devon Conway', 'Ruturaj Gaikwad', 
        'Shivam Dube', 'Ravindra Jadeja', 'Vijay Shankar', 'Deepak Hooda', 'Rachin Ravindra',
        'Ravichandaran Ashwin', 'Sam Curran'
    ],
    'Delhi Capitals': [
        'Harry Brook',  'Faf Du Plessis', 'Tristan Stubbs', 'KL Rahul','Axar Patel', 
         'Madhav Tiwari', 'Manvanth Kumar L', 'Kuldeep Yadav',
         'Mitchell Starc', 'Mohit Sharma', 'T. Natarajan'
    ],
    'Gujarat Titans': [
        'Shubman Gill', 'Sai Sudharsan', 'Glenn Phillips', 'Jos Buttler',
        'Rashid Khan', 'Rahul Tewatia',
        'Jayant Yadav', 'Arshad Khan', 'Sherfane Rutherford', 'Washington Sundar',
         'Mohammad Siraj'
    ],
    'Kolkata Knight Riders': [
        'Rinku Singh',  'Manish Pandey', 'Ajinkya Rahane', 'Quinton De Kock',
         'Sunil Narine', 'Andre Russell', 'Ramandeep Singh',
        'Venkatesh Iyer', 'Anukul Roy',  'Varun Chakaravarthy',
        'Harshit Rana'
    ],
    'Lucknow Super Giants': [
        'Aiden Markram', 'David Miller',  'Ayush Badoni', 'Nicholas Pooran', 'Rishabh Pant',
         'Abdul Samad',  'Mitchell Marsh', 'Arshin Kulkarni', 'Rajvardhan Hangargekar',
        'Ravi Bishnoi', 'Mayank Yadav'
    ],
    'Mumbai Indians': [
        'Jasprit Bumrah', 'Suryakumar Yadav', 'Tilak Verma',  'Robin Minz', 'Rohit Sharma',
        'Hardik Pandya', 'Naman Dhir',  'Will Jacks',
        'Karn Sharma', 'Trent Boult',
        'Deepak Chahar'
    ],
    'Punjab Kings': [
        'Vishnu Vinod', 'Josh Inglis', 'Shashank Singh',
        'Harpreet Brar', 
        'Pravin Dubey', 'Glenn Maxwell', 'Marcus Stoinis', 'Yash Thakur', 'Vyshak Vijaykumar', 
       'Arshdeep Singh', 'Yuzvendra Chahal'
    ],
    'Rajasthan Royals': [
        'Sanju Samson', 'Yashasvi Jaiswal', 'Shimron Hetmyer', 'Shubham Dubey', 
        'Riyan Parag', 'Vaibhav Suryavanshi',  'Nitish Rana',
        'Sandeep Sharma', 'Kumar Kartikeya', 'Maheesh Theekshana',
         'Jofra Archer'
    ],
    'Royal Challengers Bangalore': [
        'Rajat Patidar', 'Virat Kohli', 'Swastik Chhikara', 'Devdutt Padikkal', 'Phil Salt',
        'Swapnil Singh',  'Liam Livingstone', 'Krunal Pandya', 'Tim David',
        'Lungisani Ngidi', 'Bhuvneshwar Kumar'
    ],
    'Sunrisers Hyderabad': [
         'Sachin Baby','Heinrich Klaasen', 'Ishan Kishan',
         'Pat Cummins', 'Nitish Reddy', 'Abhishek Sharma', 'Travis Head', 
         'Rahul Chahar', 'Jaydev Unadkat',  'Mohammad Shami',
        'Adam Zampa'
    ]
}


player_roles = {
    # Chennai Super Kings
    'MS Dhoni': 'Wicket-keeper Batsman',
    'Devon Conway': 'Batsman',
    'Ruturaj Gaikwad': 'Batsman',
    'Shivam Dube': 'All-rounder',
    'Ravindra Jadeja': 'All-rounder',
    'Vijay Shankar': 'All-rounder',
    'Deepak Hooda': 'All-rounder',
    'Rachin Ravindra': 'All-rounder',
    'Ravichandaran Ashwin': 'Bowler',
    'Sam Curran': 'All-rounder',
    
    # Delhi Capitals
    'Harry Brook': 'Batsman',
    'Faf Du Plessis': 'Batsman',
    'Tristan Stubbs': 'Batsman',
    'KL Rahul': 'Wicket-keeper Batsman',
    'Axar Patel': 'All-rounder',
    'Madhav Tiwari': 'Batsman',
    'Manvanth Kumar L': 'Bowler',
    'Kuldeep Yadav': 'Bowler',
    'Mitchell Starc': 'Bowler',
    'Mohit Sharma': 'Bowler',
    'T. Natarajan': 'Bowler',
    
    # Gujarat Titans
    'Shubman Gill': 'Batsman',
    'Sai Sudharsan': 'Batsman',
    'Glenn Phillips': 'Wicket-keeper Batsman',
    'Jos Buttler': 'Wicket-keeper Batsman',
    'Rashid Khan': 'All-rounder',
    'Rahul Tewatia': 'All-rounder',
    'Jayant Yadav': 'All-rounder',
    'Arshad Khan': 'Bowler',
    'Sherfane Rutherford': 'All-rounder',
    'Washington Sundar': 'All-rounder',
    'Mohammad Siraj': 'Bowler',
    
    # Add for remaining teams...
    'Rinku Singh': 'Batsman',
    'Manish Pandey': 'Batsman',
    'Ajinkya Rahane': 'Batsman',
    'Quinton De Kock': 'Wicket-keeper Batsman',
    'Sunil Narine': 'All-rounder',
    'Andre Russell': 'All-rounder',
    'Ramandeep Singh': 'All-rounder',
    'Venkatesh Iyer': 'All-rounder',
    'Anukul Roy': 'All-rounder',
    'Varun Chakaravarthy': 'Bowler',
    'Harshit Rana': 'Bowler',
    
    # Add more players as needed
    'Virat Kohli': 'Batsman',
    'Rohit Sharma': 'Batsman',
    'Jasprit Bumrah': 'Bowler',
    'Hardik Pandya': 'All-rounder',
    'Arshdeep Singh': 'Bowler',
    'Yuzvendra Chahal': 'Bowler',
    'Yashasvi Jaiswal': 'Batsman',
    'Pat Cummins': 'Bowler',
    'Travis Head': 'Batsman',
    'Heinrich Klaasen': 'Wicket-keeper Batsman'
}


player_prices = {name: round(random.uniform(1.0, 18.0), 2) for name in player_roles.keys()}


def generate_player_stats():
    player_stats = {}
    for player, role in player_roles.items():
        price = player_prices.get(player, 5.0)  # Default price if not found
        
        # Base stats for all players
        stats = {
            'Matches': random.randint(5, 14),
            'Team': next((team for team, players in teams.items() if player in players), "Unknown"),
            'Role': role,
            'Price (Crores)': price
        }
        
        # Role-specific stats
        if 'Batsman' in role:
            matches = stats['Matches']
            avg_runs_per_match = random.randint(20, 50)
            total_runs = avg_runs_per_match * matches
            innings = random.randint(matches - 2, matches)
            
            stats.update({
                'Total Runs': total_runs,
                'Highest Score': random.randint(avg_runs_per_match, 100),
                'Innings': innings,
                'Not Outs': random.randint(0, 3),
                'Average': round(total_runs / max(innings, 1), 2),
                'Strike Rate': round(random.uniform(120.0, 160.0), 2),
                '50s': random.randint(0, 3),
                '100s': random.randint(0, 1),
                '4s': random.randint(total_runs // 10, total_runs // 5),
                '6s': random.randint(total_runs // 20, total_runs // 10)
            })
            
        if 'Bowler' in role:
            matches = stats['Matches']
            overs_per_match = random.randint(2, 4)
            total_overs = overs_per_match * matches
            
            stats.update({
                'Overs': total_overs,
                'Wickets': random.randint(matches // 2, matches * 2),
                'Economy': round(random.uniform(6.5, 9.5), 2),
                'Average': round(random.uniform(20.0, 35.0), 2),
                'Best Bowling': f"{random.randint(2, 5)}/{random.randint(10, 30)}",
                '3+ Wickets': random.randint(0, 2),
                'Maidens': random.randint(0, 2),
                'Dot Ball %': round(random.uniform(30.0, 45.0), 2)
            })
            
        if 'All-rounder' in role:
            matches = stats['Matches']
            # Add both batting and bowling stats for all-rounders
            avg_runs_per_match = random.randint(15, 30)
            total_runs = avg_runs_per_match * matches
            innings = random.randint(matches - 3, matches)
            
            overs_per_match = random.randint(2, 3)
            total_overs = overs_per_match * matches
            
            stats.update({
                # Batting stats
                'Total Runs': total_runs,
                'Highest Score': random.randint(avg_runs_per_match, 70),
                'Batting Average': round(total_runs / max(innings, 1), 2),
                'Strike Rate': round(random.uniform(125.0, 155.0), 2),
                '4s': random.randint(total_runs // 12, total_runs // 6),
                '6s': random.randint(total_runs // 25, total_runs // 15),
                
                # Bowling stats
                'Overs': total_overs,
                'Wickets': random.randint(matches // 3, matches),
                'Economy': round(random.uniform(7.0, 10.0), 2),
                'Bowling Average': round(random.uniform(25.0, 40.0), 2),
                'Best Bowling': f"{random.randint(1, 3)}/{random.randint(10, 25)}"
            })
        
        if 'Wicket-keeper' in role:
            stats.update({
                'Dismissals': random.randint(stats['Matches'] // 2, stats['Matches'] * 2),
                'Catches': random.randint(stats['Matches'] // 2, stats['Matches'] * 3 // 2),
                'Stumpings': random.randint(0, stats['Matches'] // 2)
            })
            
        # Add recent form (last 5 matches)
        recent_performances = []
        for _ in range(min(5, stats['Matches'])):
            if 'Batsman' in role or 'Wicket-keeper' in role:
                recent_performances.append(f"{random.randint(0, 60)} ({random.randint(10, 40)})")
            elif 'Bowler' in role:
                recent_performances.append(f"{random.randint(0, 3)}/{random.randint(15, 35)}")
            else:  # All-rounder
                recent_performances.append(f"{random.randint(0, 40)} & {random.randint(0, 2)}/{random.randint(15, 30)}")
        
        stats['Recent Form'] = recent_performances
        
        # Add head-to-head stats against current opposition
        if random.random() > 0.3:  # 70% chance of having head-to-head data
            h2h_matches = random.randint(1, 5)
            
            if 'Batsman' in role or 'Wicket-keeper' in role:
                stats['Head-to-Head'] = {
                    'Matches': h2h_matches,
                    'Runs': random.randint(h2h_matches * 15, h2h_matches * 35),
                    'Average': round(random.uniform(20.0, 50.0), 2),
                    'Strike Rate': round(random.uniform(125.0, 165.0), 2),
                    'Dismissals': random.randint(0, h2h_matches)
                }
            elif 'Bowler' in role:
                stats['Head-to-Head'] = {
                    'Matches': h2h_matches,
                    'Wickets': random.randint(0, h2h_matches * 2),
                    'Economy': round(random.uniform(6.0, 10.0), 2),
                    'Best Figures': f"{random.randint(1, 3)}/{random.randint(10, 30)}"
                }
            else:  # All-rounder
                stats['Head-to-Head'] = {
                    'Matches': h2h_matches,
                    'Runs': random.randint(h2h_matches * 10, h2h_matches * 25),
                    'Wickets': random.randint(0, h2h_matches),
                    'Performance Index': round(random.uniform(75.0, 125.0), 2)
                }
        
        player_stats[player] = stats
    
    return player_stats


player_stats = generate_player_stats()


cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']


model_files = {
    'Logistic Regression': 'models/logistic_regression.pkl',
    'Random Forest': 'models/random_forest.pkl',
    'SVM': 'models/svm.pkl',
    'Extra Trees': 'models/extra_trees.pkl',
    'XGBoost': 'models/xgboost.pkl',
    'AdaBoost': 'models/adaboost.pkl',
    'KNN': 'models/knn.pkl'
}


col1, col2 = st.columns([1.5, 2])

with col1:
    selected_model_name = st.selectbox('🏆 Select a Machine Learning Model', list(model_files.keys()))
    selected_model_file = model_files[selected_model_name]
    pipe = pickle.load(open(selected_model_file, 'rb'))

    batting_team = st.selectbox('⚾ Select the Batting Team', sorted(teams.keys()))
    bowling_team = st.selectbox('🎯 Select the Bowling Team', sorted(teams.keys()))
    selected_city = st.selectbox('📍 Select Host City', sorted(cities))
    toss_winner = st.selectbox('🪙 Select Toss Winner', [batting_team, bowling_team])
    toss_decision = st.radio('🔄 Toss Decision', ['Bat', 'Field'])

    target = st.number_input('🎯 Target Score', min_value=0)
    score = st.number_input('🏏 Current Score', min_value=0)
    overs = st.number_input('🔢 Overs Completed', min_value=0.0, step=0.1)
    wickets_out = st.number_input('❌ Wickets Out', min_value=0, max_value=10)

with col2:
    strike_batsman = st.selectbox('⚡ Strike Batsman', sorted(teams[batting_team]))
    strike_batsman_runs = st.number_input('🏃 Strike Batsman Runs', min_value=0)
    strike_batsman_balls = st.number_input('⚾ Strike Batsman Balls Faced', min_value=0)

    non_strike_batsman = st.selectbox('🛡️ Non-Strike Batsman', sorted(teams[batting_team]))
    non_strike_batsman_runs = st.number_input('🏃 Non-Strike Batsman Runs', min_value=0)
    non_strike_batsman_balls = st.number_input('⚾ Non-Strike Batsman Balls Faced', min_value=0)

    bowler = st.selectbox('🎯 Select Bowler', sorted(teams[bowling_team]))

    if st.button('📊 Predict Probability'):
        if score > target or wickets_out > 10 or non_strike_batsman_balls > 100 or strike_batsman_balls > 100:
            st.error("Invalid input values. Please check your inputs.")
        else:
            runs_left = target - score
            balls_left = 120 - int(overs * 6)
            wickets_left = 10 - wickets_out
            crr = score / overs if overs > 0 else 0
            rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
            strike_batsman_sr = (strike_batsman_runs * 100) / strike_batsman_balls if strike_batsman_balls > 0 else 0
            non_strike_batsman_sr = (non_strike_batsman_runs * 100) / non_strike_batsman_balls if non_strike_batsman_balls > 0 else 0

            input_df = pd.DataFrame({
                'batting_team': [batting_team],
                'bowling_team': [bowling_team],
                'city': [selected_city],
                'toss_winner': [toss_winner],
                'toss_decision': [toss_decision.lower()],
                'runs_left': [runs_left],
                'balls_left': [balls_left],
                'wickets': [wickets_left],
                'batsman_strike_rate': [strike_batsman_sr], 
                'non_striker_strike_rate': [non_strike_batsman_sr],  
                'total_runs_x': [target],
                'crr': [crr],
                'rrr': [rrr]
            })

            result = pipe.predict_proba(input_df)
            loss = result[0][0]
            win = result[0][1]

            st.success(f"🏏 **{batting_team}** Winning Probability: **{round(win * 100)}%**")
            st.error(f"🎯 **{bowling_team}** Winning Probability: **{round(loss * 100)}%**")

            st.markdown("## 📊 Match Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🏏 Runs Left", runs_left)
                st.metric("📊 Current Run Rate (CRR)", round(crr, 2))
            with col2:
                st.metric("🎯 Required Run Rate (RRR)", round(rrr, 2))
                st.metric("⚾ Balls Left", balls_left)
            with col3:
                st.metric("❌ Wickets Remaining", wickets_left)
                st.metric("🔢 Overs Remaining", round(balls_left / 6, 1))

            
            st.markdown("## 🏏 Current Players Statistics")
            
           
            tabs = st.tabs(["Strike Batsman", "Non-Strike Batsman", "Bowler"])
            
            with tabs[0]:
                if strike_batsman in player_stats:
                    st.subheader(f"{strike_batsman} - {player_stats[strike_batsman]['Role']}")
                    
                  
                    st.markdown("### Current Innings")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Runs", strike_batsman_runs)
                    with col2:
                        st.metric("Balls", strike_batsman_balls)
                    with col3:
                        sr = (strike_batsman_runs * 100) / strike_batsman_balls if strike_batsman_balls > 0 else 0
                        st.metric("Strike Rate", round(sr, 2))
                    
                  
                    st.markdown("### Tournament Statistics")
                    stats = player_stats[strike_batsman]
                    
                   
                    if 'Batsman' in stats['Role'] or 'Wicket-keeper' in stats['Role']:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Matches", stats.get('Matches', 0))
                            st.metric("4s", stats.get('4s', 0))
                        with col2:
                            st.metric("Runs", stats.get('Total Runs', 0))
                            st.metric("6s", stats.get('6s', 0))
                        with col3:
                            st.metric("Average", stats.get('Average', 0))
                            st.metric("50s", stats.get('50s', 0))
                        with col4:
                            st.metric("Strike Rate", stats.get('Strike Rate', 0))
                            st.metric("100s", stats.get('100s', 0))
                    
                   
                    if 'Recent Form' in stats:
                        st.markdown("### Recent Form (Last 5 Matches)")
                        st.write(", ".join(stats['Recent Form']))
                    
                  
                    if 'Head-to-Head' in stats:
                        st.markdown(f"### Head-to-Head vs {bowling_team}")
                        h2h = stats['Head-to-Head']
                        st.json(h2h)
            
            with tabs[1]:
                if non_strike_batsman in player_stats:
                    st.subheader(f"{non_strike_batsman} - {player_stats[non_strike_batsman]['Role']}")
                  
                    st.markdown("### Current Innings")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Runs", non_strike_batsman_runs)
                    with col2:
                        st.metric("Balls", non_strike_batsman_balls)
                    with col3:
                        sr = (non_strike_batsman_runs * 100) / non_strike_batsman_balls if non_strike_batsman_balls > 0 else 0
                        st.metric("Strike Rate", round(sr, 2))
                    
                  
                    st.markdown("### Tournament Statistics")
                    stats = player_stats[non_strike_batsman]
                    
                   
                    if 'Batsman' in stats['Role'] or 'Wicket-keeper' in stats['Role']:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Matches", stats.get('Matches', 0))
                            st.metric("4s", stats.get('4s', 0))
                        with col2:
                            st.metric("Runs", stats.get('Total Runs', 0))
                            st.metric("6s", stats.get('6s', 0))
                        with col3:
                            st.metric("Average", stats.get('Average', 0))
                            st.metric("50s", stats.get('50s', 0))
                        with col4:
                            st.metric("Strike Rate", stats.get('Strike Rate', 0))
                            st.metric("100s", stats.get('100s', 0))
                    
                    
                    if 'Recent Form' in stats:
                        st.markdown("### Recent Form (Last 5 Matches)")
                        st.write(", ".join(stats['Recent Form']))
                    
                    
                    if 'Head-to-Head' in stats:
                        st.markdown(f"### Head-to-Head vs {bowling_team}")
                        h2h = stats['Head-to-Head']
                        st.json(h2h)
            
            with tabs[2]:
                if bowler in player_stats:
                    st.subheader(f"{bowler} - {player_stats[bowler]['Role']}")
                    
                 
                    st.markdown("### Tournament Statistics")
                    stats = player_stats[bowler]
                    
                  
                    if 'Bowler' in stats['Role']:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Matches", stats.get('Matches', 0))
                            st.metric("Economy", stats.get('Economy', 0))
                        with col2:
                            st.metric("Overs", stats.get('Overs', 0))
                            st.metric("Average", stats.get('Average', 0))
                        with col3:
                            st.metric("Wickets", stats.get('Wickets', 0))
                            st.metric("3+ Wickets", stats.get('3+ Wickets', 0))
                        with col4:
                            st.metric("Best Bowling", stats.get('Best Bowling', "0/0"))
                            st.metric("Maidens", stats.get('Maidens', 0))
                    elif 'All-rounder' in stats['Role']:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Overs", stats.get('Overs', 0))
                            st.metric("Runs", stats.get('Total Runs', 0))
                        with col2:
                            st.metric("Wickets", stats.get('Wickets', 0))
                            st.metric("Batting Average", stats.get('Batting Average', 0))
                        with col3:
                            st.metric("Economy", stats.get('Economy', 0))
                            st.metric("Strike Rate", stats.get('Strike Rate', 0))
                        with col4:
                            st.metric("Best Bowling", stats.get('Best Bowling', "0/0"))
                            st.metric("Bowling Average", stats.get('Bowling Average', 0))
                    
                    if 'Recent Form' in stats:
                        st.markdown("### Recent Form (Last 5 Matches)")
                        st.write(", ".join(stats['Recent Form']))
                    
                    
                    if 'Head-to-Head' in stats:
                        st.markdown(f"### Head-to-Head vs {batting_team}")
                        h2h = stats['Head-to-Head']
                        st.json(h2h)
            
          
            st.markdown("### 📈 Match Progress")
            st.progress(min(score / target, 1.0), text=f"Score Progress: {score}/{target}")
            st.progress(min((120 - balls_left) / 120, 1.0), text=f"Overs Progress: {overs}/20")

            
            st.markdown("### 📊 Winning Probability")
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(["Batting Team", "Bowling Team"], [win * 100, loss * 100], color=['green', 'red'])
            ax.set_ylabel("Winning Probability (%)")
            ax.set_ylim(0, 100)
            for i, v in enumerate([win * 100, loss * 100]):
                ax.text(i, v + 1, f"{round(v)}%", ha='center')
            st.pyplot(fig)