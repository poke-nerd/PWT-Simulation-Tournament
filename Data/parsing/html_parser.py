import os

def get_players_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if " vs " in line:
                return line.strip().split(" vs ")
    return ["Player1", "Player2"]

def parse_battle_log_gen5_from_txt(file_path, player1, player2):
    battle_data = []

    p1_pokes = []
    p2_pokes = []
    battle_body = []

    # First pass: extract poke lines
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("[[[[") or " vs " in line:
                continue
            if line.startswith("|poke|p1|"):
                raw = line.split("|")[3]
                pieces = [p.strip() for p in raw.split(",")]
                name = pieces[0]
                gender = ", M" if "M" in pieces else ", F" if "F" in pieces else ""
                p1_pokes.append(f"|poke|p1|{name}{gender}")
            elif line.startswith("|poke|p2|"):
                raw = line.split("|")[3]
                pieces = [p.strip() for p in raw.split(",")]
                name = pieces[0]
                gender = ", M" if "M" in pieces else ", F" if "F" in pieces else ""
                p2_pokes.append(f"|poke|p2|{name}{gender}")

    # Second pass: extract post-teampreview battle content
    start_found = False
    with open(file_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            if not start_found:
                if line.startswith("|start") or line.startswith("|turn|"):
                    start_found = True
                    battle_body.append(line)
                continue

            battle_body.append(line)

            # Inject |-faint| after any 0 fnt damage line
            if "|-damage|" in line and "|0 fnt" in line:
                parts = line.split("|")
                if len(parts) > 2:
                    target = parts[2].strip()
                    battle_body.append(f"|-faint|{target}")

    # Build full battle log
    battle_data.extend([
        "|inactive|Battle timer is ON: inactive players will automatically lose when time's up.",
        f"|J|{player1}",
        f"|J|{player2}",
        f"|player|p1|{player1}|#{player1.lower()}",
        f"|player|p2|{player2}|#{player2.lower()}",
        "|gametype|singles",
        "|gen|5",
        "|tier|[Gen 5] Custom Battle",
        "|clearpoke",
    ])
    battle_data.extend(p1_pokes)
    battle_data.extend(p2_pokes)
    battle_data.append("|teampreview")
    battle_data.extend(battle_body)

    return battle_data

def save_html_from_battle_data(battle_data, players, format_type, output_filename):
    log_content = "\n".join(battle_data)

    html_template = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{format_type} replay: {players[0]} vs. {players[1]}</title>
  <style>
    html,body {{font-family:Verdana, sans-serif;font-size:10pt;margin:0;padding:0;}}
    body{{padding:12px 0;}} .subtle {{color:#3A4A66;}}
  </style>
</head>
<body>
  <div class="wrapper replay-wrapper" style="max-width:1180px;margin:0 auto">
    <input type="hidden" name="replayid" value="{players[0]}-vs-{players[1]}" />
    <div class="battle"></div>
    <div class="battle-log">
      <script type="text/plain" class="battle-log-data">
{log_content}
      </script>
    </div>
    <div class="replay-controls"></div>
    <div class="replay-controls-2"></div>
    <h1 style="font-weight:normal;text-align:center">
      <strong>{format_type}</strong><br />
      <a href="http://pokemonshowdown.com/users/{players[0].lower()}" class="subtle" target="_blank">{players[0]}</a> vs.
      <a href="http://pokemonshowdown.com/users/{players[1].lower()}" class="subtle" target="_blank">{players[1]}</a>
    </h1>
  </div>
  <script>
    let daily = Math.floor(Date.now()/1000/60/60/24);
    document.write('<script src="https://play.pokemonshowdown.com/js/replay-embed.js?version=' + daily + '"><\\/script>');
  </script>
</body>
</html>"""

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_template.strip())
    return True

def process_all_txt_files_in_battles_html():
    folder = "battles_html"
    if not os.path.exists(folder):
        print(f"❌ Folder '{folder}' not found.")
        return

    files = [f for f in os.listdir(folder) if f.endswith(".txt")]
    if not files:
        print(f"⚠️ No .txt files found in '{folder}'.")
        return

    for file in files:
        txt_path = os.path.join(folder, file)
        html_filename = file.replace(".txt", ".html")
        html_path = os.path.join(folder, html_filename)

        player1, player2 = get_players_from_txt(txt_path)
        format_type = "[Gen 5] Custom Battle"
        battle_data = parse_battle_log_gen5_from_txt(txt_path, player1, player2)
        success = save_html_from_battle_data(battle_data, [player1, player2], format_type, html_path)

        if success:
            print(f"✅ Converted: {file} → {html_filename} ({format_type})")

# Run it
process_all_txt_files_in_battles_html()

