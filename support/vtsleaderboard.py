#!/usr/bin/python3
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
    from secrets import LEADERBOARD_ID, SESSION_ID, AOC_YEAR

# You should not need to change this URL
LEADERBOARD_URL = "https://adventofcode.com/{}/leaderboard/private/view/{}".format(
        AOC_YEAR,
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
        # print(dayResults)
        # for day in dayResults:
            # print("3", " a: ", day, "  ", dayResults[day])
            # for k in dayResults[day]:
                # tm = time.localtime(dayResults[day][k]["get_star_ts"])
                # stm = time.strftime("%d %b %Y %H:%M:%S", tm)
                # print("k ", k, dayResults[day][k]["get_star_ts"], stm)

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

def outCSV(pList):
    """
    Handle member lists from AoC leaderboard
    """
    f = open("aoc.csv", "w")
    pList[0].csvOut(f, True)
    for p in pList:
        p.csvOut(f)
    f.close()

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
        print("Error retrieving leaderboard", LEADERBOARD_URL)
        sys.exit(1)

    # get members from json
    members = parseMembers(r.json()["members"])
    
    pList = playerList(r.json()["members"])
    
    # output csv from playerList
    outCSV(pList)
    n = 0
    pList[0].simpleout(n)
    for p in pList:
        n += 1
        p.simpleout(n)

if __name__ == "__main__":
    main()
