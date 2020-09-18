import subprocess
import json
import functools
import os
import aiohttp

def youtube_(query, filename):
    filename = f"{filename}.json"
    subprocess.call(f'youtube-dl -j --dump-json "ytsearch1:{query}" > {filename}', shell=True)

    try:
        with open(filename, "r") as f:
          l = json.load(f)

        os.remove(filename)
        
        return f"https://youtube.com/watch?v={l['id']}"

    except:
        os.remove(filename)
        return None

async def youtube(query, filename, loop):
    "Get a youtube url by a query"
    
    function = functools.partial(youtube_, query, filename)
    video = await loop.run_in_executor(None, function)
    return video

async def mystbin(data):
    data = bytes(data, 'utf-8')
    async with aiohttp.ClientSession() as cs:
        async with cs.post('https://mystb.in/documents', data = data) as r:
            res = await r.json()
            key = res["key"]
            return f"https://mystb.in/{key}"

    await cs.close()

def pull_():
    os.system("git pull origin master")

def push_():
    os.system("git add .")
    os.system('git commit -m "added things"')
    os.system('git push origin master')

class Git:

    async def pull(self, loop):
        function = functools.partial(pull_)
        await loop.run_in_executor(None, function)

    async def push(self, loop):
        function = functools.partial(push_)
        await loop.run_in_executor(None, function)
