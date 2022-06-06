from sourceserver.sourceserver import SourceServer
import requests
import time
import os


def log_player(connected, name, count, players_info):
    content = "```Players: __{}/40__\n\nPlayer list:".format(count)
    for idx, player in enumerate(players_info):
        content += "{}. {} ({} GL)\n".format(idx, player[1], player[2])
    if connected:
        content += "```\n> **{}** just connected to the server".format(name)
    else:
        content += "```\n> **{}** just left the server".format(name)

    
    data = {
        "content" : content,
    }
    
    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

url = "https://discordapp.com/api/webhooks/983371162316836935/M3EGwM-n8Atr0z3VgCZ2eYvx1xGVwdVyiIMVtjNQLch23wHJJ_Nt5LWFXxklBw-nVAwg" #os.getenv("DISCORD_WEBHOOK")
server_ip = "185.239.211.117:30515" #os.getenv("SERVER_IP")

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
    for p in players-old_players:
        log_player(True, p, count, players_info)
    for p in old_players-players:
        log_player(False, p, count, players_info)
    
    old_players = players

    time.sleep(10)


