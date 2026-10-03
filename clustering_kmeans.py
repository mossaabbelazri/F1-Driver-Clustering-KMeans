import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid', font_scale=1.2)

# 1. Charger les fichiers nettoyés
results = pd.read_csv('cleaned/results_modern.csv')
drivers = pd.read_csv('cleaned/drivers_modern.csv')
qualifying = pd.read_csv('cleaned/modern_qualifying.csv')
status = pd.read_csv('cleaned/modern_status.csv')
races = pd.read_csv('cleaned/races_modern.csv')

# 2. Création des features par pilote
# A. Participations, victoires, podiums, points moyens, position moyenne
pilot_features = results.groupby('driverId').agg(
    participations = ('raceId', 'count'),
    victoires = ('positionOrder', lambda x: (x == 1).sum()),
    podiums = ('positionOrder', lambda x: (x <= 3).sum()),
    points_moyen = ('points', 'mean'),
    position_moy = ('positionOrder', 'mean'),
)

# B. Calcul des abandons à partir du statut
status_dict = dict(zip(status['statusId'], status['status']))
results['status_desc'] = results['statusId'].map(status_dict)
def is_dnf(s):
    if pd.isna(s):
        return 0
    if s.startswith('Finished') or s.startswith('+'):
        return 0
    return 1
results['is_dnf'] = results['status_desc'].apply(is_dnf)
abandons = results.groupby('driverId')['is_dnf'].sum()
pilot_features = pilot_features.join(abandons.rename('abandons'), how='left')

# C. Moyenne du temps en Q3 (q3_mean) et nombre de Q3 atteints (corrigé)
if 'q3' in qualifying.columns:
    qualifying['q3'] = qualifying['q3'].replace([-1, '\\N', '/N', ''], pd.NA)
    qualifying['q3_s'] = pd.to_timedelta(qualifying['q3'], errors='coerce').dt.total_seconds()
    q3_mean = qualifying.groupby('driverId')['q3_s'].mean()
    q3_count = qualifying.groupby('driverId')['q3'].count()  # Compte le nombre de Q3 valides
    pilot_features = pilot_features.join(q3_mean.rename('q3_mean'), how='left')
    pilot_features = pilot_features.join(q3_count.rename('q3_count'), how='left')
else:
    pilot_features['q3_mean'] = 0
    pilot_features['q3_count'] = 0

# D. Nombre de saisons différentes
race_years = races.set_index('raceId')['year']
results['year'] = results['raceId'].map(race_years)
saisons = results.groupby('driverId')['year'].nunique()
pilot_features = pilot_features.join(saisons.rename('saisons'), how='left')

# E. Ajouter le nom complet du pilote
pilot_features = pilot_features.join(
    drivers.set_index('driverId')[['forename', 'surname']],
    how='left'
)
pilot_features['nom_complet'] = pilot_features['forename'] + ' ' + pilot_features['surname']

# 3. Nettoyage/remplacement des NaN restants
pilot_features = pilot_features.fillna(0)

# 4. Normalisation des features pour le clustering
features = ['participations', 'victoires', 'podiums', 'points_moyen', 'abandons', 'q3_mean', 'q3_count', 'position_moy', 'saisons']
X = pilot_features[features].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Choix du nombre de clusters (méthode du coude)
inertia = []
K_range = range(1, 10)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)
plt.figure(figsize=(8,4))
plt.plot(K_range, inertia, marker='o')
plt.xlabel('Nombre de clusters')
plt.ylabel('Inertie (within-cluster sum of squares)')
plt.title('Méthode du coude pour choisir K')
plt.tight_layout()
plt.savefig('cleaned/kmeans_coude.png')
plt.close()

# 6. Appliquer K-Means avec le nombre de clusters choisi (ex: 4)
K = 4  # À ajuster après avoir vu la courbe du coude
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
pilot_features['cluster'] = kmeans.fit_predict(X_scaled)

# Mapping des noms de clusters
cluster_names = {
    0: 'Réguliers',
    1: 'Expérimentés',
    2: 'Rookies',
    3: 'Champions'
}

pilot_features['nom_cluster'] = pilot_features['cluster'].map(cluster_names)

# 7. Sauvegarder le DataFrame final avec les labels de cluster, le nom complet et le nom du cluster
pilot_features.to_csv('cleaned/pilot_features_kmeans.csv', index=True)

# Charger le master pour toutes les analyses suivantes
master = pd.read_csv('cleaned/pilot_features_kmeans.csv')

# DÉBOGAGE : Afficher le top 20 des pilotes par nombre de Q3 atteints
print('\nTop 20 pilotes par nombre de Q3 atteints (q3_count) :')
print(master[['nom_complet', 'q3_count']].sort_values('q3_count', ascending=False).head(20))

# 1. Performance globale
perf_cols = ['driverId', 'nom_complet', 'victoires', 'podiums', 'points_moyen', 'position_moy']
master[perf_cols].sort_values('points_moyen', ascending=False).to_csv('cleaned/analyse_performance.csv', index=False)
plt.figure(figsize=(12,7))
top_points = master.sort_values('points_moyen', ascending=False).head(10)
sns.barplot(data=top_points, x='points_moyen', y='nom_complet', palette='viridis')
plt.title('Top 10 pilotes par points moyens (2014-2024)', fontsize=18, fontweight='bold')
plt.xlabel('Points moyens', fontsize=15)
plt.ylabel('Pilote', fontsize=15)
for i, v in enumerate(top_points['points_moyen']):
    plt.text(v + 0.2, i, f'{v:.1f}', va='center', fontsize=13)
plt.tight_layout()
plt.savefig('cleaned/plot_performance.png')
plt.close()

# 2. Régularité et fiabilité
reg_cols = ['driverId', 'nom_complet', 'abandons', 'participations']
master[reg_cols].sort_values('abandons', ascending=False).to_csv('cleaned/analyse_regularite.csv', index=False)
plt.figure(figsize=(12,7))
top_abandons = master.sort_values('abandons', ascending=False).head(10)
sns.barplot(data=top_abandons, x='abandons', y='nom_complet', palette='magma')
plt.title('Top 10 pilotes avec le plus d’abandons', fontsize=18, fontweight='bold')
plt.xlabel('Nombre d’abandons', fontsize=15)
plt.ylabel('Pilote', fontsize=15)
for i, v in enumerate(top_abandons['abandons']):
    plt.text(v + 0.2, i, f'{int(v)}', va='center', fontsize=13)
plt.tight_layout()
plt.savefig('cleaned/plot_regularite.png')
plt.close()

# 3. Compétence en qualification
qualif_cols = ['driverId', 'nom_complet', 'q3_mean', 'q3_count']
master[qualif_cols].sort_values('q3_count', ascending=False).to_csv('cleaned/analyse_qualification.csv', index=False)
plt.figure(figsize=(12,7))
top_q3 = master.sort_values('q3_count', ascending=False).head(10)
sns.barplot(data=top_q3, x='q3_count', y='nom_complet', palette='crest')
plt.title('Top 10 pilotes ayant atteint le plus souvent Q3', fontsize=18, fontweight='bold')
plt.xlabel('Nombre de Q3 atteints', fontsize=15)
plt.ylabel('Pilote', fontsize=15)
for i, v in enumerate(top_q3['q3_count']):
    plt.text(v + 0.2, i, f'{int(v)}', va='center', fontsize=13)
plt.tight_layout()
plt.savefig('cleaned/plot_qualification.png')
plt.close()

# 4. Expérience
exp_cols = ['driverId', 'nom_complet', 'participations', 'saisons']
master[exp_cols].sort_values('participations', ascending=False).to_csv('cleaned/analyse_experience.csv', index=False)
plt.figure(figsize=(12,7))
top_exp = master.sort_values('participations', ascending=False).head(10)
sns.barplot(data=top_exp, x='participations', y='nom_complet', palette='flare')
plt.title('Top 10 pilotes les plus expérimentés (participations)', fontsize=18, fontweight='bold')
plt.xlabel('Nombre de participations', fontsize=15)
plt.ylabel('Pilote', fontsize=15)
for i, v in enumerate(top_exp['participations']):
    plt.text(v + 0.2, i, f'{int(v)}', va='center', fontsize=13)
plt.tight_layout()
plt.savefig('cleaned/plot_experience.png')
plt.close()

# 5. Style de carrière (synthèse par cluster) avec noms
features = ['participations', 'victoires', 'podiums', 'points_moyen', 'abandons', 'q3_mean', 'q3_count', 'position_moy', 'saisons']
cluster_names = {
    0: 'Réguliers',
    1: 'Expérimentés',
    2: 'Rookies',
    3: 'Champions'
}
cluster_summary = master.groupby('cluster')[features].mean()
cluster_summary.to_csv('cleaned/analyse_style_carriere.csv')
cluster_summary_named = cluster_summary.copy()
cluster_summary_named.index = [cluster_names.get(i, f'Cluster {i}') for i in cluster_summary_named.index]
plt.figure(figsize=(14,8))
sns.heatmap(cluster_summary_named.T, annot=True, fmt='.1f', cmap='YlGnBu', cbar=True, linewidths=0.5)
plt.title('Profil moyen par cluster (style de carrière)', fontsize=18, fontweight='bold')
plt.ylabel('Features')
plt.xlabel('Cluster')
plt.tight_layout()
plt.savefig('cleaned/plot_style_carriere.png')
plt.close()

# 9. Visualisation 2D (PCA) avec noms de clusters
from sklearn.decomposition import PCA
scaler = StandardScaler()
X = master[features].values
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
plt.figure(figsize=(10,8))
palette = sns.color_palette('Set2', n_colors=len(cluster_names))
for i, (label, color) in enumerate(zip(cluster_names.values(), palette)):
    idx = master['cluster'] == i
    plt.scatter(X_pca[idx,0], X_pca[idx,1], label=label, s=120, alpha=0.85, edgecolor='k', color=color)
plt.xlabel('Composante principale 1', fontsize=15)
plt.ylabel('Composante principale 2', fontsize=15)
plt.title('Clusters de pilotes F1 (K-Means, PCA)', fontsize=18, fontweight='bold')
plt.legend(title='Cluster', fontsize=13)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('cleaned/kmeans_pilotes_pca.png')
plt.close()

print('Clustering et analyses terminés. Résultats et visualisations sauvegardés dans cleaned/.') 