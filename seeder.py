#!/usr/bin/env python
# @author jhertz
# script to seed a challonge bracket using GARPR
import challonge
import requests

id = ""

region = "nyc"

def init_challonge(username, api_key):
    challonge.set_credentials(username, api_key)

def get_participants():
    raw_participants = challonge.participants.index(id)
    return [ x['name'] for x in raw_participants]

def seed_participants( participants):
	ratings = dict()
	for p in participants:
		ratings[p] = lookup_garpr_rating(p)
		print "rating for", p, " is:", lookup_garpr_rating(p)
	participants.sort(key= lambda p : ratings[p])

def update_seeding( ranked):
	for i, p in enumerate(ranked):
		challonge.participants.update(id, p, seed=i)


def lookup_garpr_rating(player):
	r = requests.get("http://api.garpr.com/" + region + "/players?alias=" + player)
	print "recv'd:", r.text
	info = r.json()
	return float(info["ratings"][region]["mu"])










if __name__ == "__main__":
    api_key = ""
    username = ""
    global id 

    with open("bracket.txt") as bracket_file:
        id = bracket_file.readline().rstrip()


    if not id:
        print "failed to read bracket id, exiting"
        exit(-3)

    with open("creds.txt") as creds_file:
        username = creds_file.readline().rstrip()
        api_key = creds_file.readline().rstrip()


    if not api_key:
        print "failed to read api key, exiting"
        exit(-1)

    if not username:
        print "failed to read username, exiting"
        exit(-2)


    init_challonge(username, api_key)
    print "going to seed tourney id:", id
    participants = get_participants()
    print "got participants:", participants
    seed_participants(participants)
    print "seeded participants:", participants
    #update_seeding(participants)
    print "done!"

