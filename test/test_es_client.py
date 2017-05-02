import unittest
from config import config
from unittest.mock import patch, MagicMock
from helpers.es_client import ElasticSearchClient

class TestElasticSearchClient(unittest.TestCase):

    def test_singleton_on_es_client(self):
        with patch.dict(config, {'es_host': 'host', 'es_port': 100, 'es_index': 'test_index'}, clear=True):
            x = ElasticSearchClient.Instance()
            y = ElasticSearchClient.Instance()
            self.assertEqual(x, y)

    def test_article_insertion(self):
        with patch.dict(config, {'es_host': 'host', 'es_port': 100, 'es_index': 'test_index'}, clear=True):
            client = ElasticSearchClient.Instance()
            client.insert_article = MagicMock(return_value=True)
            article = {'id': '1', 'title': 'Title', 'body': 'BodyText', 'tags': ['test', 'tag'], 'date': '2017-03-10'}
            result = client.insert_article(article)
            client.insert_article.assert_called_with(article)
            assert result == True


if __name__ == '__main__':
    unittest.main()