from aiohttp import web
from .converter import docx_to_pdf
import os


app = web.Application()
app.router.add_post('/docx_to_pdf', docx_to_pdf)
web.run_app(app, port=int(os.getenv('PORT', "7777")))
