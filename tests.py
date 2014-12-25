
import uuid
import json
import requests
import datetime

ROOT_DOMAIN = "http://127.0.0.1:6548/"

def log(output):

    print "[{0}]: {1}".format(str(datetime.datetime.now()).split('.')[0],output) 

def url_action(url_payload, data, method):

    """ 
        url_action(url, data, method)
        
            url = url to send
            data = dict of things to send
            method = 'GET' or 'POST'

    """

    json_response = None
    if True:
    #try:

        if method == 'GET':

            #url_payload = url_payload + "?"

            for key, value in data.items():
                url_payload += "{0}={1}&".format(key,value)

            log("URL: {0}".format(url_payload))

            http_response = requests.get(url_payload).text

            log("HTTP Response: {0}".format(http_response))

            json_response = json.loads(http_response)

        elif method == 'POST':

            log("URL: {0}".format(url_payload))

            http_response = requests.post(url_payload, data=data).text

            log("HTTP Response: {0}".format(http_response))

            json_response = json.loads(http_response)


    #except:
    #    pass

    return json_response

def _execute_test(url, token, data, method):

    log("----")
    log("TEST: {0}".format(url))
    #log("")

    success = False
    response = {}

    if True:
    #try:
        if token == None:
            url_payload = "{0}{1}?".format(ROOT_DOMAIN,url)
        else:
            if not 'admin' in url:

                log('Calling Client URL')

                # this is a client url, and needs a client)id
                # rather than a token
                url_payload = "{0}{1}?client_id={2}&".format(ROOT_DOMAIN,url,token)
            else:

                log('Calling Admin URL')

                url_payload = "{0}{1}?token={2}&".format(ROOT_DOMAIN,url,token)

        response = url_action(url_payload, data, method)

        if response['success'] == False:
            raise Exception('ERROR: Success = False')

        success = True

    #except:
    #    pass

    return success, response


def run_tests():

    log("Launching tests ...")
    log("")

    success, payload = _execute_test(
        'create_user.json',
        None,
        {
            'first': 'Temp',
            'last': 'User',
            'email': 'temp@user.com',
            'password': 'password123',
        },
        'POST',
    )
    user_id = payload['user_id']

    if user_id == None:
        raise Exception('User was not created')

    log('User ID: {0}'.format(user_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'add_target_url.json',
        None,
        {
            'owner_id': user_id,
            'title': 'TimDuffy.Me Website',
            'description': "Tim Duffy's personal website",
            'url': 'http://timduffy.me',
        },
        'POST',
    )
    target_url_id = payload['target_url_id']
    log('Target URL ID: {0}'.format(target_url_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'get_target_urls.json',
        None,
        {
            'owner_id': user_id,
        },
        'GET',
    )
    target_urls = payload['target_urls']
    if len(target_urls) < 1:
        raise Exception('Created URL was not returned in query')
    log('Target URL count: {0}'.format(len(target_urls)))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'add_document_type.json',
        None,
        {
            'name': 'PDF Document',
            'description': 'Adobe PDF Document',
            'doc_type': 'application/pdf',
        },
        'POST',
    )
    doc_type_id = payload['doc_type_id']
    log('Document Type ID: {0}'.format(doc_type_id))
    log('----')
    log('')
    log('')
    
    success, payload = _execute_test(
        'create_scraper_job.json',
        None,
        {
            'owner_id': user_id,
            'target_url_id': target_url_id,
            'name': 'TimDuffy.Me Scraper Job 0',
            'notes': 'Keep up to date with docs on TimDuffy.Me',
            'link_level': -1, # exhostive - this is super dangerous
            'document_type_id': doc_type_id,
            'enabled': True,
        },
        'POST',
    )
    scraper_job_id = payload['scraper_job_id']
    log('Scraper Job ID: {0}'.format(scraper_job_id))
    log('----')
    log('')
    log('')
 
    success, payload = _execute_test(
        'get_scraper_jobs.json',
        None,
        {
            'owner_id': user_id,
        },
        'GET',
    )
    scraper_jobs = payload['scraper_jobs']
    if len(scraper_jobs) < 1:
        raise Exception('Created Scraper Job was not returned with query')
    log('Scraper Job count: {0}'.format(len(scraper_jobs)))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'get_documents.json',
        None,
        {
            'scraper_job_id': scraper_job_id,
        },
        'GET',
    )
    documents = payload['documents']
    if len(documents) < 1:
        raise Exception('Scrapers did not find any documents.')
    log('Document count: {0}'.format(len(documents)))
    log('----')
    log('')
    log('')


if __name__ == '__main__':

    print "\n\n"

    run_tests()
