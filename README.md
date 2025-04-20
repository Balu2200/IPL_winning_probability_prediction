# IPL Win Predictor

## Project Description

The **IPL Win Predictor** is an interactive web application built using Streamlit that predicts the winning probability of a cricket team in an Indian Premier League (IPL) matches . The application leverages machine learning models to provide accurate predictions and displays detailed player statistics, match progress, and visualizations to enhance user experience.

### Key Features
- **Team and Player Selection**: Users can select batting and bowling teams, the host city, toss winner, and toss decision, along with specific players (strike batsman, non-strike batsman, and bowler).
- **Match Inputs**: Input current match conditions such as target score, current score, overs completed, wickets out, and individual player performance (runs scored, balls faced).
- **Machine Learning Models**: Choose from multiple pre-trained models (e.g., Logistic Regression, Random Forest, XGBoost) to predict the winning probability of the batting and bowling teams.
- **Player Statistics**: Displays comprehensive player stats, including tournament performance, recent form, and head-to-head statistics against the opposing team.
- **Visualizations**: Interactive charts and progress bars to visualize match progress and winning probabilities.
- **Error Handling**: Validates user inputs to ensure realistic match scenarios (e.g., score not exceeding target, wickets not exceeding 10).
- **Responsive UI**: A user-friendly interface with a modern design, including custom styling, tabs for player stats, and metric displays.

### Technologies Used
- **Python**: Core programming language for the application.
- **Streamlit**: Framework for building the interactive web interface.
- **Pandas**: For data manipulation and creating input dataframes for predictions.
- **Matplotlib**: For generating visualizations like bar charts for winning probabilities.
- **Pickle**: For loading pre-trained machine learning models.
- **Random**: For generating simulated player statistics.

### How It Works
1. **User Input**: Users provide match details such as batting and bowling teams, city, toss outcome, current score, overs, wickets, and player-specific data (runs, balls faced).
2. **Data Processing**: The app calculates derived metrics like runs left, balls left, current run rate (CRR), required run rate (RRR), and batsman strike rates.
3. **Prediction**: A selected machine learning model processes the input data to predict the winning probabilities for both teams.
4. **Statistics and Visuals**: The app displays player stats (e.g., runs, wickets, recent form), match metrics (e.g., CRR, RRR), and visualizations (e.g., progress bars, probability charts).
5. **Player Stats Generation**: Simulated player statistics are generated based on their roles (batsman, bowler, all-rounder, wicket-keeper) and include metrics like total runs, wickets, strike rate, and head-to-head performance.

### Installation and Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ipl-win-predictor.git
   cd ipl-win-predictor
   ```

2. **Install Dependencies**:
   Ensure Python 3.8+ is installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Requirements File**:
   Create a `requirements.txt` with the following:
   ```
   streamlit==1.27.0
   pandas==2.0.3
   matplotlib==3.7.2
   ```

4. **Model Files**:
   Ensure the pre-trained model files (e.g., `logistic_regression.pkl`, `random_forest.pkl`) are placed in a `models/` directory within the project folder. These files should contain serialized machine learning pipelines trained on IPL match data.

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

6. **Access the App**:
   Open your browser and navigate to `http://localhost:8501` to use the application.

### File Structure
```
ipl-win-predictor/
├── app.py              # Main Streamlit application file
├── models/             # Directory containing pre-trained model files
│   ├── logistic_regression.pkl
│   ├── random_forest.pkl
│   ├── GradientBoost.pkl
│   ├── AdaBoost.pkl
│   ├── svm.pkl
│   ├── XGBoost.pkl
│   ├── DecisionTree.pkl
├── requirements.txt    # List of Python dependencies
└── README.md           # Project documentation
```

### Usage
1. Launch the app using `streamlit run app.py`.
2. Select a machine learning model from the dropdown.
3. Input match details, including teams, city, toss, scores, overs, wickets, and player stats.
4. Click the "Predict Probability" button to view the winning probabilities for both teams.
5. Explore player statistics, match metrics, and visualizations in the app interface.

### Assumptions and Limitations
- **Model Dependency**: The app assumes pre-trained model files are available in the `models/` directory. These models must be trained on relevant IPL match data.
- **Simulated Stats**: Player statistics are generated randomly within realistic ranges for demonstration purposes. In a production environment, real player data should be integrated.
- **Input Validation**: The app includes basic input validation (e.g., wickets ≤ 10, score ≤ target), but additional edge cases may need handling.
- **Static Data**: The list of teams, players, and cities is hardcoded. For a dynamic application, these could be sourced from a database or API.


### License
This project is licensed under the MIT License. See the `LICENSE` file for details.

### Contact
For questions or feedback, please contact [your-email@example.com](mailto:your-email@example.com).
