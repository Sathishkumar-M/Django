from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection()

class BlogPostIndex(DocType):
    author = Text()
    posted_date = Date()
    title = Text()
    text = Text()

    class Meta:
        index = 'blogpost-index'

def bulk_indexing():
    BlogPostIndex.init()
    es = Elasticsearch()
    # es = Elasticsearch(timeout=100000, max_retries=10, retry_on_timeout=True)
    # es.cluster.health(wait_for_status='yellow', request_timeout=1)
    bulk(client=es, actions=(b.indexing() for b in models.BlogPost.objects.all().iterator()))

def search(author):
    s = Search().filter('term', author=author)
    response = s.execute()
    return response
