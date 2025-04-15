#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Données
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/favie/Desktop/Deposit/Statsbomb/Adversaire/Progression/Progression Final Serie A.csv")
    df = df[df["Position"].notna()]  # Nettoyage de base
    return df

df = load_data()

# Interface utilisateur
st.title("Progressioni per 90min – Serie A")
teams = sorted(df["Équipe"].dropna().unique())
selected_team = st.selectbox("Selezionare una squadra", teams)
min_minutes = st.slider("Filtrare per minuti giocati (min)", 0, 4000, 500, step=100)

# Filtrage
data = df[(df["Équipe"] == selected_team) & (df["Min jouées"] >= min_minutes)]

# Ordre des positions
position_order = [
    "Goalkeeper", "Centre Back", "Fullback", "Midfielder",
    "Attacking Mid", "Winger", "Striker"
]

# Tri des joueurs : par position d'abord puis par total des actions progressives
data["Position"] = pd.Categorical(data["Position"], categories=position_order, ordered=True)
data["Total prog/90"] = data["Passes progressives par 90min"] + data["Courses progressives par 90min"]
data = data.sort_values(by=["Position", "Total prog/90"], ascending=[True, False]).reset_index(drop=True)

# Moyennes Serie A
league_data = df[df["Min jouées"] >= 500]
position_means = league_data.groupby("Position")[
    ["Passes progressives par 90min", "Courses progressives par 90min"]
].mean()

# Graphique avec taille ajustée
fig, ax = plt.subplots(figsize=(936 / 72, 432 / 72))  # Conversion de pt en pouces (1 pt = 1/72 inch)

passes = data["Passes progressives par 90min"]
carries = data["Courses progressives par 90min"]
totals = passes + carries
minutes = data["Min jouées"]
labels = data["Joueur"]

bar1 = ax.barh(labels, passes, label="Passaggi progressivi/90")
bar2 = ax.barh(labels, carries, left=passes, label="Conduzioni progressivi/90")

# Annotations internes + y-tick custom
for i, label in enumerate(labels):
    if passes.iloc[i] > 0.2:
        ax.text(passes.iloc[i] / 2, i, f"{passes.iloc[i]:.1f}", va='center', ha='center', color='white', fontsize=8)
    if carries.iloc[i] > 0.2:
        ax.text(passes.iloc[i] + carries.iloc[i] / 2, i, f"{carries.iloc[i]:.1f}", va='center', ha='center', color='white', fontsize=8)

# Personnalisation des étiquettes : Nom + Minutes
ax.set_yticks(range(len(labels)))
custom_labels = [f"{name} ({int(minute):,} m)" for name, minute in zip(labels, minutes)]
ax.set_yticklabels(custom_labels, fontsize=8)

# Ligne verticale noire à 0
y_min, y_max = -0.5, len(data) - 0.5
ax.vlines(x=0, ymin=y_min, ymax=y_max, color='black', linewidth=1)

# Longueur max
x_max = totals.max()
x_label_pos = x_max

# Lignes, moyennes, positions
for pos in position_order:
    group = data[data["Position"] == pos]
    if not group.empty:
        start_idx = group.index.min()
        end_idx = group.index.max()
        mid_index = (start_idx + end_idx) / 2

        if start_idx != data.index[0]:
            ax.hlines(y=data.index.get_loc(start_idx) - 0.5, xmin=0, xmax=x_max, color='black', linestyle='-', linewidth=1.5)

        if pos in position_means.index:
            total_mean = position_means.loc[pos, "Passes progressives par 90min"] + position_means.loc[pos, "Courses progressives par 90min"]
            ax.vlines(x=total_mean, ymin=data.index.get_loc(start_idx) - 0.5, ymax=data.index.get_loc(end_idx) + 0.5, color='red', linestyle='--', linewidth=1)
            ax.text(total_mean + 0.2, data.index.get_loc(end_idx) + 0.35,
                    f"Media Serie A: {total_mean:.1f}", va='bottom', ha='left', fontsize=8, color='red', fontstyle='italic')

        ax.text(x_label_pos, mid_index, pos, va='center', ha='left', fontsize=9, fontweight='bold', clip_on=False)

# Finalisation
ax.set_xlim(0, x_label_pos + 1)
ax.set_xlabel("Azioni progressive / 90 min")
ax.set_title(f"Progressioni per 90min – {selected_team}")

# Fixer la légende en bas à gauche
ax.legend(loc='lower right', fontsize=6)

# Supprimer le cadre autour du graphique
for spine in ax.spines.values():
    spine.set_visible(False)

ax.grid(False)
ax.set_axisbelow(True)
plt.tight_layout(rect=[0.13, 0.01, 1, 1])
plt.gca().invert_yaxis()

# Affichage
st.pyplot(fig)