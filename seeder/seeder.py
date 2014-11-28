#!/usr/bin/env python
# @author jhertz
# script to seed a challonge bracket using GARPR
import challonge
import requests
import random


tourney_id = ""
region = "nyc"

def init_challonge(username, api_key):
    challonge.set_credentials(username, api_key)

def get_participants():
    raw_participants = challonge.participants.index(tourney_id)
    return raw_participants

def seed_participants( participants):
	ratings = dict()
	names = [ x['name'] for x in participants]
	for n in names:
		ratings[n] = lookup_garpr_rating(n)
		print "rating for", n, " is:", ratings[n]
	participants.sort(key= lambda p : ratings[p['name']])
	participants.reverse()
	print "testing sorting"
	for p in participants:
		print "ordered:", p['name']



def update_seeding(participants):
	for i, p in enumerate(participants):
		print "seeded", p['id'], "AKA", p['name'], "as seed#", i+1
		challonge.participants.update(tourney_id, p['id'], seed=i+1)


def lookup_garpr_rating(player):
	#return random.randint(1,100)
	r = requests.get("http://api.garpr.com/" + region + "/players?alias=" + player)
	#print "recv'd:", r.text
	info = r.json()
	if not info["players"]:
		return -9999
	gar_id = info["players"][0]["id"]
	print "GARPR ID:", gar_id
	uri = "http://api.garpr.com/" + region + "/players/" + gar_id
	print "uri:", uri
	r = requests.get(uri)
	print "recv'd:", r.text
	info = r.json()
	rating =  float(info["ratings"][region]["mu"])
	print "rating:", rating
	return rating
	#return float(info["ratings"][region]["mu"])
	#return 0










if __name__ == "__main__":
    api_key = ""
    username = ""
    global tourney_id 

    with open("bracket.txt") as bracket_file:
        tourney_id = bracket_file.readline().rstrip()


    if not tourney_id:
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
    print "going to seed tourney id:", tourney_id
    participants = get_participants()
    #print "got participants:", participants
    seed_participants(participants)
    #print "seeded participants:", participants
    update_seeding(participants)
    print "done!"

