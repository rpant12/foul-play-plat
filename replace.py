import json

# leaders = []

# with open("teams.json", "r") as teams:
#     all_teams = json.load(teams)["trainers"]
#     for team in all_teams:
#         if "Leader" in team["trainer_class"]:
#             leaders.append(team)

# leaders.sort(key=lambda x: x["rom_id"])

with open("leaders.json", "r") as leaders:
    for leader in leaders:
        print(leader)
