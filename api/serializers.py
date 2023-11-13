from rest_framework import serializers
from blog.models import Post,Category

class PostSerializer(serializers.ModelSerializer):
	category=serializers.HyperlinkedRelatedField(
	    many=True,
	    read_only=True,
	    view_name='api_category_post_list'
	)
	class Meta:
		model = Post
		exclude = ['created','updated']

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model=Category
		fields='__all__'