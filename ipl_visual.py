# Importing required libraries
import pandas as pd
import matplotlib.pyplot as plt

# Path of File
path = r'/home/abhishek/Data Analysis/Datasets/ipl.csv'

# Reading data in Data Frame
df = pd.read_csv(path)

# create column `year` which stores the year in which match was played
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['season'] = df['year'] - 2007
# Plot the wins gained by teams across all seasons
df2 = df.drop_duplicates(['match_code'])
df_wins = df.drop_duplicates(['match_code'])
df_wins = df_wins.groupby(['winner'])['match_code'].nunique()
df_wins.sort_values(ascending=True).plot(kind='barh')
plt.xlabel('Wins')

# Plot Number of matches played by each team through all seasons
temp_data = pd.melt(df2, id_vars=['match_code', 'year'], value_vars= ['team1', 'team2'])
matches_played = temp_data.value.value_counts()
plt.figure(figsize=(12,6))
matches_played.plot(x= matches_played.index, y = matches_played, kind = 'bar', title= 'No. of matches played across 9 seasons')
plt.xticks(rotation = 'vertical')
plt.show()

# Top bowlers through all seasons
df_bowler_runs = df.groupby('bowler')[['total']].sum()
df_bowler_runs = df_bowler_runs.reset_index()
df_bowler_overs = df.groupby('bowler')[['delivery']].sum()/6
df_bowler_overs = df_bowler_overs.reset_index()
df_merged = pd.merge(left=df_bowler_overs, right=df_bowler_runs, on='bowler')
df_merged.rename(columns={'total': 'Total Runs', 'delivery': 'Overs Bowled'}, inplace=True)
df_merged['Economy'] = df_merged['Total Runs']/df_merged['Overs Bowled']
df_merged.set_index(keys='bowler',inplace=True)
df_merged[['Economy']].head(15).sort_values(by='Economy', ascending=False).plot(kind='barh')
plt.ylabel('Bowlers')
plt.xlabel('Economy')
plt.title('Top 15 Bowlers')


# How did the different pitches behave? What was the average score for each stadium?
total_runs_scored_venue_wise = df.groupby('venue')[['total']].sum()
total_matches_played_venue_wise = df2.groupby('venue')[['match_code']].count()
df_venue_run_avg = total_runs_scored_venue_wise['total']/total_matches_played_venue_wise['match_code']
df_venue_run_avg.sort_values(ascending=True).plot(kind='barh', legend=None)
plt.title('Avg Score Venue Wise')
plt.ylabel('Venue')
plt.xlabel('Avg Runs Scored')

# Types of Dismissal and how often they occur
types_of_dismissal = df['wicket_kind'].value_counts()
no_of_bowls = df['delivery'].count()
avg_dismissal_frequency = types_of_dismissal/no_of_bowls
avg_dismissal_frequency.plot(kind='bar')
plt.ylim(0, 0.03)

# Plot no. of boundaries across IPL seasons
no_of_boundaries = df[(df['runs']==4) | (df['runs']==6)]
no_of_boundaries['runs'].value_counts().plot(kind='bar')
plt.title('No of boundaries across all seasons')
plt.xticks(rotation='horizontal')
plt.xlabel('Boundary Type')
plt.ylabel('Count')
plt.show()

# Average statistics across all seasons

per_match_data = df.drop_duplicates(subset='match_code', keep='first').reset_index(drop=True)

total_runs_per_season = df.groupby('year')['total'].sum()
balls_delivered_per_season = df.groupby('year')['delivery'].count()
no_of_match_played_per_season = per_match_data.groupby('year')['match_code'].count()
avg_balls_per_match = balls_delivered_per_season/no_of_match_played_per_season
avg_runs_per_match = total_runs_per_season/no_of_match_played_per_season
avg_runs_per_ball = total_runs_per_season/balls_delivered_per_season
avg_data = pd.DataFrame([no_of_match_played_per_season, avg_runs_per_match, avg_balls_per_match, avg_runs_per_ball])
avg_data.index =['No.of Matches', 'Average Runs per Match', 'Average balls bowled per match', 'Average runs per ball']
avg_data.T.plot(kind='bar', figsize = (12,10), colormap = 'coolwarm')
plt.xlabel('Season')
plt.ylabel('Average')
plt.legend(loc=9,ncol=4);