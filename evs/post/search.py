from elasticsearch_dsl import (
    DocType,
    Date,
    Keyword,
    Text,
    Boolean,
    Integer
)


class BlogPostIndex(DocType):
    """
    BlogIndex.init(using=es_client)
    """
    author = Text()
    posted_date = Date()
    title = Text()
    text = Text()

    class Meta:
        index = 'blogpost-index'
