import discord
import asyncio
import datetime
import os
import subprocess
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
client = discord.Client(intents=intents)


# サーバーリストを読み込む関数
def load_server_list():
    server_list = []
    # サーバーリストファイルがない場合、作成
    if not os.path.exists("server_list.txt"):
        with open("server_list.txt", 'w') as f:
            f.write('')
    # サーバーリストファイルがある場合は、読み込む
    with open("server_list.txt") as f:
        for line in f:
            server_name, server_ip = line.strip().split(",")
            server_list.append((server_name, server_ip))
    return server_list

# ping結果を取得する関数
def get_ping_results(server_list):
    ping_results = []
    for server_name, server_ip in server_list:
        # subprocess.runを使用してpingコマンドを実行
        result = subprocess.run(["ping", "-n", "1", server_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print(result)
        ping_status = "🟢稼働中" if result.returncode == 0 else "🛑停止中"
        color = 0x00FF00 if result.returncode == 0 else 0xFF0000
        ping_results.append((server_name, ping_status, color))
    return ping_results


# embedを更新する関数
async def update_embed(client, ping_results):
    message_id = 1251117537509507225
    channel_id = 993406780262592532
    now_tokyo = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    now_time = now_tokyo.strftime("%Y/%m/%d %H:%M:%S")
    embed_data = discord.Embed(
        title="サーバー死活監視", description="監視情報一覧"
    )
    for server_name, ping_status, _ in ping_results:
        embed_data.description
        embed_data.add_field(
            name=server_name, value=ping_status, inline=False
        )
    embed_data.set_footer(text="Updated: " + now_time)
    color = 0xFF0000 if any(status == "🛑停止中" for _, status, _ in ping_results) else 0x00FF00
    embed_data.color = color
    channel = client.get_channel(channel_id)
    message = await channel.fetch_message(message_id) if message_id else None
    if message:
        await message.edit(embed=embed_data)
    else:
        message = await channel.send(embed=embed_data)
        message_id = message.id

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    while True:
        server_list = load_server_list()
        ping_results = get_ping_results(server_list)
        await update_embed(client, ping_results)
        await asyncio.sleep(30)

@client.event
async def on_message(message):
    if message.content.startswith("!server_add"):
        command = message.content.split(" ")
        if len(command) == 3:
            server_name, server_ip = command[1], command[2]
            with open("server_list.txt", "a") as f:
                f.write(f"{server_name},{server_ip}\n")
            await message.channel.send("サーバーを追加しました")
        else:
            await message.channel.send("サーバー名とIPアドレスを入力してください")

    elif message.content.startswith("!server_remove"):
        command = message.content.split(" ")
        if len(command) == 2:
            server_name = command[1]
            server_list = load_server_list()
            server_list = [(name, ip) for name, ip in server_list if name != server_name]
            with open("server_list.txt", "w") as f:
                f.writelines(f"{name},{ip}\n" for name, ip in server_list)
            await message.channel.send("サーバーを削除しました")
        else:
            await message.channel.send("サーバー名を入力してください")

client.run(os.environ["DISCORD_TOKEN"])
