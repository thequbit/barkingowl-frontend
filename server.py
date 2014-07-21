import os
import json
import uuid
import urllib
import datetime
import threading

from barking_owl import BusAccess

from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__, static_folder='web/static', static_url_path='')
app.template_folder = "web"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

bus_access = BusAccess( my_id = str(uuid.uuid4()) )

dispatched_urls = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_csv', methods=['POST'])
def upload_csv():

    csv_contents = ''
#    try:
    if True:

        print request.files

        file = request.files['file']
    
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_filename)
            with open(full_filename) as f:
                csv_contents = f.read()
        
#    except:
#        pass

    return csv_contents

@app.route('/shutdown_system.json')
def system_shutdown():

    resp = {'success': False}

    try:

        bus_access.send_message(
            command = 'global_shutdown',
            destination_id = 'broadcast',
            message = {},
        )

        resp['success'] = True

    except:
        pass

    return json.dumps(resp)

@app.route('/get_urls.json')
def get_urls():

    resp = {'success': False}

#    try:
    if True:

        urls = dispatched_urls

        resp['urls'] = urls
        resp['success'] = True

#    except:
#        pass

    return json.dumps(resp)

@app.route('/set_urls.json')
def app_url():

    resp = {'success': False}

    try:
#    if True:

        urls = json.loads( urllib.unquote( request.args['urls']) )

        for i in range(0,len(urls)):
            urls[i]['creation_datetime'] = str(datetime.datetime.now())

        bus_access.send_message(
            command = 'set_dispatcher_urls',
            destination_id = 'broadcast',
            message = {
                'urls': urls,
            }
        )        

        global dispatched_urls
        dispatched_urls = urls;

        resp['urls'] = dispatched_urls
        resp['success'] = True

    except:
        resp['error_text'] = "missing 'urls' request argument, or bad json format in value"
        pass

    return json.dumps(resp)

#@app.route('/start_dispatcher.json')
#def start_dispatcher():
#    
#    resp = {'success': False}
#
#    try:
#
#        dispatcher_thread = threading.Thread(target=dispatcher.start())
#        dispatcher_thread.start()
#
#        resp['success'] = True
#
#    except:
#        pass
#
#    return json.dumps(resp)

if __name__ == "__main__":
    print "Web Application Starting ..."
    
    host = '0.0.0.0'
    port = 8067

    fa = app.run(host=host, port=port)
