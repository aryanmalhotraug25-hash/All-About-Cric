import pandas as pd
import os
import pickle
import streamlit as st

# ==========================================
# DATA LOADING & CLEANING
# ==========================================

@st.cache_data
def load_and_clean_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '..', 'data')
    
    matches = pd.read_csv(os.path.join(data_path, 'matches.csv'))
    deliveries = pd.read_csv(os.path.join(data_path, 'deliveries.csv'))
    
    team_name_changes = {
        'Delhi Daredevils': 'Delhi Capitals',
        'Kings XI Punjab': 'Punjab Kings',
        'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
        'Rising Pune Supergiants': 'Rising Pune Supergiant'
    }
    
    matches['team1_std'] = matches['team1'].replace(team_name_changes)
    matches['team2_std'] = matches['team2'].replace(team_name_changes)
    matches['toss_winner_std'] = matches['toss_winner'].replace(team_name_changes)
    matches['winner_std'] = matches['winner'].replace(team_name_changes)
    
    deliveries['batting_team_std'] = deliveries['batting_team'].replace(team_name_changes)
    deliveries['bowling_team_std'] = deliveries['bowling_team'].replace(team_name_changes)
    
    return matches, deliveries


# ==========================================
# ML MODEL LOADING
# ==========================================

@st.cache_resource
def load_model():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_path = os.path.join(script_dir, '..', 'models')
    
    with open(os.path.join(models_path, 'score_predictor.pkl'), 'rb') as f:
        model = pickle.load(f)
    
    with open(os.path.join(models_path, 'metadata.pkl'), 'rb') as f:
        metadata = pickle.load(f)
    
    return model, metadata


def predict_score(model, batting_team, bowling_team, venue,
                  current_runs, current_wickets, overs_decimal,
                  runs_last_5, wickets_last_5):
    
    # RULE 1: All out
    if current_wickets >= 10:
        return current_runs
    
    # RULE 2: Innings completed
    if overs_decimal >= 20:
        return current_runs
    
    # Calculate features
    crr = round(current_runs / overs_decimal, 2) if overs_decimal > 0 else 0
    overs_left = round(20 - overs_decimal, 2)
    wickets_left = 10 - current_wickets
    momentum = round(runs_last_5 - (crr * 5), 2)
    
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'venue': [venue],
        'current_runs': [current_runs],
        'wickets_left': [wickets_left],
        'crr': [crr],
        'overs_left': [overs_left],
        'momentum': [momentum],
        'wickets_last_5': [wickets_last_5]
    })
    
    predicted = int(model.predict(input_df)[0])
    
    # ===== CRICKET-AWARE MANUAL CAP =====
    # Tail-enders rarely add many runs
    if current_wickets == 9:
        max_additional = 15   # last man + tail, very limited
        predicted = min(predicted, current_runs + max_additional)
    
    elif current_wickets == 8:
        max_additional = 25   # tail with one resource
        predicted = min(predicted, current_runs + max_additional)
    
    elif current_wickets == 7:
        max_additional = 45   # lower order, some resistance
        predicted = min(predicted, current_runs + max_additional)
    
    # Never less than current runs
    return max(predicted, current_runs)


# ==========================================
# SEASON ANALYSIS
# ==========================================

def get_champions(matches):
    matches_sorted = matches.sort_values('date')
    finals = matches_sorted.groupby('season').tail(1)
    champions = finals[['season', 'date', 'team1_std', 'team2_std', 'winner_std']].reset_index(drop=True)
    champions.columns = ['Season', 'Final Date', 'Team 1', 'Team 2', 'Champion']
    return champions

def get_matches_per_season(matches):
    return matches['season'].value_counts().sort_index()


# ==========================================
# TEAM ANALYSIS
# ==========================================

def get_team_stats(matches):
    total_wins = matches['winner_std'].value_counts()
    matches_played = pd.concat([matches['team1_std'], matches['team2_std']]).value_counts()
    
    team_stats = pd.DataFrame({
        'Matches': matches_played,
        'Wins': total_wins
    }).fillna(0)
    
    team_stats['Losses'] = team_stats['Matches'] - team_stats['Wins']
    team_stats['Win %'] = (team_stats['Wins'] / team_stats['Matches'] * 100).round(2)
    team_stats = team_stats.astype({'Matches': int, 'Wins': int, 'Losses': int})
    return team_stats.sort_values('Win %', ascending=False)

def get_single_team_stats(matches, team):
    team_matches = matches[
        (matches['team1_std'] == team) | (matches['team2_std'] == team)
    ]
    wins = team_matches[team_matches['winner_std'] == team].shape[0]
    total = team_matches.shape[0]
    losses = total - wins
    win_pct = (wins / total * 100) if total > 0 else 0
    return total, wins, losses, win_pct


# ==========================================
# PLAYER ANALYSIS
# ==========================================

def get_top_batters(deliveries, n=10):
    return deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(n)

def get_top_bowlers(deliveries, n=10):
    bowler_dismissals = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
    wicket_data = deliveries[deliveries['dismissal_kind'].isin(bowler_dismissals)]
    return wicket_data.groupby('bowler').size().sort_values(ascending=False).head(n)

def get_top_sixes(deliveries, n=10):
    sixes = deliveries[deliveries['batsman_runs'] == 6]
    return sixes.groupby('batter').size().sort_values(ascending=False).head(n)

def get_top_fours(deliveries, n=10):
    fours = deliveries[deliveries['batsman_runs'] == 4]
    return fours.groupby('batter').size().sort_values(ascending=False).head(n)

def get_top_pom(matches, n=10):
    return matches['player_of_match'].value_counts().head(n)

def get_orange_cap_per_season(matches, deliveries):
    merged = deliveries.merge(matches[['id', 'season']], left_on='match_id', right_on='id')
    season_runs = merged.groupby(['season', 'batter'])['batsman_runs'].sum().reset_index()
    orange_cap = season_runs.loc[season_runs.groupby('season')['batsman_runs'].idxmax()]
    orange_cap = orange_cap.reset_index(drop=True)
    orange_cap.columns = ['Season', 'Player', 'Runs']
    return orange_cap

def get_purple_cap_per_season(matches, deliveries):
    bowler_dismissals = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
    merged = deliveries.merge(matches[['id', 'season']], left_on='match_id', right_on='id')
    wickets = merged[merged['dismissal_kind'].isin(bowler_dismissals)]
    season_wickets = wickets.groupby(['season', 'bowler']).size().reset_index(name='wickets')
    purple_cap = season_wickets.loc[season_wickets.groupby('season')['wickets'].idxmax()]
    purple_cap = purple_cap.reset_index(drop=True)
    purple_cap.columns = ['Season', 'Player', 'Wickets']
    return purple_cap

def get_top_keepers(deliveries, n=10):
    keepers = deliveries[deliveries['dismissal_kind'] == 'stumped']['fielder'].dropna().unique()
    keeper_dismissals = deliveries[
        (deliveries['fielder'].isin(keepers)) &
        (deliveries['dismissal_kind'].isin(['caught', 'stumped']))
    ]
    return keeper_dismissals.groupby('fielder').size().sort_values(ascending=False).head(n)


# ==========================================
# VENUE ANALYSIS
# ==========================================

def get_top_venues(matches, n=10):
    return matches['venue'].value_counts().head(n)

def get_highest_scoring_venues(matches, deliveries, n=10, min_matches=10):
    first_innings = deliveries[deliveries['inning'] == 1]
    runs_per_match = first_innings.groupby('match_id')['total_runs'].sum().reset_index()
    runs_with_venue = runs_per_match.merge(matches[['id', 'venue']], left_on='match_id', right_on='id')
    
    venue_avg = runs_with_venue.groupby('venue').agg(
        avg_score=('total_runs', 'mean'),
        match_count=('total_runs', 'count')
    ).round(2)
    
    venue_avg = venue_avg[venue_avg['match_count'] >= min_matches]
    return venue_avg['avg_score'].sort_values(ascending=False).head(n)


# ==========================================
# HEAD-TO-HEAD
# ==========================================

def get_head_to_head(matches, team_a, team_b):
    h2h = matches[
        ((matches['team1_std'] == team_a) & (matches['team2_std'] == team_b)) |
        ((matches['team1_std'] == team_b) & (matches['team2_std'] == team_a))
    ]
    total = h2h.shape[0]
    team_a_wins = h2h[h2h['winner_std'] == team_a].shape[0]
    team_b_wins = h2h[h2h['winner_std'] == team_b].shape[0]
    no_result = total - team_a_wins - team_b_wins
    return total, team_a_wins, team_b_wins, no_result