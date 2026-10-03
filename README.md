# 🏎️ Formula 1 Driver Clustering (K-Means)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

An end-to-end Machine Learning pipeline that groups modern Formula 1 drivers (2014-2024) into distinct profiles using **K-Means Clustering** based on their performance, consistency, and career statistics.

---

## 📖 Table of Contents
- [Project Overview](#-project-overview)
- [Data Pipeline & Preparation](#-data-pipeline--preparation)
- [Master Dataset Construction](#-master-dataset-construction)
- [K-Means Clustering & Analysis](#-k-means-clustering--analysis)
- [Visualizations](#-visualizations)
- [Getting Started](#-getting-started)
- [License](#-license)

---

## 🎯 Project Overview

This project analyzes Formula 1 race and qualifying data from the modern hybrid era (2014–2024) to objectively categorize drivers based on their statistical footprints. 

Using K-Means clustering, the algorithm automatically identifies **four distinct driver profiles**:
1. 🏆 **Champions** (e.g., Lewis Hamilton, Max Verstappen)
2. 🚀 **Experienced** (Veterans with solid track records)
3. 🏎️ **Regulars** (Consistent mid-field drivers)
4. 🔰 **Rookies** (Newcomers with limited data)

---

## 🧹 Data Pipeline & Preparation

The project relies on a comprehensive set of historical F1 data.
- **Raw Data Source (`archive/`)**: `races.csv`, `results.csv`, `drivers.csv`, `constructors.csv`, `circuits.csv`, `qualifying.csv`, `status.csv`
- **Data Cleaning (`data_cleaning.py`)**:
  - Filtered exclusively for the **2014 to 2024** seasons.
  - Removed entities (drivers, constructors, circuits) not active during this period.
  - Imputed missing values (`/N`, `\N` replaced with `-1` for critical columns like `q1`, `q2`, `q3`, `time`, and `milliseconds`).
- **Cleaned Outputs (`cleaned/`)**: Generated modern, standardized CSVs ready for feature engineering.

---

## 🏗️ Master Dataset Construction

The final analytical pipeline (`clustering_kmeans.py`) processes the cleaned files into a single, unified Master Dataset: **`pilot_features_kmeans.csv`**.

This central database contains:
- **Clustering Features**: Participations, Wins, Podiums, Average Points, DNFs (Retirements), Q3 Appearances, Average Track Position, Total Seasons, etc.
- **Clustering Results**: Assigned `cluster_id` and descriptive `cluster_name`.
- **Driver Identifiers**: `driverId` and Full Name.

*Note: This master file is perfectly structured to be exported to MongoDB or any SQL/NoSQL database, ensuring complete reproducibility for all downstream visualizations.*

---

## 🧠 K-Means Clustering & Analysis

1. **Normalization**: All features are standardized (Z-score scaling) to ensure unbiased distance calculations.
2. **Optimal 'K' Selection**:
   - The **Elbow Method** was utilized by plotting inertia against K.
   - The inflection point clearly indicated **K=4** as the optimal number of clusters (`kmeans_coude.png`).
3. **Cluster Assignment & Profiling**:
   - K-Means was applied to the normalized dataset, successfully mapping every driver into one of the 4 defined profiles.
4. **Deep-Dive Analytics**:
   - Multiple dimensions of the clusters were analyzed, generating dedicated CSV reports and visualizations for:
     - Performance (`analyse_performance.csv`)
     - Consistency/Regularity (`analyse_regularite.csv`)
     - Qualifying Prowess (`analyse_qualification.csv`)
     - Experience (`analyse_experience.csv`)
     - Career Style (`analyse_style_carriere.csv`)

---

## 📊 Visualizations

To make the clustering results highly interpretable, the pipeline generates 2D projections using **Principal Component Analysis (PCA)**. 

- **PCA Scatter Plot (`kmeans_pilotes_pca.png`)**: Visually separates the 4 clusters on a 2D plane, clearly showing the boundary between Champions, Rookies, and the midfield.

*(All plots and charts are automatically generated from the master dataset to guarantee consistency).*

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Required Libraries: `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `numpy`

### Running the Pipeline
1. **Clean the Data**:
   ```bash
   python data_cleaning.py
   ```
2. **Run the Clustering Algorithm** (This will generate the Master Dataset and all visual plots):
   ```bash
   python clustering_kmeans.py
   ```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
