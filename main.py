import fastapi
import base64
from fastapi.responses import StreamingResponse
#from starlette.responses import StreamingResponse
from urllib3 import Retry
import aiohttp
app = fastapi.FastAPI()


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
    'Accept': 'image/avif,image/webp,*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.picuki.com/',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0.2',
    'Cache-Control': 'max-age=0',
    'TE': 'trailers',
}


def EncodeUrl(url):
    return base64.urlsafe_b64encode(bytes(url, 'utf-8')).decode("UTF-8")


def DecodeUrl(urlE):
    return base64.urlsafe_b64decode(bytes(urlE, 'utf-8')).decode("UTF-8")


async def read(session, u):
    async with session.get(u) as r:
        async for data, _ in r.content.iter_chunks():
            yield data
    await session.close()


@app.get("/cdn")
async def proxy(url: str = ""):
    u = DecodeUrl(url)
    session = aiohttp.ClientSession()
    rheaders = {}
    rheaders['Access-Control-Allow-Origin'] = '*'
    return StreamingResponse(read(session, u), headers=rheaders)
