import pandas as pd

qualifying = pd.read_csv('cleaned/modern_qualifying.csv')
print(qualifying[qualifying['driverId'].isin([1, 830])][['raceId', 'driverId', 'q1', 'q2', 'q3']].head(20))