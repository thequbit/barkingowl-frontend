from barking_owl import Scraper

import uuid
import time
import json
import requests


class FrontEndScraper(object):

    def __init__(self):
 
        self.jobsurl = "http://localhost:6548/get_scraper_job.json"
        
        self.uid = str(uuid.uuid4())

        self.scraper = Scraper(uid=self.uid)

    def check_for_job(self):

        """
        {
            "job": {
                "target_url": {
                    "url": "http://www.timduffy.me/",
                    "disabled": false,
                    "description": "Tim Duffy's Website",
                    "title": "TimDuffy.Me"
                },
                "creation_datetime": "2014-12-20 15:37:17.968523",
                "target_url_id": 1,
                "document_type_id": 1,
                "last_run_datetime": "2013-12-20 15:37:17.968523",
                "document_type": {
                    "doc_type": "application/pdf",
                    "name": "PDF Document",
                    "description": "PDF Document"
                },
                "id": 1,
                "name": "Daily TimDuffy.me Scraper Job",
                "notes": "Should run pretty quickly",
                "enabled": false,
                "author_id": 1,
                "link_level": -1
            },
            "success": true
        }
        """

        print "Checking for job ..."

        url = '{0}?unique={1}'.format(self.jobsurl,self.uid)

        http_response = requests.get(url).text
        response = json.loads(http_response)

        if response['success'] == False:
            raise Exception('invalid response from server.')

        print "Job response recieved."

        return response['job']

    def execute_job(self, job):

        print "Executing Job ..."

        # create our url payload 
        url_data = {
            'target_url': job['target_url']['url'],
            'max_link_level': -1, #job['link_level'],
            'doc_type': job['document_type']['doc_type'],
        }

        print "\n\n"
        print url_data
        print "\n\n"

        # reset the scraper to it is ready to accept our job
        self.scraper.reset()

        # set the payload
        self.scraper.set_url_data( url_data )

        # begin scraping
        docs = self.scraper.find_docs()

        #docs = self.scraper.status['documents']

        print docs

        #print self.scraper.status

        print "Done with job."

    def start(self):


        while(1):

            job = None
            if True:
            #try:
                job = self.check_for_job()
            #except:
            #    pass

            if job != None:
                self.execute_job(job)

            print "Waiting 5 seconds ..."
            time.sleep(5)


if __name__ == '__main__':

    print "Starting BarkingOwl FrontEnd Scraper"

    scraper = FrontEndScraper()

    scraper.start()
