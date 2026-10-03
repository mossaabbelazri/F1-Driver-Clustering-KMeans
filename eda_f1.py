import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les fichiers nettoyés
races = pd.read_csv('cleaned/races_modern.csv')
results = pd.read_csv('cleaned/results_modern.csv')
drivers = pd.read_csv('cleaned/drivers_modern.csv')
constructors = pd.read_csv('cleaned/constructors_modern.csv')
circuits = pd.read_csv('cleaned/circuits_modern.csv')

# Statistiques générales
print('--- Statistiques générales ---')
print(f"Nombre de courses (2014-2024) : {len(races)}")
print(f"Nombre de pilotes : {len(drivers)}")
print(f"Nombre de constructeurs : {len(constructors)}")
print(f"Nombre de circuits : {len(circuits)}")
print(f"Nombre total de résultats : {len(results)}")

# Nombre moyen de courses par saison
grouped = races.groupby('year').size()
print(f"Nombre moyen de courses par saison : {grouped.mean():.2f}")

# Top pilotes par nombre de victoires
victoires = results[results['positionOrder'] == 1]['driverId'].value_counts().head(10)
victoire_pilotes = drivers.set_index('driverId').loc[victoires.index][['forename', 'surname']]
victoire_pilotes['victoires'] = victoires.values
print('\nTop 10 pilotes par victoires :')
print(victoire_pilotes)

# Top constructeurs par victoires
victoires_const = results[results['positionOrder'] == 1]['constructorId'].value_counts().head(10)
victoire_teams = constructors.set_index('constructorId').loc[victoires_const.index][['name']]
victoire_teams['victoires'] = victoires_const.values
print('\nTop 10 constructeurs par victoires :')
print(victoire_teams)

# Répartition des nationalités des pilotes
plt.figure(figsize=(10,5))
drivers['nationality'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 nationalités de pilotes (2014-2024)')
plt.ylabel('Nombre de pilotes')
plt.tight_layout()
plt.savefig('cleaned/plot_nationalites_pilotes.png')
plt.close()

# Circuits les plus utilisés
plt.figure(figsize=(10,5))
circuits['name'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 circuits les plus utilisés (2014-2024)')
plt.ylabel('Nombre de courses')
plt.tight_layout()
plt.savefig('cleaned/plot_circuits_utilises.png')
plt.close()

# Distribution des positions à l’arrivée
plt.figure(figsize=(10,5))
results['positionOrder'].value_counts().sort_index().plot(kind='bar')
plt.title('Distribution des positions à l’arrivée')
plt.xlabel('Position')
plt.ylabel('Nombre de résultats')
plt.tight_layout()
plt.savefig('cleaned/plot_positions_arrivee.png')
plt.close()

print("\nQuelques visualisations ont été sauvegardées dans le dossier cleaned/.") 