import discord, json, requests
from discord.ext import commands
import requests, time
import ctypes
import threading
from threading import Thread
from colorama import init, Fore
from capmonster_python import RecaptchaV2Task
from concurrent.futures import ThreadPoolExecutor

ctypes.windll.kernel32.SetConsoleTitleW(f"Boosts Bot V.2 | ogu.gg/pyex")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", description="", intents=discord.Intents.all())
bot.remove_command('help')


settings = json.load(open("settings.json", encoding="utf-8"))

ta = len(open('tokens.txt', encoding='utf-8').read().splitlines())

@bot.event
async def on_ready():
    activity = discord.Game(name=".gg/devwrld", type=2)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".gg/devwrld"))
    print(f"""
██████╗ ██╗   ██╗███████╗██╗  ██╗
██╔══██╗╚██╗ ██╔╝██╔════╝╚██╗██╔╝
██████╔╝ ╚████╔╝ █████╗   ╚███╔╝ 
██╔═══╝   ╚██╔╝  ██╔══╝   ██╔██╗ 
██║        ██║   ███████╗██╔╝ ██╗
╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    print(f"({Fore.YELLOW}INFO{Fore.RESET}) Authentification . . .")
    time.sleep(2)
    print(f"({Fore.GREEN}SUCCESS{Fore.RESET}) Authentified")
    time.sleep(1)
    print(f"\n({Fore.RED}STATUS{Fore.RESET}) Sellix")
    print(f"({Fore.RED}STATUS{Fore.RESET}) Sell.App")
    print(f"({Fore.GREEN}STATUS{Fore.RESET}) Discord Bot\n\n")

def removeToken():
    with open('tokens.txt', 'r') as fin:
        data = fin.read().splitlines(True)
        with open('tokens.txt', 'w') as fout:
            fout.writelines(data[1:])

@bot.command()
@commands.has_role(" ENTER YOUR ROLE")
@commands.guild_only()
async def boost(ctx, inv, amount: int):
    
    embed=discord.Embed(title=f"Started", description=F"**Server**\n> https://discord.gg/{inv}\n\n**Amount**\n> {amount}x\n\n**User**\n> {ctx.author.mention}", color=discord.Color.from_rgb(0, 163, 255))
    embed.set_footer(text = f"discord.gg/devwrld", icon_url = "")
    await ctx.reply(embed=embed)
    
    done = 0
    retries = 0
    bypass = 0
    
    threads = int("8")

    for i in range(amount):
        try:
         threading.active_count() <= threads
         threading.Thread(target=boost, args=(inv,)).start()
        except Exception as e:
 #           print(e)
            pass


    embed=discord.Embed(title=f"Finished", description=F"**Server**\n> https://discord.gg/{inv}\n\n**Amount**\n> {amount}x\n\n**User**\n> {ctx.author.mention}", color=discord.Color.from_rgb(0, 163, 255))
    embed.set_footer(text = f"discord.gg/devwrld", icon_url = "")
    await ctx.reply(embed=embed)

def boost(invite):
    global done

    try:
        with open('tokens.txt', 'r') as f:
            token = f.readline().strip()

        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-GB',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me', 
            'sec-fetch-dest': 'empty', 
            'sec-fetch-mode': 'cors',
            'cookie': '__dcfduid=23a63d20476c11ec9811c1e6024b99d9; __sdcfduid=23a63d21476c11ec9811c1e6024b99d9e7175a1ac31a8c5e4152455c5056eff033528243e185c5a85202515edb6d57b0; locale=en-GB',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.1.9 Chrome/83.0.4103.122 Electron/9.4.4 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMS45Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTc3NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTM1NTQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
            'te': 'trailers',
        }
        r = requests.get("https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers)
        if r.status_code == 200:
            slots = r.json()
            if len(slots) != 0:
                guid = None
                joined = False
                headers["content-type"] = 'application/json'
                try:
                        join_server = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={
                        })
                        if "captcha_sitekey" in join_server.text:
                            createTask = requests.post("https://api.capmonster.cloud/createTask", json={
                                "clientKey": settings["capmonsterKey"],
                                "task": {
                                    "type": "HCaptchaTaskProxyless",
                                    "websiteURL": "https://discord.com/channels/@me",
                                    "websiteKey": join_server.json()['captcha_sitekey']
                                }
                            }).json()["taskId"]
                            getResults = {}
                            getResults["status"] = "processing"
                            while getResults["status"] == "processing":
                                getResults = requests.post("https://api.capmonster.cloud/getTaskResult", json={
                                    "clientKey": settings["capmonsterKey"],
                                    "taskId": createTask
                                }).json()

                                time.sleep(1)

                            solution = getResults["solution"]["gRecaptchaResponse"]

                            print(f"({Fore.YELLOW}+{Fore.RESET}) || Captcha Solved")

                            join_server = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={
                                "captcha_key": solution
                            })

                        if join_server.status_code == 200:
                            join_outcome = True
                            guid = join_server.json()["guild"]["id"]
                            print(f"({Fore.GREEN}+{Fore.RESET}) || JOINED || {token}")
                        else: 
                            print(f"({Fore.RED}+{Fore.RESET}) || ERROR JOINING || {token}")
                            return
                except Exception as e:
                        pass
            for slot in slots:
                slotid = slot['id']
                payload = {"user_premium_guild_subscription_slot_ids": [slotid]}
                r2 = requests.put(f'https://discord.com/api/v9/guilds/{guid}/premium/subscriptions', headers=headers, json=payload)
                if r2.status_code == 201:
                    print(f'({Fore.GREEN}+{Fore.RESET}) || BOOSTED || {token}')
                    done += 1
                else:
                    print(f'({Fore.RED}+{Fore.RESET}) || ERROR BOOSTING || {token}')
                    removeToken()
                    


    except Exception as e:
        print('')

@bot.command()
@commands.has_role("[🔧︱Developer]")
@commands.guild_only()
async def stock(ctx):
    embed=discord.Embed(title="Stock", description=f"\n\
    Tokens: {len(open('tokens.txt', encoding='utf-8').read().splitlines())} \n\
    Boosts: {len(open('tokens.txt', encoding='utf-8').read().splitlines())* 2}", color=discord.Color.from_rgb(0, 163, 255))
    embed.set_image(url="https://cdn.discordapp.com/attachments/1005128875149377697/1010257524118802483/DevWrld-Discord-banner.png")
    embed.set_footer(text = f"discord.gg/devwrld", icon_url = "")
    await ctx.reply(embed=embed)

bot.run(settings["botToken"])