from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from datetime import datetime
from pytz import UTC
from django.core.files.uploadedfile import SimpleUploadedFile
from blog.models import Post,Category


class PostApiTestCase(TestCase):

	def setUp(self):
		#CREATE USER
		self.u1=get_user_model().objects.create(username='author',password='password',is_author=True)
		self.u2=get_user_model().objects.create(username='normal',password='password')

		#CREAE CATEGORY
		self.category=Category.objects.create(
				title='testcat',
				slug='testcatslug',
				status=True				
			)
		#CREATE POST
		self.post=Post.objects.create(
				title='testpost',
				slug='testpostslug',
				author=self.u1,
				description='test description',
				thumbnail=SimpleUploadedFile(name='test_image.jpg', content=b'imagebinary', content_type='image/jpeg'),
				status=True,
				published=timezone.now(),
			)

		self.client=APIClient()
		self.token1=Token.objects.create(user=self.u1)
		self.token2=Token.objects.create(user=self.u2)

		

	def test_post_list(self):
		resp=self.client.get('/api/v1/posts/')
		data=resp.json()
		self.assertEqual(len(data),1)

		for post_dict in data:
			self.assertEqual(self.post.title,post_dict['title'])
			self.assertEqual(self.post.author.id,post_dict['author'])
			self.assertEqual(self.post.description,post_dict['description'])
			self.assertTrue(post_dict['thumbnail'].endswith(self.post.thumbnail.url))
			self.assertEqual(
				self.post.published,
				datetime.strptime(post_dict['published'],'%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=UTC)
				)

	def test_unauthorized_post_create(self):
		self.client.credentials(HTTP_AUTHORIZATION='token '+self.token2.key)
		post_dict={
			"title":"post",
			"slug":"post",
			"author":"2",
			"description":"this is post",
			"status":True,
			"published":"2022-01-10T09:00:00Z",
		}
		resp=self.client.post('/api/v1/posts/',post_dict)
		self.assertEqual(resp.status_code,403)


	def test_post_create(self):
		self.client.credentials(HTTP_AUTHORIZATION='token '+self.token1.key)
		post_dict={
			"title":"post",
			"slug":"post",
			"author":1,
			"description":"this is post",
			"status":'d',
			"published":"2022-01-10T09:00:00Z",
		}
		resp=self.client.post('/api/v1/posts/',post_dict)
		self.assertEqual(resp.status_code,201)