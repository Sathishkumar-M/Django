from elasticsearch import Elasticsearch, RequestsHttpConnection
from rest_framework_elasticsearch import es_views, es_pagination, es_filters
from .search import BlogPostIndex
from .serializers import ElasticBlogSerializer

class BlogView(es_views.ListElasticAPIView):
    es_client = Elasticsearch(hosts=['http://localhost:9200/'],
                              connection_class=RequestsHttpConnection)

    es_model = BlogPostIndex
    serializer_class = ElasticBlogSerializer
    es_pagination_class = es_pagination.ElasticLimitOffsetPagination

    es_filter_backends = (
        es_filters.ElasticFieldsFilter,
        es_filters.ElasticSearchFilter,
        es_filters.ElasticOrderingFilter,
    )
    es_ordering_fields = (
        "posted_date",
        ("title.raw", "title")
    )
    es_filter_fields = (
        es_filters.ESFieldFilter('search','author'),
        es_filters.ESFieldFilter('tag','title'),
    )
    es_search_fields = (
        'author'
    )
