from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Users,
    TargetURLs,
    DocumentTypes,
    ScraperJobAssignments,
    ScraperStatuses,
    Scrapers,
    ScraperRuns,
    ScraperJobs,
    Documents,
    DocumentContents,
    DocumentNotes, 
)

import json

def make_response(resp_dict):

    print "[DEBUG]"
    print resp_dict
    print '\n'

    resp = Response(json.dumps(resp_dict), content_type='application/json', charset='utf8')
    resp.headerlist.append(('Access-Control-Allow-Origin', '*'))

    return resp

def str2bool(text):
    b = False
    if text.strip().lower() == 'true':
        b = True
    return b

@view_config(route_name='/', renderer='templates/index.mak')
def web_index(request):

    return {}

@view_config(route_name='/create_user.json')
def web_create_user(request):

    result = {'success': False}
    try:

        try:
            first = request.POST['first']
            last = request.POST['last']
            email = request.POST['email']
            password = request.POST['password']
        except:
            raise Exception('Invalid/Missing fields.')

        user = Users.add_user(
            session = DBSession,
            first = first,
            last = last,
            email = email,
            password = password,
        )

        result['user_id'] = user.id

        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return make_response(result)


@view_config(route_name='/add_target_url.json')
def web_create_target_url(request):

    result = {'success': False}

    try:

        try:
            owner_id = request.POST['owner_id']
            title = request.POST['title']
            description = request.POST['description']
            url = request.POST['url']
        except:
            raise Exception('Invalid/Missing fields.')

        target_url = TargetURLs.add_target_url(
            session = DBSession,
            owner_id = owner_id,
            title = title, 
            description = description,
            url = url, 
        )

        result['target_url_id'] = target_url.id
        result['target_url'] = target_url.url

        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)
        pass

    return make_response(result)

@view_config(route_name='/get_target_urls.json')
def web_get_target_urls(request):

    result = {'success': False}
    try:

        try:
            owner_id = request.GET['owner_id']
        except:
            raise Exception('Invalid/Missing fields.')

        _target_urls = TargetURLs.get_all_by_owner_id(
            session = DBSession,
            owner_id = owner_id,
        )

        target_urls = []
        for t_id, t_owner_id, t_title, t_description, t_url, t_disabled, \
                t_creation_datetime in _target_urls:
            target_urls.append({
                'id': t_id,
                'owner_id': t_owner_id,
                'title': t_title,
                'description': t_description,
                'url': t_url,
                'disabled': t_disabled,
                'created': str(t_creation_datetime),
            })

        result['target_urls'] = target_urls

        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return make_response(result)

@view_config(route_name='/add_document_type.json')
def web_add_document_type(request):

    result = {'success': False}
    try:

        try:
            name = request.POST['name']
            description = request.POST['description']
            doc_type = request.POST['doc_type']
        except:
            raise Exception('Invalid/Missing fields.')

        doc_type = DocumentTypes.add_new(
            session = DBSession,
            name = name,
            description = description,
            doc_type = doc_type,
        )

        result['doc_type_id'] = doc_type.id

        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return make_response(result)

@view_config(route_name='/create_scraper_job.json')
def web_create_scraper_job(request):

    result = {'success': False}
    try:

        try:
            owner_id = request.POST['owner_id']
            target_url_id = request.POST['target_url_id']
            name = request.POST['name']
            notes = request.POST['notes']
            #frequency = request.POST['frequency']
            link_level = request.POST['link_level']
            document_type_id = request.POST['document_type_id']
            enabled = str2bool(request.POST['enabled'])
        except:
            raise Exception('Invalid/Missing fields.')

        scraper_job = ScraperJobs.create_scraper_job(
            session = DBSession,
            owner_id = owner_id,
            target_url_id = target_url_id,
            name = name,
            notes = notes,
            frequency = 1, #frequency, 
            link_level = link_level,
            document_type_id = document_type_id,
            enabled = enabled,
        )

        result['scraper_job_id'] = scraper_job.id

        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return make_response(result)

@view_config(route_name='/get_scraper_jobs.json')
def web_get_scraper_jobs(request):

    result = {'success': False}
    if True:
    #try:

        if True:
        #try:
            owner_id = request.GET['owner_id']
        #except:
        #    raise Exception('Invalid/Missing fields.')


        _scraper_jobs = ScraperJobs.get_scraper_jobs(
            session = DBSession,
            owner_id = owner_id,
        )

        scraper_jobs = []
        for s_id, s_author_id, s_target_url_id, s_name, s_notes, s_frequency, \
                s_link_level, s_document_type_id, s_enabled, \
                s_last_run_datetime, s_creation_datetime, t_title, \
                t_description, t_url, t_disabled, d_name, d_description, \
                d_doc_type in _scraper_jobs:
            scraper_jobs.append({
                'id': s_id,
                'author_id': s_author_id,
                'target_url_id': s_target_url_id,
                'name': s_name,
                'notes': s_notes,
                #'frequency': s_frequency,
                'link_level': s_link_level,
                'document_type_id': s_document_type_id,
                'enabled': s_enabled,
                'last_run_datetime': str(s_last_run_datetime),
                'creation_datetime': str(s_creation_datetime),
                'target_url': {
                    'title': t_title,
                    'description': t_description,
                    'url': t_url,
                    'disabled': t_disabled,
                },
                'document_type': {
                    'name': d_name,
                    'description': d_description,
                    'doc_type': d_doc_type,
                },
            })

        result['scraper_jobs'] = scraper_jobs

        result['success'] = True

    #except Exception, e:
    #    result['error_text'] = str(e)

    return make_response(result)
 

@view_config(route_name='/register_scraper.json')
def web_add_scraper(request):

    """ This registers a scraper with the database """

    result = {'success': False}
    try:

        unique = None
        try:
            unique = request.POST['unique']
        except:
            raise Exception('Invalid/Missing unique field within POST')

        if unique == None or unique.strip() == '':
            raise Exception('Invalid unique value: must not be blank')

        _scraper = Scrapers.get_by_unique(
            session = DBSession,
            unique = unique,
        )

        if _scraper != None:
            raise Exception('Scraper already registered')

        scraper = Scrapers.add_scraper(
            session = DBSession,
            unique = unique,
            label = '',
        )

        if scraper == None:
            raise Exception("Internal error while registering scraper")

        result['scraper_id'] = scraper.id

        result['success'] = True

    except Exception, e:
       result['error_text'] = str(e)
       pass

    return make_response(result)

@view_config(route_name='/get_scraper_job.json')
def web_get_scraper_job(request):

    """ this returns a single scraper job (URL) for scraping """

    result = {'success': False}
    try:

        unique = None
        try:
            unique = request.GET['unique']
        except:
            raise Exception('Invalid/Missing unique field within POST')

        if unique == None or unique.strip() == '':
            raise Exception('Invalid unique value: must not be blank') 

        _job = ScraperJobs.get_next_job(
            session = DBSession,
        )

        print "\n\n"
        print _job
        print "\n\n"

        s_id, s_author_id, s_target_url_id, s_name, s_notes, s_frequency, \
            s_link_level, s_document_type_id, s_enabled, \
            s_last_run_datetime, s_creation_datetime, t_title, \
            t_description, t_url, t_disabled, d_name, d_description, \
            d_doc_type = _job

        job = {
            'id': s_id,
            'author_id': s_author_id,
            'target_url_id': s_target_url_id,
            'name': s_name,
            'notes': s_notes,
            #'frequency': s_frequency,
            'link_level': s_link_level,
            'document_type_id': s_document_type_id,
            'enabled': s_enabled,
            'last_run_datetime': str(s_last_run_datetime),
            'creation_datetime': str(s_creation_datetime),
            'target_url': {
                'title': t_title,
                'description': t_description,
                'url': t_url,
                'disabled': t_disabled,
            },
            'document_type': {
                'name': d_name,
                'description': d_description,
                'doc_type': d_doc_type,
            },
        }

        result['job'] = job

        result['success'] = True

    except Exception, e:
       result['error_text'] = str(e)
       pass

    return make_response(result)
