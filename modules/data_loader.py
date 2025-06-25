import os
import pandas as pd
from modules.constants import COLUMN_MAP, TLOL_SPORTS

def load_and_merge_scores(report_folder="reports"):
    # Load files
    df1 = pd.read_csv(os.path.join(report_folder, "TLOL 1 Scores.csv"))
    df2 = pd.read_csv(os.path.join(report_folder, "TLOL 2 Scores.csv"))

    # Filter only M or F genders
    df1 = df1[df1['Gender'].isin(['M', 'F'])]
    df2 = df2[df2['Gender'].isin(['M', 'F'])]

    # Standardize player names
    for df in [df1, df2]:
        df['Player'] = df['Player'].str.strip().str.title()

    # Remove unnamed columns and participation-type markers
    def clean_and_map(df):
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        df = df.drop(columns=[col for col in df.columns if 'participation' in col.lower()], errors='ignore')
        id_cols = ['Player', 'Gender']
        score_cols = [col for col in df.columns if col not in id_cols]

        df_melted = df.melt(id_vars=id_cols, value_vars=score_cols, var_name="Game", value_name="Score")
        df_melted["Game"] = df_melted["Game"].map(COLUMN_MAP).fillna(df_melted["Game"])
        df_melted['Score'] = pd.to_numeric(df_melted['Score'], errors='coerce').fillna(0)

        return df_melted

    df1_clean = clean_and_map(df1)
    df2_clean = clean_and_map(df2)

    merged = pd.concat([df1_clean, df2_clean], ignore_index=True)

    # Final summary and pivot
    summary = merged.groupby(['Player', 'Gender', 'Game'])['Score'].sum().reset_index()
    pivoted = summary.pivot_table(index=['Player', 'Gender'], columns='Game', values='Score', fill_value=0).reset_index()

    # Flatten columns
    pivoted.columns.name = None

    # Keep only known sports + identity columns
    final_df = pivoted[['Player', 'Gender'] + [col for col in TLOL_SPORTS if col in pivoted.columns]].copy()
    
    existing_sports = [sport for sport in TLOL_SPORTS if sport in final_df.columns]
    final_df.loc[:, 'Total Score'] = final_df[existing_sports].sum(axis=1)

    return final_df
