from sourceserver.sourceserver import SourceServer
import requests
import time
import os


def log_player(text, name):
    data = {
    }
    data["embeds"] = [
        {
            "description" : name,
            "title" : text
        }
    ]
    
    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

url = os.getenv("DISCORD_WEBHOOK")
server_ip = os.getenv("SERVER_IP")

server = SourceServer(server_ip)
_, old_players = server.getPlayers()
old_players = {p[1] for p in old_players if p[1]}

while True:
    _, players = server.getPlayers()
    players = {p[1] for p in players if p[1]}
    
    print(players-old_players)
    print(old_players-players)
    print("============")
    for p in players-old_players:
        log_player("Player connected", p)
    for p in old_players-players:
        log_player("Player disconnected", p)
    
    old_players = players

    time.sleep(10)


