import json


bosses = []

with open("teams.json", "r") as teams:
    all_teams = json.load(teams)["trainers"]
    for team in all_teams:
        if "Commander" in team["trainer_class"]:
            bosses.append(team)
        elif "Leader" in team["trainer_class"]:
            bosses.append(team)
        elif "Elite Four" in team["trainer_class"]:
            bosses.append(team)
        elif "Champion" in team["trainer_class"]:
            bosses.append(team)

# bosses.sort(key=lambda x: x["rom_id"])  

with open("bosses.json", "w") as bossesfile:
    for i in range(len(bosses)):
        boss = bosses[i]
        bossesfile.write(json.dumps(boss, indent=4) + "\n")
    bossesfile.write("\n")  # Add a newline at the end for better readability