import pandas as pd
import numpy as np
import os

# 1. Charger les fichiers CSV principaux
races = pd.read_csv('archive/races.csv')
results = pd.read_csv('archive/results.csv')
drivers = pd.read_csv('archive/drivers.csv')
constructors = pd.read_csv('archive/constructors.csv')
circuits = pd.read_csv('archive/circuits.csv')

# 2. Filter les courses de 2014 à 2024
races_modern = races[(races['year'] >= 2014) & (races['year'] <= 2024)]
modern_race_ids = races_modern['raceId'].unique()

#3. Filtrer les résultats pour ces courses
results_modern = results[results['raceId'].isin(modern_race_ids)]


#Nettoyage des colonnes time et milliseconds dans results
for col in ['time', 'milliseconds']:
    if col in results_modern.columns:
        results_modern[col] = results_modern[col].replace(['\\N', '/N'], -1)
        #Pour milliseconds, s'assurer que c'est bien numérique
        if col == 'milliseconds':
            results_modern[col] = pd.to_numeric(results_modern[col], errors='coerce').fillna(-1)
            
#4. Filtrer les pilotes ayant participé à ces courses
modern_driver_ids = results_modern['driverId'].unique()
drivers_modern = drivers[drivers['driverId'].isin(modern_driver_ids)]

#5. Filtrer les constructeurs ayant participé à ces courses
modern_constructor_ids = results_modern['constructorId'].unique()
constructors_modern = constructors[constructors['constructorId'].isin(modern_constructor_ids)]            

# Nettoyage des colonnes time et milliseconds dans results_modern
for col in ['time', 'milliseconds']:
    if col in results_modern.columns:
        results_modern[col] = results_modern[col].replace(['\\N', '/N'], -1)
        # Pour milliseconds, s'assurer que c'est bien numérique
        if col == 'milliseconds':
            results_modern[col] = pd.to_numeric(results_modern[col], errors='coerce').fillna(-1)

# 4. Filtrer les pilotes ayant participé à ces courses
modern_driver_ids = results_modern['driverId'].unique()
drivers_modern = drivers[drivers['driverId'].isin(modern_driver_ids)]

# 5. Filtrer les constructeurs ayant participé à ces courses
modern_constructor_ids = results_modern['constructorId'].unique()
constructors_modern = constructors[constructors['constructorId'].isin(modern_constructor_ids)]

#6. Filtrer les circuits utilisés 
modern_circuit_ids = races_modern['circuitId'].unique()
circuits_modern = circuits[circuits['circuitId'].isin(modern_circuit_ids)]

#7. Créer le dossier cleaned/ 
os.makedirs('cleaned', exist_ok=True)

#8. Sauvegarder les nouveaux fichiers nettoyés principaux
races_modern.to_csv('cleaned/races_modern.csv', index=False)
results_modern.to_csv('cleaned/results_modern.csv', index=False)
drivers_modern.to_csv('cleaned/drivers_modern.csv', index=False)
constructors_modern.to_csv('cleaned/constructors_modern.csv', index=False)
circuits_modern.to_csv('cleaned/circuits_modern.csv', index=False)

#9. Filtrer les autres fichiers selon raceId
other_files = [
    'lap_times.csv',
    'pit_stops.csv',
    'qualifying.csv',
    'sprint_results.csv',
    'driver_standings.csv',
    'constructor_standings.csv',
    'constructor_results.csv'
]
for fname in other_files:
    path = f'archive/{fname}'
    if os.path.exists(path):
        df = pd.read_csv(path)
        if 'raceId' in df.columns:
            df_modern = df[df['raceId'].isin(modern_race_ids)]
            # Nettoyage spécifique pour qualifying
            if fname == 'qualifying.csv':
                for col in ['q1', 'q2', 'q3']:
                    if col in df_modern.columns:
                        df_modern[col] = df_modern[col].replace(['\\N', '/N'], -1)
            df_modern.to_csv(f'cleaned/modern_{fname}', index=False)
                        
#10. Filtrer seasons.csv
seasons_path = 'archive/seasons.csv'
if os.path.exists(seasons_path):
    seasons = pd.read_csv(seasons_path)
    if 'year' in seasons.columns:
        seasons_modern =seasons[(seasons['year'] >= 2014) & (seasons['year'] <= 2024)]
        seasons_modern.to_csv('cleaned/modern_seasons.csv', index=False)

#11. Copier status.csv sans filtrage 
status_path = 'archive/status.csv'
if os.path.exists(status_path):
    status = pd.read_csv(status_path)
    status.to_csv('cleaned/modern_status.csv', index=False)
    
print('Nettoyage terminé. Tous les fichiers filtrés et nettoyés sont dans le dossier cleaned/.')    
