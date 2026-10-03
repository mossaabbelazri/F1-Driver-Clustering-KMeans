import pandas as pd

qualifying = pd.read_csv('cleaned/modern_qualifying.csv')
subset = qualifying[qualifying['driverId'].isin([1, 830])][['raceId', 'driverId', 'q1', 'q2', 'q3']]
subset.to_csv('cleaned/qualif_hamilton_verstappen.csv', index=False)

# Nettoyage des valeurs spéciales dans q3
subset['q3'] = subset['q3'].replace([-1, '\\N', '/N', ''], pd.NA)

# Calcul du nombre de Q3 atteints pour chaque pilote
q3_count = subset.groupby('driverId')['q3'].count()
print('Nombre de Q3 atteints :')
for driver_id, count in q3_count.items():
    if driver_id == 1:
        print(f"Lewis Hamilton (driverId=1) : {count}")
    elif driver_id == 830:
        print(f"Max Verstappen (driverId=830) : {count}") 