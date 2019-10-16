import asyncio
import aiohttp
import aiofiles
import os
from aiohttp.formdata import FormData


async def write_image(data):
    files_path = 'files'
    if not os.path.exists(files_path):
        os.makedirs(files_path)
    async with aiofiles.open(f'{files_path}/out.pdf', mode='wb') as file:
        await file.write(data)


async def fetch_content(url, session):
    async with aiofiles.open("input.docx", mode='rb') as file:
        data = FormData()
        data.add_field('file', file, filename='_.docx')
        async with session.post(url, data=data) as response:
            data = await response.read()
            await write_image(data)


async def main():
    url = 'http://0.0.0.0:7777/docx_to_pdf'
    tasks = []
    async with aiohttp.ClientSession() as session:
        for _ in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
