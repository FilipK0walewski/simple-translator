import aiohttp
import aioredis
import json
import os
import requests

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

redis, session = None, None
app = FastAPI()


@app.on_event('startup')
async def app_startup():
    global redis, session
    redis = aioredis.from_url("redis://localhost", decode_responses=True)
    api_key = os.environ.get('DEEPL_API_KEY')
    print(api_key)
    session = aiohttp.ClientSession(headers={'Authorization': f'DeepL-Auth-Key {api_key}'})


@app.on_event('shutdown')
async def app_shutodwn():
    await redis.close()
    await session.close()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/')
async def translate(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'input': None, 'result': None, 'target_lang': None, 'source_lang': None})


@app.get('/result')
async def get_result(request: Request, text: str, source_lang: str, target_lang: str):
    key = f'tranlation.{source_lang}.{target_lang}.{text}'
    cached = await redis.get(key)
    if cached is not None:
        data = json.loads(cached)
        return templates.TemplateResponse('index.html', {'request': request, 'input': text, 'result': data['translations'][0]['text'], 'target_lang': target_lang, 'source_lang': source_lang})

    payload = {'text': text, 'source_lang': source_lang, 'target_lang': target_lang}
    async with session.post('https://api-free.deepl.com/v2/translate', data=payload) as res:
        data = await res.json()
        await redis.set(key, json.dumps(data))
        return templates.TemplateResponse('index.html', {'request': request, 'input': text, 'result': data['translations'][0]['text'], 'target_lang': target_lang, 'source_lang': source_lang})
