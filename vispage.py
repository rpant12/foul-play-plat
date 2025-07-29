import streamlit as st
import pandas as pd
import os
import base64

bosses = pd.read_json("bosses.json").transpose()
leaders = bosses[bosses.get("trainer_name").str.contains("Leader")]

st.title("Leader Stats Viewer")

trainer_names = leaders["trainer_name"].unique()
selected_trainer = st.selectbox("Select a Leader", trainer_names)

selected_stats = leaders[leaders["trainer_name"] == selected_trainer]
st.subheader(f"{selected_trainer}'s Pokemon")

pokemon_list = selected_stats["pokemon"].iloc[0]
pokemon_df = pd.DataFrame(pokemon_list)

# Remove unwanted columns if present
for col in ["xp", "nature_id", "personality", "forme"]:
    if col in pokemon_df.columns:
        pokemon_df = pokemon_df.drop(columns=[col])

sprite_folder = os.path.join(os.path.dirname(__file__), "platinum")

def get_sprite_html(species_id, species):
    sprite_path = os.path.join(sprite_folder, f"{species_id}.png")
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as img_file:
            b64 = base64.b64encode(img_file.read()).decode()
        return f'<img src="data:image/png;base64,{b64}" width="72" alt="{species}" style="display:block;margin:auto;"/>'
    else:
        return "<i>No sprite</i>"

# Prepare transposed data
columns = ["Sprite"] + [row.get("species", f"Pokémon {i+1}") for i, row in pokemon_df.iterrows()]
rows = []

# Sprite row
sprite_row = ["<b>Sprite</b>"]
for _, row in pokemon_df.iterrows():
    sprite_row.append(get_sprite_html(row["species_id"], row.get("species", "")))
rows.append(sprite_row)

# For each stat (excluding species_id, species, moves, and removed columns), build a row
stat_cols = [col for col in pokemon_df.columns if col not in ("species_id", "species", "moves")]
for stat in stat_cols:
    stat_row = [f'<b>{stat.capitalize()}</b>']
    for _, row in pokemon_df.iterrows():
        stat_row.append(row.get(stat, ""))
    rows.append(stat_row)

# Moves row (special display)
moves_row = ['<b>Moves</b>']
for _, row in pokemon_df.iterrows():
    moves = row.get("moves", [])
    move_boxes = ""
    for i in range(4):
        move = moves[i] if i < len(moves) else "no move"
        move_boxes += (
            f'<div style="background: #353945; color: #fff; border-radius: 8px; '
            f'padding: 6px 12px; margin: 2px 0; min-width: 80px; text-align: center; '
            f'font-size: 0.95em; border: 1px solid #44495a; width: 100%;">{move}</div>'
        )
    moves_row.append(
        f'<div style="display:flex;flex-direction:column;align-items:stretch;width:100%;">{move_boxes}</div>'
    )
rows.append(moves_row)

# Build HTML table with enhanced CSS
header_html = "<tr>" + "".join([f"<th>{col}</th>" for col in columns]) + "</tr>"
rows_html = ""
for i, row in enumerate(rows):
    row_style = ' style="background-color:#23272f;"' if i % 2 == 0 else ''
    row_html = "".join([f"<td>{cell}</td>" for cell in row])
    rows_html += f"<tr{row_style}>{row_html}</tr>"

table_html = f"""
<style>
.poke-table {{
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    font-family: 'Segoe UI', Arial, sans-serif;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    margin-bottom: 2em;
    background: #23272f;
}}
.poke-table th {{
    background: linear-gradient(90deg, #23272f 0%, #3a3f4b 100%);
    color: #fff;
    font-size: 1.1em;
    padding: 12px 8px;
    text-align: center;
    border-bottom: 2px solid #44495a;
}}
.poke-table td {{
    padding: 10px 8px;
    text-align: center;
    font-size: 1em;
    border-bottom: 1px solid #353945;
    color: #e0e6f0;
    background: #23272f;
}}
.poke-table tr:hover td {{
    background-color: #2d3340 !important;
    transition: background 0.2s;
}}
.poke-table td:first-child, .poke-table th:first-child {{
    background-color: #2d3340;
    font-weight: bold;
    width: 120px;
}}
</style>
<table class="poke-table">
    <thead>{header_html}</thead>
    <tbody>{rows_html}</tbody>
</table>
"""

st.markdown("### Pokémon Table")
st.markdown(table_html, unsafe_allow_html=True)