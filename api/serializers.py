from rest_framework import serializers
from blog.models import Post,Category

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = "__all__"
		read_only_fields =["updated", "created"]

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model=Category
		fields='__all__'