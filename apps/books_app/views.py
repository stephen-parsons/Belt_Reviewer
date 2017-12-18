from django.shortcuts import render, redirect
from .models import *
from ..main_app import *
from django.contrib import messages

def index(request):
	reviews = Review.objects.all().order_by('-created_at')[:3]
	books_to_exclude = [review.book.id for review in reviews]
	books = Book.objects.all().exclude(id__in=books_to_exclude)
	user = Users.objects.get(id=request.session['user_id'])
	return render(request, "books_app/index.html", {'reviews' : reviews, 'user' : user, 'books' : books})

def book_add(request):
	user = Users.objects.get(id=request.session['user_id'])
	authors = Author.objects.all()
	return render(request, "books_app/books_add.html", {'authors' : authors, 'user' : user})

def book_process(request):
	print request.POST
	user = Users.objects.get(id=request.session['user_id'])
	new_book = Book.objects.AddBook(
		request.POST['name'],
		request.POST['author_list'],
		request.POST['author_text'],
		user.id
		)
	if type(new_book) is list:
		for error in new_book:
			messages.add_message(request, messages.ERROR, error)
		return redirect('/books/add')
	new_review = Review.objects.AddReview(
		request.POST['review'],
		request.POST['rating'],
		new_book.id,
		user.id
		)
	if type(new_review) is list:
		for error in new_review:
			messages.add_message(request, messages.ERROR, error)
		author = new_book.authors.first()
		if len(Author.objects.filter(first_name=author.first_name, last_name=author.last_name)) < 1:
			author.delete()
		new_book.delete()	
		return redirect('/books/add')	
	return redirect("/books/{}".format(new_book.id))

def book_review(request, id):
	user = Users.objects.get(id=request.session['user_id'])
	book = Book.objects.get(id=id)
	return render(request, "books_app/book_review_add.html", {'book' : book, 'user' : user})	

def book_add_review(request, id):
	# book = Book.objects.get(id=id)
	new_review = Review.objects.AddReview(
		request.POST['review'],
		request.POST['rating'],
		id,
		request.session['user_id']
		)
	if type(new_review) is list:
		for error in new_review:
			messages.add_message(request, messages.ERROR, error)	
	return redirect('/books/{}'.format(id))	

def delete_review(request, book_id, comment_id):
	review = Review.objects.get(id=comment_id)
	review.delete()
	return redirect('/books/{}'.format(book_id))	 	 
	
