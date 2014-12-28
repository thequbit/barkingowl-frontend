from sqlalchemy import update, desc, func

from sqlalchemy import (
    Column,
    Index,
    ForeignKey,
)
from sqlalchemy import (    
    Integer,
    Text,
    DateTime,
    Boolean,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

import transaction

import datetime
import uuid
import hashlib

DBSession = scoped_session(
    sessionmaker(
        extension=ZopeTransactionExtension(),
        expire_on_commit=False
    )
)
Base = declarative_base()

#class MyModel(Base):
#    __tablename__ = 'models'
#    id = Column(Integer, primary_key=True)
#    name = Column(Text)
#    value = Column(Integer)
#
#Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first = Column(Text)
    last = Column(Text)
    email = Column(Text)
    passhash = Column(Text)
    passsalt = Column(Text)
    
    @classmethod
    def add_user(cls, session, first, last, email, password):
        
        """ Add a new user """

        passsalt = str(uuid.uuid4())
        passhash = hashlib.sha256('{0}{1}'.format(
            password,
            passsalt
        )).hexdigest()

        with transaction.manager:
            user = Users(
                first = first,
                last = last,
                email = email,
                passhash = passhash,
                passsalt = passsalt,
            )
            session.add(user)
            transaction.commit()
        return user

    @classmethod
    def authenticate_user(cls, session, email, password):
        
        """ Authenticate user, and deturmine if credentials are correct """
        
        with transaction.manager:
            user = None
            _user = session.query(
                Users,
            ).filter(
                Users.email == email,
            ).first()
            if _user != None:
                pass_hash = hashlib.sha256('{0}{1}'.format(
                    password,
                    _user.pass_salt,
                )).hexdigest()
            if _user.pass_hash == pass_hash:
                user = _user
        return user

    @classmethod
    def get_by_email(cls, session, email):
        
        """ Get a user by their email address """

        with transaction.manager:
            user = session.query(
                Users,
            ).filter(
                Users.email == email,
            ).first()
        return user 


class TargetURLs(Base):

    __tablename__ = 'targeturls'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    title = Column(Text)
    description = Column(Text)
    url = Column(Text)
    disabled = Column(Boolean)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_target_url(cls, session, owner_id, title, description, url):

        """ Adds a new target url """

        with transaction.manager:
            target_url = TargetURLs(
                owner_id = owner_id,
                title = title,
                description = description,
                url = url,
                disabled = False,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(target_url)
            transaction.commit()
        return target_url

    @classmethod
    def get_all_target_urls(cls, session):
    
        """ Returns all target urls in the database """

        with transaction.manager:
            target_urls = session.query(
                TargetURLs,
            ).all()
        return target_urls

    @classmethod
    def get_all_by_owner_id(cls, session, owner_id):
    
        """ Returns all target urls by owner id """

        with transaction.manager:
            target_urls = session.query(
                TargetURLs.id,
                TargetURLs.owner_id,
                TargetURLs.title,
                TargetURLs.description,
                TargetURLs.url,
                TargetURLs.disabled,
                TargetURLs.creation_datetime,
            ).filter(
                TargetURLs.owner_id == owner_id,
            ).all()
        return target_urls


class DocumentTypes(Base):

    __tablename__ = 'documenttypes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    doc_type = Column(Text)

    @classmethod
    def add_new(cls, session, name, description, doc_type):
        with transaction.manager:
            document_type = DocumentTypes(
                name = name,
                description = description,
                doc_type = doc_type,
            )
            session.add(document_type)
            transaction.commit()
        return document_type

    @classmethod
    def get_by_id(cls, session, id):
        
        with transaction.manager:
            document_type = session.query(
                DocumentTypes,
            ).filter(
                DocumentTypes.id == id,
            ).first()
        return document_type

    @classmethod
    def get_all_types(cls, session):
        with transaction.manager:
            document_types = session.query(
                DocumentTypes.id,
                DocumentTypes.name,
                DocumentTypes.description,
                DocumentTypes.doc_type,
            ).all()
        return document_types

class ScraperJobAssignments(Base):

    __tablename__ = 'scraperjobassignments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    scraper_job_is = Column(Integer, ForeignKey('scraperjobs.id'))
    
    @classmethod
    def make_assignment(cls, session, user_id, scraper_job_id):
        with transaction.manager:
            assignment = ScraperJobAssignments(
                user_id = user_id,
                scraper_job_id = scraper_job_id,
            )
        return assignment

    @classmethod
    def get_assignment(cls, session, user_id, scraper_job_id):
        with transaction.manager:
            assignment = session.query(
                ScraperJobAssignments,
            ).filter(
                ScraperJobAssignments.user_id == user_id,
                ScraperJobAssignments.scraper_job_id,
            ).first()
        return assignment

class ScraperStatuses(Base):

    __tablename__ = 'scraperstatuses'
    id = Column(Integer, primary_key=True)
    scraper_id = Column(Integer, ForeignKey('scrapers.id'))
    status = Column(Text)
    current_scraper_run_id = Column(Integer, ForeignKey('scraperruns.id'), \
        nullable=True)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_scraper_status(cls, session, scraper_id, status, \
            current_scraper_run_id=None):
    
        """ adds a scraper status to the database """

        with transaction.manager:
            status = ScraperStatuses(
                scraper_id = scraper_id,
                status = status,
                current_scraper_run_id = current_scraper_run_id,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(status)
            transaction.commit()
        return status

    @classmethod
    def get_scraper_statuses(cls, session, scraper_id, start, count):
    
        """ gets the statuses for a scraper """

        with transaction.manager:
            statuses = session.query(
                ScraperStatuses,
            ).filter(
                ScraperStatuses.scraper_id == scraper_id,
            ).all()
        return statuses

class Scrapers(Base):

    __tablename__ = 'scrapers'
    id = Column(Integer, primary_key=True)
    unique = Column(Text)
    label = Column(Text)
    url_count = Column(Integer)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_scraper(cls, session, unique, label):

        """ add a scraper """

        with transaction.manager:
            scraper = Scrapers(
                unique = unique,
                label = label,
                url_count = 0,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(scraper)
            transaction.commit()
        return scraper

    @classmethod
    def increment_url_count(cls, session, scraper_id):
    
        """ Increases the number of urls scraped by one"""

        with transaction.manager:
            scraper = session.query(
                Scrapers,
            ).filter(
                Scrapers.scraper_id == scraper_id,
            ).first()
            scraper.url_count += 1
            session.add(scraper)
            transaction.commit()
        return scraper

    @classmethod
    def get_from_unique(cls, session, unique):
    
        """ gets a scraper by its unique id """

        with transaction.manager:
            scraper = session.query(
                Scrapers,
            ).filter(
                Scrapers.unique == unique,
            ).first()
        return scraper

class ScraperRuns(Base):

    __tablename__ = 'scraperruns'
    id = Column(Integer, primary_key=True)
    scraper_job_id = Column(Integer, ForeignKey('scraperjobs.id'))
    scraper_id = Column(Integer, ForeignKey('scrapers.id'))
    finished = Column(Boolean)
    successful = Column(Boolean)
    bad_link_count = Column(Integer)
    processed_link_count = Column(Integer)
    bandwidth = Column(Integer)
    ignored_count = Column(Integer)
    document_count = Column(Integer)    

    # these may not want to be popualted, as they could be MASSIVE
    #processed_links_json = Column(Text)
    #bad_links_json = Column(Text)
    #documents_json = Column(Text)    

    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime, nullable=True)
   
    @classmethod
    def create_run(cls, session, scraper_id, scraper_job_id):

        """ Create a scraper run """

        with transaction.manager:
            run = ScraperRuns(
                scraper_id = scraper_id,
                scraper_job_id = scraper_job_id,
                finished = False,
                successful = False,
                bad_link_count = -1,
                processed_link_count = -1,
                bandwidth = -1,
                ignored_count = -1,
                document_count = -1,
                start_datetime = datetime.datetime.now(),
                end_datetime = None,
            )
            session.add(run)
            transaction.commit()
        return run
 
    @classmethod
    def update_run(cls, session, scraper_run_id, finished, successful, \
            bad_link_count, processed_link_count, bandwidth, ignored_count, \
            document_count, end_datetime):

        """ Updates the contents of a scraper run """

        with transaction.manager:
            scraper_run = session.query(
                ScraperRuns,
            ).filter(
                ScraperRuns.id == scraper_run_id,
            ).first()
            scraper_run.finished = finished
            scraper_run.successful = successful
            scraper_run.bad_link_count = bad_link_count
            scraper_run.processed_link_count = processed_link_count
            scraper_run.bandwidth = bandwidth
            scraper_run.ignored_count = ignored_count
            scraper_run.document_count = document_count
            scraper_run.end_datetime = end_datetime
            session.add(scraper_run)
            transaction.commit()

        return scraper_run

    @classmethod
    def get_runs_for_scraper_job(cls, session, scraper_job_id, start, count):
    
        """ get the runs for a scraper job """

        with transaction.manager:
            runs = session.query(
                ScraperRuns,
            ).filter(
                ScraperRuns.scraper_job_id == scraper_job_id,
            ).all()
        return runs

class ScraperJobs(Base):

    __tablename__ = 'scraperjobs'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    target_url_id = Column(Integer, ForeignKey('targeturls.id'))
    name = Column(Text)
    notes = Column(Text)
    frequency = Column(Integer) # in hours
    link_level = Column(Integer) # 0 = exhostive
    document_type_id = Column(Integer, ForeignKey('documenttypes.id'))
    enabled = Column(Boolean)
    last_run_datetime = Column(DateTime)
    creation_datetime = Column(DateTime)

    @classmethod
    def create_scraper_job(cls, session, owner_id, target_url_id, name, \
            notes, frequency, link_level, document_type_id, enabled=False):

        """ creates a new scraper job in the database """

        with transaction.manager:
            scraper_job = ScraperJobs(
                owner_id = owner_id,
                target_url_id = target_url_id,
                name = name,
                notes = notes,
                frequency = frequency,
                link_level = link_level,
                document_type_id = document_type_id,
                enabled = enabled,
                # set this to a long time ago
                last_run_datetime = datetime.datetime.now() - \
                    datetime.timedelta(days=365),
                creation_datetime = datetime.datetime.now(),
            )
            session.add(scraper_job)
            transaction.commit()
        return scraper_job

    @classmethod
    def get_scraper_jobs(cls, session, owner_id):
        with transaction.manager:
            jobs = session.query(
                ScraperJobs.id,
                ScraperJobs.owner_id,
                ScraperJobs.target_url_id,
                ScraperJobs.name,
                ScraperJobs.notes,
                ScraperJobs.frequency,
                ScraperJobs.link_level,
                ScraperJobs.document_type_id,
                ScraperJobs.enabled,
                ScraperJobs.last_run_datetime,
                ScraperJobs.creation_datetime,
                TargetURLs.title,
                TargetURLs.description,
                TargetURLs.url,
                TargetURLs.disabled,
                DocumentTypes.name,
                DocumentTypes.description,
                DocumentTypes.doc_type,
            ).join(
                TargetURLs, TargetURLs.id == ScraperJobs.target_url_id,
            ).outerjoin(
                DocumentTypes, DocumentTypes.id == \
                    ScraperJobs.document_type_id,
            ).filter(
                owner_id == owner_id,
            ).all()
        return jobs

    @classmethod
    def get_next_job(cls, session):

        """ gets a job that needs to be run """

        with transaction.manager:
            job = session.query(
                ScraperJobs.id,
                ScraperJobs.owner_id,
                ScraperJobs.target_url_id,
                ScraperJobs.name,
                ScraperJobs.notes,
                ScraperJobs.frequency,
                ScraperJobs.link_level,
                ScraperJobs.document_type_id,
                ScraperJobs.enabled,
                ScraperJobs.last_run_datetime,
                ScraperJobs.creation_datetime,
                TargetURLs.title,
                TargetURLs.description,
                TargetURLs.url,
                TargetURLs.disabled,
                DocumentTypes.name,
                DocumentTypes.description,
                DocumentTypes.doc_type,
            ).filter(
                ScraperJobs.last_run_datetime <= 
                    datetime.datetime.now() - datetime.timedelta(days=1),
            ).join(
                TargetURLs, TargetURLs.id == ScraperJobs.target_url_id,
            ).first()
        if job != None:
            with transaction.manager:
                _job = session.query(
                    ScraperJobs,
                ).filter(
                    ScraperJobs.id == job.id,
                ).first()
                _job.last_run_datetime = datetime.datetime.now()
                #session.add(_job)
                #transaction.commit()
        return job

class Documents(Base):

    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    target_url_id = Column(Integer, ForeignKey('targeturls.id'))
    scraper_run_id = Column(Integer, ForeignKey('scraperruns.id'))
    scraper_job_id = Column(Integer, ForeignKey('scraperjobs.id'))
    
    label = Column(Text)
    description = Column(Text)

    # these are the things we get back from BarkingOwl
    url = Column(Text)
    unique_name = Column(Text, nullable=True)
    filename = Column(Text)
    link_text = Column(Text)
    page_url = Column(Text)
    page_title = Column(Text)
    size = Column(Text)
    
    download_datetime = Column(Text, nullable=True)
    creation_datetime = Column(Text)

    @classmethod
    def add_document(cls, session, target_url_id, scraper_run_id, \
            scraper_job_id, label, description, url, unique_name, filename, \
            link_text, page_url, page_title, size, download_datetime):

        """ Adds a document """

        with transaction.manager:
            document = Documents(
                target_url_id = target_url_id,
                scraper_run_id = scraper_run_id,
                scraper_job_id = scraper_job_id,
                label = label,
                description = description,
                url = url,
                unique_name = unique_name,
                filename = filename,
                link_text = link_text,
                page_url = page_url,
                page_title = page_title,
                size = size,
                download_datetime = download_datetime,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(document)
            transaction.commit()
        return document

    @classmethod
    def get_documents_by_owner_id(cls, session, owner_id):

        """ Get all documents for the user that is assigned to
            the scraper job """

        with transaction.manager:
            documents = session.query(
                Documents,
            ).join(
                ScraperJobAssignments,
                    ScraperJobAssignments.scraper_job_id == \
                        Documents.scraper_job_id,
            ).filter(
                ScraperJobAssignments.user_id == owner_id,
            ).all()
        return documents

    @classmethod
    def get_by_scraper_job_id(cls, session, scraper_job_id):
    
        """ Gets all documents from a scraper job """    

        with transaction.manager:
            documents = session.query(
                Documents.id,
                Documents.scraper_run_id,
                Documents.scraper_job_id,
                Documents.label,
                Documents.description,
                Documents.url,
                Documents.unique_name,
                Documents.filename,
                Documents.link_text,
                Documents.page_url,
                Documents.page_title,
                Documents.size,
                Documents.download_datetime,
                Documents.creation_datetime,
            ).filter(
                Documents.scraper_job_id == scraper_job_id,
            ).all()
        return documents
class DocumentContents(Base):

    __tablename__ = 'documentcontents'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    text = Column(Text)
    creation_datetime = Column(DateTime)

    @classmethod
    def create_document_contents(cls, session, document_id, text):

        """  Creates an entry with the document text in it """

        with transaction.manager:
            document_text = DocumentContents(
                document_id = document_id,
                text = text,
                creation_datetime = datetime.datetime.now(),
            )
        return document_text

class DocumentNotes(Base):

    __tablename__ = 'documentnotes'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    contents = Column(Text)
    edited = Column(Boolean)
    edited_datetime = Column(DateTime, nullable=True)
    creation_datetime = Column(DateTime)

    @classmethod
    def create_document_note(cls, session, document_id, author_id, contents):

        """ create a document note """

        with transaction.manager:
            document_note = DocumentNotes(
                document_id = document_id,
                author_id = author_id,
                contents = contents,
            )
            session.add(document_note)
            transaction.commit()
        return document_note

    @classmethod
    def get_document_notes_by_document_id(cls, session, document_id):
    
        """ get all notes for a document """

        with transaction.manager:
            document_notes = session.query(
                DocumentNotes,
            ).filter(
                DocumentNotes.id == document_id,
            ).all()
        return document_notes

