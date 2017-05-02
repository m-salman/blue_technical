import os
import yaml
import bottle
import logging
from bottle_swagger import SwaggerPlugin

# Install Swagger plugin for Bottle, please see details at
# https://github.com/ampedandwired/bottle-swagger


logger = logging.getLogger(__name__)

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
assets_path = os.path.join(root_path, 'src/assets')


def _load_swagger_def():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open("{}/swagger.yml".format(this_dir), 'r') as f:
        _swagger_def = yaml.load(f)

    return _swagger_def

swagger_def = _load_swagger_def()
bottle.install(SwaggerPlugin(swagger_def))

# Setup swagger endpoints
app = bottle.Bottle()

@app.get('/')
def index_redirect():
    bottle.redirect("/api-docs/")

@app.get('/api-docs')
def api_docs_redirect():
    bottle.redirect("/api-docs/")

@app.get('/api-docs/')
def api_docs_index():
    return bottle.static_file("index.html", root=os.path.join(assets_path, 'swagger-ui'))

@app.get('/api-docs/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root=os.path.join(assets_path, 'swagger-ui'))
