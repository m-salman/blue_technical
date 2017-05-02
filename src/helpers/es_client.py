import time
import logging
from config import config
from helpers.singleton import Singleton
from elasticsearch import Elasticsearch, ElasticsearchException

logger = logging.getLogger(__name__)

@Singleton
class ElasticSearchClient:
    def __init__(self):
        try:
            self.index = config['es_index']
            self.es_client = Elasticsearch(hosts=[{'host': config['es_host'], 'port': config['es_port']}])

        except ElasticsearchException:
            logger.exception("msg=Exception while trying to connect to ElasticSearch "
                             "| Host={} | Port={}".format(config['es_port'], config['es_port']))

    def insert_article(self, article):
        try:
            logger.info("msg=Inserting article into ElasticSearch | Article={}".format(article))
            article.update({'epoch': int(time.time())})
            self.es_client.update(index=self.index,
                                  doc_type='article',
                                  id=article['id'],
                                  body={'doc': article, 'doc_as_upsert': True})
            return True

        except ElasticsearchException:
            logger.exception("msg=Failed to fetch article from ElasticSearch | ArticleID={}".format(article['id']))
            return False

    def fetch_article(self, article_id):
        try:
            logger.info("msg=Fetching article with Article ID | ID={}".format(article_id))

            result = self.es_client.get(index=self.index, doc_type='article', id=article_id,
                                        _source_include=['id', 'title', 'body', 'tags', 'date'])
            if not result:
                logger.warning("msg=ArticleID not found in ElasticSearch | ArticleID:{}".format(article_id))
                return None

            return result['_source']

        except ElasticsearchException:
            logger.exception("msg=Failed to fetch article from ElasticSearch | ArticleID={}".format(article_id))
            return None

    def fetch_articles_using_tag(self, tag, date):
        try:
            articles = list()
            logger.info("msg=Searching ES clsuter for articles | Tag:{} | Date:{}".format(tag, date))
            response = self.es_client.search(index=self.index,
                                             doc_type='article',
                                             body=
                                             {
                                                 "query": {
                                                     "bool": {
                                                         "must": [
                                                             {
                                                                 "term": {
                                                                     "tags": {"value": tag}
                                                                 }
                                                             },
                                                             {
                                                                 "range": {
                                                                     "date": {
                                                                         "from": date,
                                                                         "to": date
                                                                     }
                                                                 }
                                                             }
                                                         ]
                                                     }
                                                 }
                                             })

            if not response:
                logger.warning("msg=Tag not found in ElasticSearch | Tag:{}".format(tag))
                return articles

            for record in response['hits']['hits']:
                articles.append(dict(record['_source']))

            return articles

        except ElasticsearchException:
            logger.exception("msg=Exception while trying to fetch tags from Elastic Search")
            return []
