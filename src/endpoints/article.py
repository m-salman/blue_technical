import json
import bottle
import logging
from src.helpers.es_client import ElasticSearchClient
from src.helpers.response_helper import build_response

logger = logging.getLogger(__name__)
app = bottle.Bottle()


@app.post('/articles')
def post_article():
    req_params = bottle.request.json
    if not req_params and not _is_valid_request(req_params):
        logger.warning('msg=Invalid POST body or bad request')
        return bottle.HTTPResponse(status=400, body=build_response(400, 'Bad or malformed request'))

    es_client = ElasticSearchClient.Instance()

    if es_client.insert_article(req_params):
        return bottle.HTTPResponse(status=200, body=build_response(200, 'Success'))
    else:
        return bottle.HTTPResponse(status=500, body=build_response(500, 'Server error, failed to process article!'))


@app.get('/articles/<article_id>')
def get_article(article_id):
    es_client = ElasticSearchClient.Instance()

    article = es_client.fetch_article(article_id)

    if not article:
        return bottle.HTTPResponse(status=500, body=build_response(500, 'Server error, failed to process article!'))
    else:
        return bottle.HTTPResponse(status=200, body=json.dumps(article))


def _is_valid_request(req_params):
    if all(key in req_params for key in ['id', 'tags', 'body', 'title', 'date']):
        return True
    else:
        False
