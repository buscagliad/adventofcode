#!/usr/bin/env python
'''
This script will grab the leaderboard from Advent of Code and print it
'''
# pylint: disable=wrong-import-order
# pylint: disable=C0301,C0103,C0209

import os
import datetime
import sys
import json
import requests
import time
import players as pl
import functools

LEADERBOARD_ID = os.environ.get('LEADERBOARD_ID')
SESSION_ID = os.environ.get('SESSION_ID')

# If the ENV Var hasn't been set, then try to load from local config.
# Simply create secrets.py with these values defined.
# See README for more detailed directions on how to fill these variables.
if not all([LEADERBOARD_ID, SESSION_ID]):
	from secrets import LEADERBOARD_ID, SESSION_ID

# You should not need to change this URL
LEADERBOARD_URL = "https://adventofcode.com/{}/leaderboard/private/view/{}".format(
		datetime.datetime.today().year,
		LEADERBOARD_ID)


def printMembers(members):
	"""
	Format the message to conform to Slack's API
	"""
	message = ""

	# add each member to message
	medals = [':third_place_medal:', ':second_place_medal:', ':trophy:']
	for username, score, stars in members:
		if medals:
			medal = ' ' + medals.pop()
		else:
			medal = ''
		message += f"{medal}*{username}* {score} Points, {stars} Stars\n"


	return message


def parseMembers(members_json):
	"""
	Handle member lists from AoC leaderboard
	"""
	# get member name, score and stars
	members = [(m["name"],
				m["local_score"],
				m["stars"]
				) for m in members_json.values()]

	# sort members by score, descending
	members.sort(key=lambda s: (-s[1], -s[2]))

	return members

def playerList(members_json):
	members = [(m["name"],
				m["stars"],
				m["last_star_ts"],
				m["id"],
				m["completion_day_level"]
				) for m in members_json.values()]
	plist = []
	for name, stars, laststar, playerID, dayResults in members:
		#print(playerID, name, pl.getPlayerName(playerID))
		p = pl.Player(playerID, stars, laststar)
		#print("**************** ", name, " ************************")
		#print()
		tm = time.localtime(laststar)
		stm = time.strftime("%d %b %Y %H:%M:%S", tm)
		#print(" Number of stars: ", stars, " Last Star: ", stm);
		#print(dayResults)
		#for day in dayResults:
			#print("3", " a: ", day, "  ", dayResults[day])
			#for k in dayResults[day]:
				#tm = time.localtime(dayResults[day][k]["get_star_ts"])
				#stm = time.strftime("%d %b %Y %H:%M:%S", tm)
				#print("k ", k, dayResults[day][k]["get_star_ts"], stm)

		for day in dayResults:
			t1 = 0
			t2 = 0
			for part in dayResults[day]:
				if part == '1': t1 = dayResults[day][part]["get_star_ts"]
				if part == '2': t2 = dayResults[day][part]["get_star_ts"]
			#print(day, t1, t2, part)
			p.addDay(int(day), t1, t2)
		plist.append(p)
	plist.sort(key=functools.cmp_to_key(pl.plcomp))
	return plist

def outCSV(members_json):
	"""
	Handle member lists from AoC leaderboard
	"""
	# get member name, score and stars
	members = [(m["name"],
				m["local_score"],
				m["stars"],
				m["last_star_ts"],
				m["completion_day_level"]
				) for m in members_json.values()]
	for q in members:
		print("**************** ", q[0], " ************************")
		print()
		tm = time.localtime(q[3])
		stm = time.strftime("%d %b %Y %H:%M:%S", tm)
		print("Score: ", q[1], " Number of stars: ", q[2], " Last Star: ", stm);
		for j in q[4]:
			print("3", " j: ", j, "  ", q[4][j])
			for k in q[4][j]:
				tm = time.localtime(q[4][j][k]["get_star_ts"])
				stm = time.strftime("%d %b %Y %H:%M:%S", tm)
				print("k ", q[4][j][k]["get_star_ts"], stm)
		print()
		print()
			#print(j)
		#if not q[3]["3"] is None:
		#	print(q[3]["3"])

		#print(pretty_json)
		#for g in m[3]:
		#	print("Game ", g)
		#	for d in g:
		#		print("Day ", d)
	

def main():
	"""
	Main program loop
	"""
	# make sure all variables are filled
	if LEADERBOARD_ID == "" or SESSION_ID == "" :
		print("Please update script variables before running script.\n\
				See README for details on how to do this.")
		sys.exit(1)

	# retrieve leaderboard
	r = requests.get(
		"{}.json".format(LEADERBOARD_URL),
		timeout=60,
		cookies={"session": SESSION_ID}
	)
	if r.status_code != requests.codes.ok:  # pylint: disable=no-member
		print("Error retrieving leaderboard")
		sys.exit(1)

	# get members from json
	members = parseMembers(r.json()["members"])
	
	
	# output csv from JOSN
	# outCSV(r.json()["members"])
	pList = playerList(r.json()["members"])
	n = 0
	for p in pList:
		if (n == 0) :
			p.simpleout(0)
			n += 1
		p.simpleout(n)
		n += 1

if __name__ == "__main__":
	main()
