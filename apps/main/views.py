from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import *

#helper functions
def current_user(request):
	if 'user_id' in request.session:
		return User.objects.get(id=request.session['user_id'])

# Create your views here.
def index(request):
	return render(request, 'main/index.html')

def createUser(request):
	if request.method != 'POST':
		return redirect('/')
	attempt = User.objects.validateUser(request.POST)
	if attempt['status'] == True:
		user = User.objects.createUser(request.POST)
		request.session['user_id'] = user.id
		return redirect('/books')
	else:
		for error in attempt['errors']:
			messages.add_message(request, messages.ERROR, error, extra_tags="registration")
			return redirect('/')

def loginUser(request):
	if request.method != 'POST':
		return redirect('/')
	attempt = User.objects.loginUser(request.POST)
	if attempt['status'] == True:
		request.session['user_id'] = attempt['user'].id
		return redirect('/books')
	else:
		messages.add_message(request, messages.ERROR, attempt['message'], extra_tags="login")
		return redirect('/')

def indexBook(request):
	duplicate_reviews = Review.objects.order_by('-created_at').all()[3:]
	other_book_reviews = []
	for review in duplicate_reviews:
		if review.book not in other_book_reviews:
			other_book_reviews.append(review.book)

	context = {
		'current_user': current_user(request),
		'recent_book_reviews': Review.objects.order_by('-created_at').all()[:3],
		'other_book_reviews': other_book_reviews,
	}
	return render(request, 'main/books.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')

def newBook(request):
	#get authors from DB
	context = {
		'authors': Author.objects.all(),
	}
	#display a form for creating a new book and a review
	return render(request, 'main/new_book.html', context)

def createBookAndReview(request):
	#validate the form
	attempt = Review.objects.validateBookAndReview(request.POST)
	if attempt['status'] == True:
		#create author if need be
		if 'list_author' not in request.POST:
			find_author = Author.objects.filter(name=request.POST.get('new_author')).first()
			if not find_author:
				author = Author.objects.create(name=request.POST.get('new_author'))
			else:
				author = find_author
		else:
			author = Author.objects.get(id=request.POST.get('list_author'))
		#create book
		book = Book.objects.create(
			title=request.POST.get('title'),
			author=author
		)
		#create review
		Review.objects.create(
			review=request.POST.get('review'),
			rating=request.POST.get('rating'),
			book=book,
			user=current_user(request)
		)
		return redirect('/books')
	else:
		for error in attempt['errors']:
			messages.add_message(request, messages.ERROR, error, extra_tags="new_book")
			return redirect('/books/new')
	print request.POST
	return redirect('/books/new')

def showBook(request, id):
	book = Book.objects.filter(id=id).first()
	context = {
		'book': book,
		'reviews': book.reviews.select_related('user').all(),
		'current_user': current_user(request),
	}
	return render(request, 'main/show_book.html', context)

def deleteReview(request, id):
	review = Review.objects.filter(id=id).first()
	if review:
		review.delete()
	return redirect('/books')

def createReview(request, id):
	#validate the form
	attempt = Review.objects.validateReview(request.POST)
	if attempt['status'] == True:
		#create Review
		Review.objects.create(
			review=request.POST.get('review'),
			rating=request.POST.get('rating'),
			book=Book.objects.get(id=id),
			user=current_user(request)
		)
		return redirect('/books')
		pass
	else:
		for error in attempt['errors']:
			messages.add_message(request, messages.ERROR, error, extra_tags="new_review")
		return redirect('/books/{}'.format(id))

def showUser(request, id):
	user = User.objects.annotate(num_reviews=Count('reviews')).filter(id=id).first()
	if user:
		reviews = user.reviews.all()
		new_reviews = []
		for review in reviews:
			if review.book not in new_reviews:
				new_reviews.append(review.book)
	context = {
		'user': user,
		'reviews': new_reviews,
	}
	return render(request, 'main/user_show.html', context)




