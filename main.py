import asyncio
import pandas as pd
import httpx
import time

FILE_NAME = 'data.xlsx'


async def solved(username):
    url = 'https://ojhunt.com/api/crawlers/codeforces/'+username
    print(url)
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
    print(r)
    json = r.json()
    if(json['error']):
        print('API ERROR')
        return -1
    else:
        return json['data']['solved']


async def cfrank(username):
    url = 'https://codeforces.com/api/user.info'
    params = {'handles': username}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
    json = r.json()
    print(type(json))
    if 'rating' not in json['result'][0]:
        return 0
    return json['result'][0]['rating']


async def main():
    df = pd.read_excel(FILE_NAME, header=0)
    today_solved, today_rank = [], []
    for id in df['CFID']:
        today_solved.append(await solved(id))
        today_rank.append(await cfrank(id))
        await asyncio.sleep(5) # API接口访问有限制，所以要间隔 5s
        print(f'{id} {str(today_solved[-1])} {str(today_rank[-1])} \n')

    df[f'CF做题数_{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}'] = today_solved
    df[f'CF天梯分_{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}'] = today_rank
    print(df)
    df.to_excel(FILE_NAME)

asyncio.run(main())
