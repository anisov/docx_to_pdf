import os
import re
import tempfile
import subprocess
import aiofiles
from aiohttp import web
from .logger import logger
from .exception import LibreOfficeError
import logging
logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), f'logs/exceptions.txt'),)


def convert(folder: str, source: str, timeout: int = 60) -> None:
    args = ['/usr/bin/soffice', '--headless', '--convert-to', 'pdf', '--outdir', folder, source]
    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    filename = re.search('-> (.*?) using filter', process.stdout.decode())

    if not filename:
        raise LibreOfficeError('Error')


async def docx_to_pdf(request):
    tf_name = tempfile.NamedTemporaryFile().name
    async with aiofiles.open(tf_name, mode='wb') as file:
        reader = await request.multipart()
        doc = await reader.next()
        doc_data = await doc.read()

        await file.write(doc_data)
        await file.flush()

        convert(os.path.abspath(os.path.dirname(tf_name)), os.path.abspath(tf_name))

        response = web.StreamResponse(status=200)
        response.content_type = 'application/pdf'
        await response.prepare(request)

        pdf_name = "{}.pdf".format(tf_name)
        try:
            async with aiofiles.open(pdf_name, 'rb') as pdf:
                pdf_data = await pdf.read()
                await response.write(pdf_data)
                await pdf.flush()
        except Exception as ex:
            await logger.error(f'Error: {ex}')
            response = web.Response(status=400)

        await logger.info('ok')
        os.remove(tf_name)
        os.remove(pdf_name)
        return response
