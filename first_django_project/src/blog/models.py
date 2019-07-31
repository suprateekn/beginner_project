from django.db import models
from django.conf import settings

class BlogPostQuerySet(models.QuerySet):
	def search(self, query):
		return self.filter(title__iexact = query)

class BlogPostManager(models.Manager):
	def get_queryset(self):
		return BlogPostQuerySet(self.model, using = self._db)
		
	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().search()

User = settings.AUTH_USER_MODEL
class BlogPost(models.Model):
	user = models.ForeignKey(User, default = 1, null=True, on_delete = models.SET_NULL)
	image = models.ImageField(upload_to='image/', blank = True, null = True)
	title = models.CharField(max_length = 120)
	slug = models.SlugField(unique=True)
	content = models.TextField(null=True, blank = True)
	publish_date = models.DateTimeField(auto_now = False, auto_now_add = False, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now=True)

	objects = BlogPostManager()