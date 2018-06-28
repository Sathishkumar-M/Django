from rest_framework_elasticsearch.es_serializer import ElasticModelSerializer
from .models import BlogPost
from .search import BlogPostIndex

class ElasticBlogSerializer(ElasticModelSerializer):
    class Meta:
        model = BlogPost
        es_model = BlogPostIndex
        fields = ('title', 'text')
