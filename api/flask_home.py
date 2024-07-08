import logging
import json
from config import *


from quart import Quart, jsonify, redirect, render_template, \
    make_response, abort
from book_routes import books_page

from auth import api_key_required

from quart_schema import QuartSchema

from model.sql_connect import get_session, engine, Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Quart('Book Suggesstion')
QuartSchema(app,
            security=[{"app_id": []}],
            security_schemes={"app_id": {"type": "apiKey", "name": "X-API-KEY", "in_": "header"}},)

app.register_blueprint(books_page)

app.config['NAME'] = 'BooksSuggestion'
app.config['VERSION'] = '0.0.1'
app.config['VERSION_APP'] = 'v0.0'
app.config['API_KEY'] = 'ganesh'
#app.config['BASIC_AUTH_PASSWORD'] = 'ganesh'


@app.before_serving
async def start_app():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


#@validate_headers(Headers)
@app.route('/home')
@app.route('/index')
@app.route('/root')
@app.route('/')
@api_key_required()
async def index():
    return 'Books App is running'



if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1',port='80')

    except Exception as err:
        logger.error(err)