import pandas as pd
import numpy as np

from os import listdir
from os.path import isdir, isfile, join

def load_data( folder ):
    
    files = [f for f in listdir(folder) if isfile(join(folder, f)) and 'Playoff' not in f]
    df = pd.read_csv(join(folder, files[0]))
    for f in files[1:]:
        df = pd.concat((df, pd.read_csv(join(folder, f))), axis=0)
    
    df.reset_index(drop=True, inplace=True)
    df.drop(df.index[~df['Status'].isin(['Active'])], inplace=True)
    df.sort_values(by='gameID', axis=0, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df.rename(columns={'FT': 'FTM'}, inplace=True)
    df.reset_index(drop=True, inplace=True)    
    return df

def construct_game_df(df, game_cols):
    df_home_away = df.groupby(['gameID','Home']).first().loc[:,game_cols]
    unique_games = df_home_away.index.levels[0]
    tuples = (unique_games, 1)
    df_home_away = df_home_away.loc[tuples,:]
    df_home_away.index = df_home_away.index.droplevel(1)
    df_games = df_home_away
    return df_games

def get_score_columns(df):
    df['HomeID'] = df.teamid.values
    df['AwayID'] = df.OpponentID.values
    df['HomeScore_Vegas'] = df['ProjectedTotal'].values / 2 - df['Spread'].values / 2
    df['AwayScore_Vegas'] = df['ProjectedTotal'].values - df['HomeScore_Vegas'].values
    df.loc[df['season'].isin([201415, 201516]),'HomeScore_Vegas'] = 105
    df.loc[df['season'].isin([201415, 201516]),'AwayScore_Vegas'] = 103
    return df

def get_team_games( df ):
    teams = df.HomeID.unique()
    team_games = {}
    for team in teams:
        team_games[team] = {}
        team_games[team]['home'] = df[df['HomeID'].isin([team])].index.to_numpy()
        team_games[team]['away'] = df[df['AwayID'].isin([team])].index.to_numpy()
        team_games[team]['all'] = np.sort(np.append(team_games[team]['home'], team_games[team]['away']))
    return team_games

def convert_date_to_days_ago(df, games_dict):
    games = df.index.unique()
    home_days_ago_home = np.zeros((games.shape[0]))
    home_days_ago_away = np.zeros((games.shape[0]))
    away_days_ago_home = np.zeros((games.shape[0]))
    away_days_ago_away = np.zeros((games.shape[0]))
    for i, game in enumerate(games):
        homeID = df.loc[game,'HomeID']
        awayID = df.loc[game,'AwayID']
        if i > 50:
            home_last_home_game_date = df.loc[games_dict[homeID]['home'][np.where(games_dict[homeID]['home']<game)[0]][-1],'date']
            home_last_away_game_date = df.loc[games_dict[homeID]['away'][np.where(games_dict[homeID]['away']<game)[0]][-1],'date']
            away_last_home_game_date = df.loc[games_dict[awayID]['home'][np.where(games_dict[awayID]['home']<game)[0]][-1],'date']
            away_last_away_game_date = df.loc[games_dict[awayID]['away'][np.where(games_dict[awayID]['away']<game)[0]][-1],'date']
        else:
            home_last_home_game_date = df.loc[games[0],'date']
            home_last_away_game_date = df.loc[games[0],'date']
            away_last_home_game_date = df.loc[games[0],'date']
            away_last_away_game_date = df.loc[games[0],'date']
        current_date = df.loc[game,'date']
        home_days_ago_home[i] = (current_date - home_last_home_game_date).value / 1e9 / 3600 / 24
        home_days_ago_away[i] = (current_date - home_last_away_game_date).value / 1e9 / 3600 / 24
        away_days_ago_home[i] = (current_date - away_last_home_game_date).value / 1e9 / 3600 / 24
        away_days_ago_away[i] = (current_date - away_last_away_game_date).value / 1e9 / 3600 / 24
    df['Home_days_ago_home'] = np.minimum(10, home_days_ago_home)
    df['Home_days_ago_away'] = np.minimum(10, home_days_ago_away)
    df['Away_days_ago_home'] = np.minimum(10, away_days_ago_home)
    df['Away_days_ago_away'] = np.minimum(10, away_days_ago_away)
    return df

def points_calc(df, fantasy_points = {'SecondsPlayed' : 0,
                                      'Two_PM' : 2,
                                      'Two_PA' : 0,
                                      'Three_PM' : 3.5,
                                      'Three_PA' : 0,
                                      'FTM' : 1,
                                      'FTA' : 0,
                                      'ORB' : 1.25,
                                      'DRB' : 1.25,
                                      'AST' : 1.5,
                                      'STL' : 2,
                                      'BLK' : 2,
                                      'TOV' : -0.5,
                                      'PFouls' : 0,
                                      'PlusMinus' : 0,
                                      'Double-double' : 1.5,
                                      'Triple-double' : 3}):
    '''
    Returns a numpy array of the fantasy points from the input
    of the stats.
    Inputs:
    df - dataframe with columns of data required to calculate the fantasy points
    fantasy_points - dict giving the value of each point
    '''
    points = {'Two_PM' : 2, 'Three_PM' : 3, 'FTM' : 1}
    points_cols = list(points.keys())
    points_vec = np.array(list(points.values())).reshape(-1, 1)
    df['point_cliff'] = df[points_cols].values @ points_vec >= 10

    rebs = {'ORB' : 1, 'DRB' : 1}
    rebs_cols = list(rebs.keys())
    rebs_vec = np.array(list(rebs.values())).reshape(-1, 1)
    df['reb_cliff'] = df[rebs_cols].values @ rebs_vec >= 10

    df['ast_cliff'] = df['AST'].values >= 10

    df['stl_cliff'] = df['STL'].values >= 10

    df['blk_cliff'] = df['BLK'].values >= 10

    df['double_digits'] = df[['point_cliff', 'reb_cliff', 'ast_cliff', 'stl_cliff', 'blk_cliff']].sum(axis=1)

    df['Double-double'] = (df['double_digits'] >= 2) + 0
    df['Triple-double'] = (df['double_digits'] >= 3) + 0

    fantasy_cols = list(fantasy_points.keys())
    fantasy_vec = np.array(list(fantasy_points.values())).reshape(-1, 1)
    
    return df[fantasy_cols].values @ fantasy_vec