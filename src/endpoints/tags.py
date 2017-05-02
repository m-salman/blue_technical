import bottle
import logging
from datetime import datetime
from src.helpers.es_client import ElasticSearchClient
from src.helpers.response_helper import build_response

logger = logging.getLogger(__name__)
app = bottle.Bottle()


@app.get('/tags/<tag_name>/<date>')
def fetch_tags(tag_name, date):
    es_client = ElasticSearchClient.Instance()

    if not tag_name or not date:
        logger.warning("msg=Insufficent GET parameters, please provide /tags/<tag_name>/<date>")

    logger.info("msg=Fetching articles | Tag={} | Date={}".format(tag_name, date))

    # Format the date time to %Y-%m-%d format
    try:
        formatted_date = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
    except TypeError:
        logger.exception("msg=Invalid date format, please provide date as YYYYmmdd")
        return bottle.HTTPResponse(status=400, body=build_response(400, 'Invalid date format provided!'))

    # Fetch the articles by matching tags, then filtering by date. ElasticSearch backend
    # ensures this is all done in constant time O(c).
    articles = es_client.fetch_articles_using_tag(tag_name, formatted_date)

    if not articles:
        logger.warning("msg=No articles found for tag={} and date={}".format(tag_name, date))
        return bottle.HTTPResponse(status=404, body=build_response(404, 'Not found!'))

    # Aggregate tag counts and build set for related tags
    tag_counts, related_tags = aggregate_article_tags(tag_name, articles)

    # Sort the articles by epoch time field attached to each article.
    # Get the top 10 items
    latest_articles = sort_articles_by_time(articles, top_items=10)

    result = {'tag': tag_name,
              'count': tag_counts,
              'articles': latest_articles,
              'related_tags': list(related_tags)
              }

    return bottle.HTTPResponse(status=200, body=result)


def aggregate_article_tags(tag, articles):
    count = 0
    unique_tags = set()

    for article in articles:
        tags = article['tags']
        count += tags.count(tag)
        unique_tags |= set(tags)

    related_tags = unique_tags - set([tag])
    return count, related_tags


def sort_articles_by_time(articles, top_items=10):
    time_sorted = sorted(articles, key=lambda top_article: top_article['epoch'], reverse=True)
    return [top_item['id'] for top_item in time_sorted[:top_items]]
