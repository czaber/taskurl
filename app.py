import web

from web.contrib.template import render_jinja
from db import Database
 
url_prefix = 'http://localhost:8080/'
urls = (
    '/', 'Shorten',
    '/assets/(.+)', 'Assets',
    '/(.+)', 'Redirect',
)

app = web.application(urls, globals())
wsgi = app.wsgifunc()

render = render_jinja('templates', encoding = 'utf-8',)
render._lookup.globals.update(assets='/assets')
db = Database()

def extract_uri(url):
  from urlparse import urlparse
  result = urlparse(url)
  return result.path

def generate_short_uri(uri):
  from uuid import uuid4
  short_uri = uuid4().hex
  return short_uri

def generate_easy_uri(url, easy_suffix):
  easy_suffix = easy_suffix.replace(' ', '-')
  return easy_suffix

def get_error_description(problem, short_url, easy_url):
    if problem == 'column easy_uri is not unique':
        return 'Link %s already exists! Please, choose another name.' % easy_url
    return None

class Shorten:
    def GET(self):
        return render.index(prefix=url_prefix)

    def generate_short_url(self, url):
	if len(url) is 0:
            return None, None

        short_uri = generate_short_uri(url)
        short_url = url_prefix + short_uri
        return short_url, short_uri

    def generate_easy_url(self, url, suffix):
        if len(suffix) is 0:
            return None, None

        easy_uri = generate_easy_uri(url, suffix)
        easy_url = url_prefix + easy_uri
        return easy_url, easy_uri
        
    def POST(self):
        url = web.input().get('url', '')
        easy_suffix = web.input().get('easy_suffix', '')

        short_url, short_uri = self.generate_short_url(url)
        easy_url, easy_uri = self.generate_easy_url(url, easy_suffix)

        problem = db.put_url(url=url, short_uri=short_uri, easy_uri=easy_uri)
        if problem:
            error = get_error_description(problem, short_url, easy_url)
            return render.index(error=error, url=url, easy_suffix=easy_suffix, prefix=url_prefix)

        if easy_uri is None:
            error = "Please, provide a URL"
            return render.index(error=error, url=url, easy_suffix=easy_suffix, prefix=url_prefix)

        return render.addresses(url=url, prefix=url_prefix, short_uri=short_uri, easy_uri=easy_uri)

class Redirect:
    def GET(self, short_or_easy_url):
        short_or_easy_uri = extract_uri(short_or_easy_url)
        urls = db.get_urls_by_short_or_easy_uri(short_or_easy_uri)
        if len(urls) is 0:
            raise web.notfound(render.not_found(url=short_or_easy_url))
        if len(urls) is 1:
            url = urls[0]
            db.increment_visits(url.short_uri)
            raise web.redirect(url.url, '307 Temporary Redirect')
        return render.found(prefix=url_prefix, url=short_or_easy_url, urls=urls)

class Assets:
    def GET(self, path):
        try:
            f = open('assets/' + path, 'r')
            content = f.read()
            return content
        except IOError, e:
            print e
            raise web.notfound()

if __name__ == "__main__":
    app.run()
