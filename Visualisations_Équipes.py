#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fonction pour charger les dataframes depuis le fichier CSV
@st.cache_data
def load_data():
    file_path = 'Serie A teamdata.csv'
    df = pd.read_csv(file_path)

    # Traitement des données et création des quatre tableaux avec moyenne et renommage des colonnes
    def prepare_table(df, columns, rename_dict):
        table = df[["team_name"] + columns].copy()
        for col in columns:
            table[col] = table[col].round(2)
        table.rename(columns=rename_dict, inplace=True)
        avg_row = table.drop(columns=["team_name"]).mean(numeric_only=True).to_dict()
        avg_row = {col: round(val, 2) for col, val in avg_row.items()}
        avg_row["team_name"] = "Media Serie A"
        table.loc[len(table)] = avg_row
        return table

    # Productions Offensives
    prod_off_cols = [
        "team_season_op_xg_pg", "team_season_np_xg_per_shot", "team_season_op_shots_pg",
        "team_season_counter_attacking_shots_pg", "team_season_pace_towards_goal",
        "team_season_high_press_shots_pg", "team_season_shots_in_clear_pg", "team_season_op_shot_distance",
        "team_season_passes_inside_box_pg", "team_season_sp_xg_pg", "team_season_op_shots_outside_box_pg",
        "team_season_penalties_won_pg"
    ]
    prod_off_rename = {
        "team_season_op_xg_pg": "OP xG", "team_season_np_xg_per_shot": "OP xG/Shot", "team_season_op_shots_pg": "OP Shots",
        "team_season_counter_attacking_shots_pg": "C-A Shots", "team_season_pace_towards_goal": "Pace to Goal",
        "team_season_high_press_shots_pg": "High Press Shots", "team_season_shots_in_clear_pg": "Clear Shots",
        "team_season_op_shot_distance": "Shot Distance", "team_season_passes_inside_box_pg": "Passes Inside Box",
        "team_season_sp_xg_pg": "Set Pieces xG", "team_season_op_shots_outside_box_pg": "Shots Outside the Box",
        "team_season_penalties_won_pg": "Penalties"
    }
    prod_off_df = prepare_table(df, prod_off_cols, prod_off_rename)
    prod_off_top, prod_off_bottom = list(prod_off_rename.values())[:6], list(prod_off_rename.values())[6:]

    # Style Offensif
    style_cols = [
        "team_season_passing_ratio", "team_season_passes_inside_box_pg", "team_season_deep_progressions_pg",
        "team_season_deep_completions_pg", "team_season_gk_pass_distance", "team_season_gk_long_pass_ratio",
        "team_season_box_cross_ratio", "team_season_crosses_into_box_pg", "team_season_successful_crosses_into_box_pg",
        "team_season_completed_dribbles_pg", "team_season_dribble_ratio", "team_season_possession"
    ]
    style_rename = {
        "team_season_passing_ratio": "Passing %", "team_season_passes_inside_box_pg": "Passes inside Box",
        "team_season_deep_progressions_pg": "Deep Prog.", "team_season_deep_completions_pg": "Deep Comp.",
        "team_season_gk_pass_distance": "GK Pass Length", "team_season_gk_long_pass_ratio": "GK Long Pass%",
        "team_season_box_cross_ratio": "Box Cross%", "team_season_crosses_into_box_pg": "Box Cross",
        "team_season_successful_crosses_into_box_pg": "Succ. Box Cross", "team_season_completed_dribbles_pg": "Succ. Dribbles",
        "team_season_dribble_ratio": "Dribble%", "team_season_possession": "Possession%"
    }
    style_df = prepare_table(df, style_cols, style_rename)
    style_top, style_bottom = list(style_rename.values())[:6], list(style_rename.values())[6:]

    # Pressing
    pressing_cols = [
        "team_season_ppda", "team_season_defensive_distance", "team_season_aggression",
        "team_season_aggressive_actions_pg", "team_season_defensive_action_regains_pg", "team_season_pressures_pg",
        "team_season_pressure_regains_pg", "team_season_fhalf_pressures_pg", "team_season_fhalf_pressures_ratio",
        "team_season_counterpressures_pg", "team_season_fhalf_counterpressures_pg", "team_season_fhalf_counterpressures_ratio"
    ]
    pressing_rename = {
        "team_season_ppda": "PPDA", "team_season_defensive_distance": "Def. Distance",
        "team_season_aggression": "Aggression", "team_season_aggressive_actions_pg": "Agg. Actions",
        "team_season_defensive_action_regains_pg": "Def. Action Regains", "team_season_pressures_pg": "Pressures",
        "team_season_pressure_regains_pg": "Pressure Regains", "team_season_fhalf_pressures_pg": "Pressure 1/2",
        "team_season_fhalf_pressures_ratio": "Pressure 1/2 %", "team_season_counterpressures_pg": "Counterpr.",
        "team_season_fhalf_counterpressures_pg": "Counterpr. 1/2", "team_season_fhalf_counterpressures_ratio": "Counterpr. 1/2 %"
    }
    pressing_df = prepare_table(df, pressing_cols, pressing_rename)
    pressing_top, pressing_bottom = list(pressing_rename.values())[:6], list(pressing_rename.values())[6:]

    # Productions Défensives
    def_cols = [
        "team_season_op_xg_conceded_pg", "team_season_np_xg_per_shot_conceded", "team_season_op_shots_conceded_pg",
        "team_season_op_shot_distance_conceded", "team_season_shots_in_clear_conceded_pg", "team_season_counter_attacking_shots_conceded_pg",
        "team_season_high_press_shots_conceded_pg", "team_season_passes_inside_box_conceded_pg", "team_season_deep_progressions_conceded_pg",
        "team_season_opp_passing_ratio", "team_season_penalties_conceded_pg", "team_season_sp_xg_conceded_pg"
    ]
    def_rename = {
        "team_season_op_xg_conceded_pg": "OP xG Conceded", "team_season_np_xg_per_shot_conceded": "OP xG/Shot Conc.",
        "team_season_op_shots_conceded_pg": "OP Shots Conc.", "team_season_op_shot_distance_conceded": "Opp. Shots Distance",
        "team_season_shots_in_clear_conceded_pg": "Clear Shots Conc.", "team_season_counter_attacking_shots_conceded_pg": "C-A Shots Conc.",
        "team_season_high_press_shots_conceded_pg": "HP Shots Conc.", "team_season_passes_inside_box_conceded_pg": "Passes in Box Conc.",
        "team_season_deep_progressions_conceded_pg": "Opp. Deep Progression", "team_season_opp_passing_ratio": "Opp. Passing%",
        "team_season_penalties_conceded_pg": "Penalties Conc.", "team_season_sp_xg_conceded_pg": "Set Pieces xG Conc."
    }
    def_df = prepare_table(df, def_cols, def_rename)
    def_top, def_bottom = list(def_rename.values())[:6], list(def_rename.values())[6:]

    return {
        "Produzioni Offensive": prod_off_df,
        "Stile Offensivo": style_df,
        "Pressing": pressing_df,
        "Produzione Difensiva": def_df
    }, {
        "Produzioni Offensive": (prod_off_top, prod_off_bottom, {v: v for v in prod_off_rename.values()}),
        "Stile Offensivo": (style_top, style_bottom, {v: v for v in style_rename.values()}),
        "Pressing": (pressing_top, pressing_bottom, {v: v for v in pressing_rename.values()}),
        "Produzione Difensiva": (def_top, def_bottom, {v: v for v in def_rename.values()})
    }

# Fonction de rendu du tableau avec surlignage de ligne (inchangée)
def render_table(df, top_metrics, bottom_metrics, title_map, highlight_team):
    num_cols = max(len(top_metrics), len(bottom_metrics))
    row_height = 0.4  # hauteur par ligne
    n_teams = df.shape[0] + 1  # +1 pour la ligne de titre
    fig_height = 22
    fig_width = 20

    fig, axes = plt.subplots(
    nrows=2, ncols=num_cols,
    figsize=(fig_width, fig_height),
    sharey=True

    )

    if isinstance(axes[0], plt.Axes):
        axes = [axes]

    for row_idx, metrics_set in enumerate([top_metrics, bottom_metrics]):
        for col_idx, metric in enumerate(metrics_set):
            ax = axes[row_idx][col_idx]
            sorted_df = df.sort_values(by=metric, ascending=(metric in ascending_metrics)).reset_index(drop=True)
            ax.axis("off")
            ax.set_ylim(0, 1)
            # Ligne d'en-tête
            ax.annotate(
            title_map[metric],
            xy=(0.5, 1),
            xycoords='axes fraction',
            ha='center',
            fontsize=13,
            fontweight='bold',
            annotation_clip=False
            )
            
            # Affichage des équipes
            for i, row in enumerate(sorted_df.itertuples(), start=1):
                team = getattr(row, "team_name")
                value = df.loc[df["team_name"] == team, metric].values[0]

                if team == "Media Serie A":
                    bgcolor = "silver"
                elif team == "AS Roma":
                    bgcolor = "firebrick"
                elif team == highlight_team:
                    bgcolor = "peachpuff"
                else:
                    bgcolor = None

                color = "white" if bgcolor == "firebrick" else "black"
                fontweight = "bold" if bgcolor else "normal"
                ypos = 1 - (i + 1) / (df.shape[0] + 2)

                if bgcolor:
                    ax.axhspan(ypos - 0.02, ypos + 0.02, color=bgcolor, zorder=0)
                ax.text(0.0, ypos, team, fontsize=15, ha="left", color=color, fontweight=fontweight, zorder=1)
                ax.text(0.95, ypos, f"{value:.2f}", fontsize=15, ha="right", color=color, fontweight=fontweight, zorder=1)

        for j in range(len(metrics_set), len(axes[row_idx])):
            axes[row_idx][j].axis("off")

    plt.tight_layout(h_pad=4)
    st.pyplot(fig)

# Streamlit UI
explications = {
    "Produzioni Offensive": """
### Spiegazione delle metriche

**OP xG**: xG generato su azione, esclusi i calci piazzati.  
**OP xG/Shot**: xG per tiro su azione.  
**OP Shots**: tiri creati su azione.  
**C-A Shots**: tiri da contropiede (generati nei 15 secondi successivi a un possesso iniziato nella metà campo della propria squadra).  
**Pace to Goal**: velocità media delle azioni che terminano con un tiro, dal recupero palla fino al tiro (metri/secondo).  
**High Press Shots**: tiri generati da possessi recuperati entro 5 secondi da un’azione difensiva (pressione, contrasto, intercetto o passaggio bloccato) nella metà campo avversaria.  
**Clear Shots**: tiri effettuati con il solo portiere avversario tra il tiratore e la porta.  
**Shot Distance**: distanza media dei tiri dalla porta (esclusi i rigori).  
**Passes Inside Box**: passaggi completati all’interno dell’area di rigore avversaria da un giocatore già posizionato nell’area.  
**Set Pieces xG**: xG generato da calcio piazzato (esclusi i rigori).  
**Shots Outside the Box**: tiri da fuori area su azione.  
**Penalties**: rigori conquistati.
""",

    "Stile Offensivo": """
### Spiegazione delle metriche

**Passing%**: percentuale di passaggi completati sul totale dei passaggi tentati.  
**Passes in. Box**: passaggi completati all’interno dell’area di rigore avversaria da parte di un giocatore già posizionato nell’area.  
**Deep Comp.**: Deep Completions (passaggi riusciti verso un compagno situato entro 20 metri dalla porta avversaria).  
**Deep Prog.**: Deep Progressions (passaggi o conduzioni riuscite nel terzo offensivo avversario).  
**GK Pass Length**: lunghezza media dei rinvii o passaggi del portiere in fase di costruzione dal basso.  
**GK Long Pass%**: percentuale di lanci lunghi (oltre 32 metri) del portiere che raggiungono un compagno.  
**Box Cross%**: percentuale di cross sul totale dei passaggi diretti verso l’area di rigore avversaria.  
**Box Cross**: numero di cross effettuati verso l’area di rigore avversaria.  
**Succ. Box Cross**: cross completati all’interno dell’area di rigore avversaria.  
**Succ. Dribble**: numero di dribbling riusciti della squadra.  
**Dribble%**: percentuale di dribbling riusciti sul totale dei tentativi.  
**Possession%**: percentuale di possesso palla della squadra.
""",

    "Pressing": """
### Spiegazione delle metriche

**PPDA**: quanti passaggi l’avversario riesce a completare prima che la squadra effettui un’azione difensiva (contrasto, intercetto, fallo). Indicatore dell’intensità del pressing, calcolato nelle zone alte del campo (il 40% più lontano dalla propria porta).  
**Def. Distance**: distanza media dalla propria porta in cui la squadra effettua azioni difensive.  
**Aggression**: percentuale di passaggi ricevuti da un avversario che sono immediatamente seguiti da un contrasto, fallo o pressione entro 2 secondi dalla ricezione.  
**Agg. Actions**: contrasti, falli o pressioni effettuati nei 2 secondi successivi alla ricezione del pallone da parte di un avversario.  
**Def. Action Regains**: numero di volte in cui la squadra ha recuperato il pallone entro 5 secondi da un’azione difensiva (pressione, contrasto, intercetto o passaggio bloccato) di un proprio giocatore.  
**Pressure**: numero di volte in cui la squadra esercita pressione su un avversario in possesso del pallone.  
**Pressure Regains**: palloni recuperati entro 5 secondi da una pressione su un avversario.  
**Pressure ½**: pressioni effettuate nella metà campo avversaria.  
**Pressure ½ %**: percentuale di pressioni effettuate nella metà campo avversaria sul totale delle pressioni.  
**Counterpr.**: pressioni effettuate nei 5 secondi successivi a una perdita di possesso.  
**Counterpr. ½**: pressioni effettuate nei 5 secondi successivi a una perdita di possesso nella metà campo avversaria.  
**Counterpr. ½ %**: percentuale di contropressioni nella metà campo avversaria sul totale delle contropressioni.
""",

    "Produzione Difensiva": """
### Spiegazione delle metriche

**OP xG Conceded**: xG concessi su azione, esclusi i calci piazzati.  
**OP xG/Shot Conc.**: xG per tiro concesso su azione.  
**OP Shots Conc.**: tiri concessi su azione.  
**Opp. Shot Distance**: distanza media dalla porta dei tiri concessi (esclusi i rigori).  
**Clear Shots Conc.**: tiri concessi in cui solo il portiere si trova tra il tiratore e la porta.  
**C-A Shots Conc.**: tiri concessi in contropiede (entro 15 secondi da un possesso iniziato nella metà campo avversaria).  
**HP Shots Conc.**: tiri concessi dopo che l’avversario ha recuperato il possesso entro 5 secondi da un’azione difensiva.  
**Passes in Box Conc.**: passaggi completati dall’avversario all’interno dell’area di rigore, da parte di un giocatore già posizionato nell’area.  
**Opp. Deep Progression**: passaggi e conduzioni subiti nel terzo offensivo avversario.  
**Opp. Passing%**: percentuale di passaggi completati dall’avversario.  
**Penalties Conc.**: rigori concessi.  
**Set Pieces xG**: xG concessi da calcio piazzato (esclusi i rigori).
"""
}

st.title("Visualizza i dati per squadra - Serie A")

dataframes, config = load_data()

tableau = st.selectbox("Scegliere una tabella :", list(dataframes.keys()))
df = dataframes[tableau]
top_metrics, bottom_metrics, title_map = config[tableau]

all_teams = df[df["team_name"] != "Media Serie A"]["team_name"].tolist()
highlight_team = st.multiselect("Scegliere una squadra da mettere in evidenza :", all_teams, index=all_teams.index("AC Milan") if "AC Milan" in all_teams else 0)

# Liste des métriques à trier du plus petit au plus grand
ascending_metrics = [
    "PPDA",  # Pressing
    "OP xG Conceded", "OP xG/Shot Conc.", "OP Shots Conc.", "Clear Shots Conc.",
    "C-A Shots Conc.", "HP Shots Conc.", "Passes in Box Conc.",
    "Opp. Deep Progression", "Opp. Passing%", "Penalties Conc.", "Set Pieces xG Conc."
]

render_table(df, top_metrics, bottom_metrics, title_map, highlight_team)

st.markdown("---")
st.markdown(explications[tableau])
