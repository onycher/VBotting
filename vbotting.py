from sourceserver.sourceserver import SourceServer
import requests
import time
import os


def log_player(connecteds, names, count, players_info):
    players_info = [p for p in players_info if p[1] != ""]
    content = "> Players: {}/40\n> \n> Player list:\n".format(len([p for p in players_info if p[1] != ""]))
    for idx, player in enumerate(sorted(players_info, key=lambda p: p[2], reverse=True)):
        content += "> {}. **{}** ({} GL)\n".format(idx+1, player[1], player[2])
    for connected, name in zip(connecteds, names):
        if connected:
            content += "> \n``` {} just connected to the server```".format(name)
        else:
            content += "> \n``` {} just left the server```".format(name)

    
    data = {
        "content" : content,
    }
    
    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

url = os.getenv("DISCORD_WEBHOOK")
server_ip = os.getenv("SERVER_IP")

server = SourceServer(server_ip)
_, old_players = server.getPlayers()
old_players = {p[1] for p in old_players if p[1]}

while True:
    try:
        count, players_info = server.getPlayers()
    except:
        time.sleep(10)
        continue
    players = {p[1] for p in players_info if p[1]}
    c = []
    n = []
    for p in players-old_players:
        c.append(True)
        n.append(p)
    for p in old_players-players:
        c.append(True)
        n.append(p)
    log_player(c, n, count, players_info)
    old_players = players

    time.sleep(10)


