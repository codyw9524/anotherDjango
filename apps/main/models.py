from __future__ import unicode_literals

from django.db import models
import re, bcrypt

# Create your models here.
class UserManager(models.Manager):
	def validateUser(self, post):
		is_valid = True
		errors = []
		if len(post.get('name')) == 0:
			errors.append('Name must not be blank')
			is_valid = False
		user = User.objects.filter(email=post.get('email')).first()
		if user:
			errors.append('This email is already in use.')
			is_valid = False
		if not re.search(r'\w+\@\w+\.\w+', post.get('email')):
			errors.append('You must provide a valid email.')
			is_valid = False
		if len(post.get('password')) < 4:
			errors.append('Your password must exceed three characters.')
			is_valid = False
		if post.get('password') != post.get('password_confirmation'):
			errors.append('Your passwords do not match.')
			is_valid = False
		return {'status': is_valid, 'errors': errors}

	def createUser(self, post):
		return User.objects.create(
			name=post.get('name'),
			email=post.get('email'),
			password=bcrypt.hashpw(post.get('password').encode(), bcrypt.gensalt())
		)

	def loginUser(self, post):
		user = User.objects.filter(email=post.get('email')).first()
		if user and bcrypt.hashpw(post.get('password').encode(), user.password.encode()) == user.password:
			return {'status': True, 'user': user}
		else:
			return {'status': False, 'message': 'Invalid credentials.'}

class ReviewManager(models.Manager):
	def validateBookAndReview(self, post):
		is_valid = True
		errors = []
		if len(post.get('title')) == 0:
			errors.append('Your title must not be blank')
			is_valid = False
		if len(post.get('review')) == 0:
			errors.append('Review must not be blank')
			is_valid = False
		if post.get('rating') == '':
			errors.append('Your rating is invalid')
			is_valid = False
		elif int(post.get('rating')) < 0 or int(post.get('rating')) > 5:
			errors.append('Your rating is invalid')
			is_valid = False
		if 'list_author' not in post and len(post.get('new_author')) == 0:
			errors.append('You must select or create an author')
			is_valid = False
		if 'list_author' in post and len(post.get('new_author')) > 0:
			errors.append('Only one author may be selected')
			is_valid = False
		return {'status': is_valid, 'errors': errors}

	def validateReview(self, post):
		is_valid = True
		errors = []
		if len(post.get('review')) == 0:
			errors.append('Review must not be blank')
		if post.get('rating') == '':
			errors.append('Your rating is invalid')
			is_valid = False
		elif int(post.get('rating')) < 0 or int(post.get('rating')) > 5:
			errors.append('Your rating is invalid')
			is_valid = False
		return {'status': is_valid, 'errors': errors}


class User(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Author(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.ForeignKey(Author, related_name="books")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
	review = models.TextField()
	rating = models.IntegerField()
	user = models.ForeignKey(User, related_name="reviews")
	book = models.ForeignKey(Book, related_name="reviews")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ReviewManager()












