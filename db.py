from sqlite3 import IntegrityError
import web

class Database:

    def __init__(self):
        self.connection = web.database(dbn='sqlite', db='urls.db')
        self.connection.text_factory = str

    def create_all_tables(self):
        self.connection.query('CREATE TABLE urls (\n url text not null,\n short_uri text primary key,\n easy_uri text unique,\n visits integer default 0)')

    def get_urls_by_short_or_easy_uri(self, uri):
        by_short_uri = self.get_urls_by_short_uri(uri)
        by_easy_uri = self.get_urls_by_easy_uri(uri)
        if len(by_easy_uri) > 0:  # matching easy URL is more important
            return by_easy_uri
        return by_short_uri

    def get_urls_by_easy_uri(self, easy_uri):
        urls = []
        for url in self.connection.select('urls', vars={'easy_uri': easy_uri}, what='*', where='easy_uri=$easy_uri'):
            urls.append(url)
        return urls

    def get_urls_by_short_uri(self, short_uri):
        urls = []
        for url in self.connection.select('urls', vars={'short_uri': short_uri + '%'}, what='*', where='short_uri LIKE $short_uri'):
            urls.append(url)
        return urls

    def put_url(self, url, short_uri, easy_uri = None):
        try:
            self.connection.insert('urls', url=url, short_uri=short_uri, easy_uri=easy_uri)
        except IntegrityError as e:
            return str(e)

    def increment_visits(self, short_uri):
        visits = 0
        for url in self.connection.select('urls', vars={'short_uri': short_uri}, what='visits', where='short_uri=$short_uri'):
            visits = url.visits
        self.connection.update('urls', vars={'short_uri':short_uri}, where="short_uri=$short_uri", visits=visits + 1)
