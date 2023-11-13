from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from blog.models import Post,Category


class PostModelTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user=get_user_model().objects.create_user(
				username='testuser',
				email='test@email.com',
				password='secret'
			)
		cls.category=Category.objects.create(
				title='testcat',
				slug='testcatslug',
				status=True
			)
		cls.post=Post.objects.create(
				title='testpost',
				slug='testpostslug',
				author=cls.user,
				description='test description',
				thumbnail=SimpleUploadedFile(name='test_image.jpg', content=b'imagebinary', content_type='image/jpeg'),
				status=True
			)
		cls.post.category.add(cls.category)

	# def setUp(self):
	# 	print("setUp: Run once for every test method to setup clean data.")
	# 	pass

	def test_post_model(self):
		self.assertEqual(self.post.author.username, "testuser")
		self.assertListEqual([str(cat) for cat in self.post.category.all()], ["testcat"])
		self.assertEqual(self.post.thumbnail.readlines(), [b'imagebinary'])
		self.assertEqual(self.post.status,True)
