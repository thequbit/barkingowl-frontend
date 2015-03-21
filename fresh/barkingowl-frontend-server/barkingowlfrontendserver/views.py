import json
import datetime
import pymongo

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

@view_config(route_name='/', renderer='templates/index.mak')
def index(request):

    return {}

@view_config(route_name='/get_documents.json')
def get_documents(request):

    dbclient = MongoClient('mongodb://localhost:27017/')
    db = dbclient['barkingowl']
    documents = db['documents']
    docs = documents.find({'document': {'url': {'url': request.GET['url']}}})
    for i in range(0,len(docs)):
        docs[i]._id = str(docs[i]._id)
    return {'docs': docs}

'''
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'barkingowl-frontend-server'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_barkingowl-frontend-server_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
'''
