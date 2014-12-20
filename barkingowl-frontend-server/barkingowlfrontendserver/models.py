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
            pass_salt
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
                disabled = disabled,
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
                TargetURLs,
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
                DocumentTypes,
            ).all()
        return document_types

class ScrapingJobAssignments(Base):

    __tablename__ = 'scrapingjobassignments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    scraping_job_is = Column(Integer, ForeignKey('scrapingjobs.id'))
    
    @classmethod
    def make_assignment(cls, session, user_id, scraping_job_id):
        with transaction.manager:
            assignment = ScrapingJobAssignments(
                user_id = user_id,
                scraping_job_id = scraping_job_id,
            )
        return assignment

    @classmethod
    def get_assignment(cls, session, user_id, scraping_job_id):
        with transaction.manager:
            assignment = session.query(
                ScrapingJobAssignments,
            ).filter(
                ScrapingJobAssignments.user_id == user_id,
                ScrapingJobAssignments.scraping_job_id,
            ).first()
        return assignment

class Scrapers(Base):

    __tablename__ = 'scrapers'
    id = Column(Integer, primary_key=True)
    unique = Column(Text)
    status = Column(Text)
    current_scraper_run_id = Column(Integer, ForeignKey('scraperruns.id'), \
        nullable=True)
    checkin_datetime = Column(DateTime)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_scraper(cls, session, unique, status):

        """ add a scraper """

        with transaction.manager:
            scraper = Scrapers(
                unique,
                status,
                current_scraper_run_id = None,
                checkin_datetime = datetime.datetime.now(),
                creation_datetime = datetime.datetime.no(),
            )
            session.add(scraper)
            transaction.commit()
        return scraper

    @classmethod
    def set_scraper_run_id(cls, session, scraper_run_id):
    
        """ sets the scraper run the scraper is working on """

        with transaction.manager:
            scraper = session.query(
                # TODO: finish this
            )
        return scraper

class ScraperRuns(Base):

    __tablename__ = 'scraperruns'
    id = Column(Integer, primary_key=True)
    scraping_job_id = Column(Integer, ForeignKey('scrapingjobs.id'))
    #scraper_unique = Column(Text)
    scraper_id = Column(Integer, ForeignKey('scrapers.id'))
    successful = Column(Boolean)
    bad_link_count = Column(Integer)
    processed_link_count = Column(Integer)
    bandwidth = Column(Integer)
    ignored_count = Column(Integer)
    
    # these may not want to be popualted, as they could be MASSIVE
    #processed_links_json = Column(Text)
    #bad_links_json = Column(Text)
    
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    
    @classmethod
    def add_run(cls, session, scraper_unique, scraping_job_id, successful, \
            bad_link_count, processed_link_count, bandwidth, ignored_count, \
            processed_links_json, bad_links_json, start_datetime, \
            end_datetime):
        
        """ Add a run to the log """

        with transaction.manager:
            run = ScraperRuns(
                scraping_job_id = scraping_job_id,
                scraper_unique = scraper_unique,
                successful = successful,
                bad_link_count = bad_link_count,
                processed_link_count,
                bandwidth = bandwidth,
                ignored_count = ignored_count,
                #processed_links_json = processed_links_json,
                #bad_links_json = bad_links_json,
                start_datetime = start_datetime,
                end_datetime = end_datetime,
            )
            session.add(run)
            transaction.commit()
        return run
        
    @classmethod
    def get_runs_for_scraping_job(cls, session, scraping_job_id, start, count):
    
        """ get the runs for a scraping job """

        with transaction.manager:
            runs = session.query(
                ScraperRuns,
            ).filter(
                ScraperRuns.scraping_job_id == scraping_job_id,
            ).all()
        return runs

class ScrapingJobs(Base):

    __tablename__ = 'scrapingjobs'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    target_url_id = Column(Integer, ForeignKey('targeturls.id'))
    name = Column(Text)
    notes = Column(Text)
    frequency = Column(Integer) # in hours
    link_level = Column(Integer) # 0 = exhostive
    document_type_id = Column(Integer, ForeignKey('documenttypes.id')
    enabled = Column(Boolean)
    creation_datetime = Column(DateTime)

    @classmethod
    def create_scraping_job(cls, session, author_id, target_url_id, name, \
            notes, frequency, link_level, document_type_id):

        with transaction.manager:
            scraping_job = ScrapingJobs(
                author_id = author_id,
                target_url_id = target_url_id,
                name = name,
                notes = notes,
                frequency = frequency,
                link_level = link_level,
                document_type_id = document_type_id,
                enabled = False,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(scraping_job)
            transaction.commit()
        return scraping_job

    @classmethod
    def get_users_scraping_jobs(cls, session, user_id):
        with transaction.manager:
            jobs = session.query(
                ScrapingJobs,
            ).filter(
                author_id == user_id,
            ).all()
        return

    @classmethod
    def get_one_unrun_job(cls, session):
        with transaction.manager:
            job = session.query(
                ScrapingJobs,
            ).filter(
                ScrapingJobs.
            ).first()
        return job

class Documents(Base):

    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    target_url_id = Column(Integer, ForeignKey('targeturls.id'))
    scraper_run_id = Column(Integer, ForeignKey('scraperruns.id'))
    scraping_job_id = Column(Integer, ForeignKey('scrapingjobs.id'))
    
    label = Column(Text)
    description = Column(Text)

    # these are the things we get back from BarkingOwl
    url = Column(Text)
    unique = Column(Text)
    filename = Column(Text)
    link_text = Column(Text)
    page_url = Column(Text)
    page_title = Column(Text)
    size = Column(Text)
    
    download_datetime = Column(Text)
    creation_datetime = Column(Text)    

    @classmethod
    def add_document(cls, session, target_url_id, scraper_run_id, \
            scraping_job_id, label, description, url, unique, filename, \
            link_text, page_url, page_title, size, download_datetime):

        """ Adds a document """

        with transaction.manager:
            document = Documents(
                target_url_id = target_url_id,
                scraper_run_id = scraper_run_id,
                scraping_job_id = scraping_job_id,
                label = label,
                description = descritpion,
                url = url,
                unique = unique,
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
            the scraping job """

        with transaction.manager:
            documents = session.query(
                Documents,
            ).join(
                ScrapingJobAssignments,
                    ScrapingJobAssignments.scraping_job_id == \
                        Documents.scraping_job_id,
            ).filter(
                ScrapingJobAssignments.user_id == owner_id,
            ).all()
        return documents

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

