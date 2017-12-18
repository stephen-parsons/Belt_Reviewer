from __future__ import unicode_literals

from django.db import models

from ..main_app.models import Users

import re

AUTHOR_REGEX = re.compile(r"^[a-zA-Z ,.'-]+$")

class BookValidator(models.Manager):
	def AddBook(self, name, author_list, author_text, uploader):
		errors = []
		print str(author_text)
		if len(name) < 1:
			errors.append("Must have a title!")
		if len(Book.objects.filter(name=name)) > 0:
			errors.append("Book already in system!")	
		# if author_text < 1 and author_list == "":
		# 	errors.append("Must have author!")
		if len(author_text) > 0 and str(author_list) != "":		
			errors.append("Must input or select only one author!")
		elif len(author_text) > 0:
			if not AUTHOR_REGEX.match(str(author_text)):
				errors.append("Invalid author name!")
			else:
				names = author_text.split(" ", 1)
				author = Author.objects.create(first_name = names[0], last_name = names[1])
		elif str(author_list) != "":
			author = Author.objects.get(id = author_list)
		else:
			errors.append("Must have author!")		
		if len(errors) > 0:
			return errors
		else:
			user = Users.objects.get(id=uploader)
			new_book = Book.objects.create(name=name, uploader=user)
			new_book.authors.add(author)
			return new_book		

class Book(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	# uploader (user) to books
	uploader = models.ForeignKey(Users, related_name="books")
	objects = BookValidator()
	def __repr__(self):
		return "<Book object: {} {}>".format(self.name, self.desc)

class Author(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	# author to books and books to author
	books = models.ManyToManyField(Book, related_name="authors")	
	def __repr__(self):
		return "<Author object: {} {}>".format(self.first_name, self.last_name)

class ReviewValidator(models.Manager):
	def AddReview(self, content, rating, book, user):
		errors = []
		if len(content) < 1:
			errors.append("Must include review!") 	
		if len(rating) < 1:
			errors.append("Must include rating!")
		if len(errors) > 0:
			return errors
		else:
			book = Book.objects.get(id=book)
			user = Users.objects.get(id=user)
			new_review = Review.objects.create(content=content, rating=rating, book=book, user=user)
			return new_review	


class Review(models.Model):
	content = models.TextField(max_length=1000)
	rating = models.IntegerField()
	# review to books
	book = models.ForeignKey(Book, related_name="reviews")
	#review to user
	user = models.ForeignKey(Users, related_name = "reviews")
	objects = ReviewValidator()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	def __repr__(self):
		return "<Review object: {} {} {} {}>".format(self.content, self.rating, self.book, self.user)	


