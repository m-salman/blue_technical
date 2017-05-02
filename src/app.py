import bottle
import logging
from src.endpoints import tags
from src.endpoints import article
from src.endpoints import swagger


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("msg=Starting Article API")

def _create_app():
    app = bottle.default_app()
    app.merge(article.app)
    app.merge(tags.app)
    app.merge(swagger.app)
    return app


application = _create_app()

logger.info("msg=Started Article API")

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080, reload=True)