import discord
from discord.ext import commands, tasks
import requests as r
import json
import pandas as pd
from pandas import json_normalize
import mysql.connector as mysql
import time
import urllib.request
import insightly
from datetime import date, datetime
import main

bot = commands.Bot(command_prefix="", case_insensitive=True, help_command=None)


@tasks.loop(seconds=10)
async def statusupdate():
    await bot.wait_until_ready()
    chan = bot.get_channel(956638982593216513)

    print("starting hotspot status check")

    r1 = insightly.hotspots_data()
    insightly.verify_nodes()
    r2 = insightly.hotspots_data()

    changed = [item for item in r2 if item not in r1]

    if len(changed) > 0:
        mydb = mysql.connect(
            host="neodbinstance.cqieshqdcqmd.us-east-2.rds.amazonaws.com",
            user="neoadmin", password="mycelium1", database="neodb"
        )
        for item in changed:
            my_cursor = mydb.cursor()
            sql = f"UPDATE hotspots SET status = '{item['status']}' WHERE address = '{item['address']}'"
            my_cursor.execute(sql)
        print("Updated status table")

        for item in changed:
            statusmsg = f"{item['name']}, a {item['level']} {item['hardware']}, has changed status to {item['status']}"
            embed = discord.Embed(title="__Status Change Alert__", description="", color=0x109319)
            embed.add_field(name="Alert", value=statusmsg, inline=False)
            await chan.send(embed=embed)

    print("Reached end of hotspot status update.")


    # # Create an empty dataframe/table with pandas (pd) named "nodes" as a starting reference
    # # For each wallet address fetch the list of hotspots from the API
    # # Append output of hotspots for each wallet address to "hotspots" table
    #
    # hotspots = pd.DataFrame()
    #
    # #Insightly Data for Hotspot status checker
    #
    # # record the time of data retrieval
    # timefetched = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print("built hotspot table")
    #
    # # Compare statuses between tables and build a status msg list to be inserted into the comments mysql table
    #
    #
    #
    # hotspots['status.timestamp'] = hotspots['status.timestamp'].str[:19]
    # hotspots['status.timestamp'] = hotspots['status.timestamp'].astype('datetime64[ns]')
    #
    # statusmsglist = []
    # for a in addrs:
    #     laststatusrow = laststatustable[laststatustable['address']==a].reset_index()
    #     laststatus = laststatusrow['status'][0]
    #     statustime = laststatusrow['timestamp'][0]
    #     try:
    #         hourmin = statustime.strftime("%H:%M")
    #         datestr = statustime.strftime("%m-%d-%Y")
    #         t = time.strptime(hourmin, "%H:%M")
    #         fixedtime = time.strftime( "%I:%M %p", t )
    #     except TypeError:
    #         fixedtime = "N/A"
    #
    #     newrow = hotspots[hotspots['address']==a].reset_index()
    #     name = newrow['name'][0]
    #     newstatus = newrow['status.online'][0]
    #     newstatustime = newrow['status.timestamp'][0]
    #
    #
    #
    #     if newstatus == 'offline':
    #         newstatus = 'OFFLINE'
    #     if newstatus.lower() != laststatus:
    #         #statusmsg = name + " last changed status to " + laststatus + " on " + datestr + " at " + fixedtime + " and is now " + newstatus + " (" + laststatus + " for " + elapsed + "hours)"
    #         statusmsg = "**"+ name + "** last changed status to " + laststatus + " on " + datestr + " at " + fixedtime + " and is now " + "**"+newstatus+"**"
    #         embed=discord.Embed(title="__Status Change Alert__", description="", color=0x109319)
    #         embed.add_field(name="Alert", value=statusmsg, inline=False)
    #         await chan.send(embed=embed)
    #         #statusmsglist.append(statusmsg)
    #         updates = updates.append({"address":a,"statusnew":newstatus.lower(),"timenew":newstatustime},ignore_index=True)
    #
    #     else:
    #         continue

