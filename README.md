# IPL Win Predictor and Strategy Analyser

**Live demo:** https://ipl-win-predictor-pqvkqrpy4fedzvputbk7a9.streamlit.app

Analysed 17 seasons of IPL data (1,090 matches, 260,000+ deliveries) to build 
a live win probability predictor, venue intelligence dashboard, and player 
form tracker using Python, SQL, and scikit-learn.

## Key findings
- Wickets remaining is the strongest predictor of match outcome (logistic 
  regression coefficient +0.56)
- At M Chinnaswamy Stadium, teams batting first after winning the toss win 
  only 0% of matches across 14 games — far below the expected 50%

## Tech stack
Python, pandas, scikit-learn, Streamlit, Plotly, SQLite

## Model
Logistic Regression trained on 125,000+ second-innings ball states. 
Features: overs remaining, wickets left, runs needed, required run rate, 
current run rate, venue.
