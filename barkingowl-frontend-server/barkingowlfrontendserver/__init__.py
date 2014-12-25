from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('/', '/')

    config.add_route('/create_user.json', 'create_user.json')

    config.add_route('/add_target_url.json','/add_target_url.json')
    config.add_route('/get_target_urls.json','/get_target_urls.json')

    config.add_route('/add_document_type.json', '/add_document_type.json')

    config.add_route('/create_scraper_job.json', '/create_scraper_job.json')
    config.add_route('/get_scraper_jobs.json', '/get_scraper_jobs.json')

    config.add_route('/register_scraper.json','/register_scraper.json')
    config.add_route('/get_scraper_job.json','/get_scraper_job.json')

    config.add_route('/add_document.json', '/add_document.json')
    config.add_route('/get_documents.json', '/get_documents.json')

    config.scan()
    return config.make_wsgi_app()
