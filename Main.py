import asyncio
import random
import threading
import requests
import time
from flask import Flask
import yaylib

# --- 設定 ---
EMAIL = "arakiyuujirou1@gmail.com"
PASS = "Yukie0331"
# Renderから割り当てられるURL（作成後に確認してここを書き換えてください）
APP_URL = "https://araki-bot.onrender.com" 

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Alive"

# 15分ごとのスリープを防ぐ「自分起こし」機能
def poke_myself():
    while True:
        try:
            requests.get(APP_URL)
            print("Self-poke successful")
        except: pass
        time.sleep(600) # 10分おき

def run_server():
    app.run(host='0.0.0.0', port=10000)

async def main_logic():
    client = yaylib.Client()
    client.login(EMAIL, PASS)
    processed_ids = set()
    
    while True:
        try:
            timeline = client.get_timeline(number=20)
            posts = timeline.posts if timeline else []
            for p in posts:
                if not p.liked and p.id not in processed_ids:
                    client.like(p.id)
                    processed_ids.add(p.id)
                    # サーバーIPなので少し攻めてもnnaに影響なし！
                    await asyncio.sleep(random.uniform(3.0, 6.0))
            
            if len(processed_ids) > 1000: processed_ids.clear()
            await asyncio.sleep(random.uniform(10, 20))
            
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(300)

async def run_all():
    # サーバーとボットを同時に動かす
    threading.Thread(target=run_server, daemon=True).start()
    threading.Thread(target=poke_myself, daemon=True).start()
    await main_logic()

if __name__ == "__main__":
    asyncio.run(run_all())
