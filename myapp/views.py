from datetime import datetime
import random

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Publisher, Book, Order, Review
from django.http import HttpResponse
from .forms import FeedbackForm, SearchForm, OrderForm, OrderFormLab, ReviewForm


def index(request):
    books = Book.objects.all()
    last_login = request.session.get('last_login')
    if last_login:
        message = f"Your last login was on {last_login}"
    else:
        message = "Your last login was more than one hour ago"
    return render(request, 'myapp/index0.html', {'booklist':books,'message': message})



# def about(request):
#     books = Book.objects.all()
#     return render(request, 'myapp/about0.html', {'books': books})


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'myapp/detail0.html', {'book': book})


def orders(request):
    purchased_orders = Order.objects.filter(status='Purchased')
    return render(request, 'myapp/orders.html', {'orders': purchased_orders})


def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = 'to borrow books.'
            elif feedback == 'P':
                choice = 'to purchase books.'
            else:
                choice = 'None.'
            message = f"You have chosen {choice}"
            return render(request, 'myapp/fb_results.html', {'message': message})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']

            # Filter books by max_price and category if provided
            books = Book.objects.filter(price__lte=max_price)
            if category:
                books = books.filter(category=category)

            booklist = books
            return render(request, 'myapp/results.html', {'name': name, 'category': category, 'booklist': booklist})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
    return render(request, 'myapp/findbooks.html', {'form': form})


def orderformlab(request):
    if request.method == 'POST':
        form = OrderFormLab(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']

            # booklist = books
            return render(request, 'myapp/results.html', {'name': name,'price':price})
        else:
            return HttpResponse('Invalid data')
    else:
        form = ()
    return render(request, 'myapp/orderlab.html', {'form': form})

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = order.member
            order_type = order.order_type
            order.save()
            if order_type == 1:
                for book in order.books.all():
                    member.borrowed_books.add(book)
            return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save()
                book = review.book
                book.num_reviews += 1
                book.save()
                return redirect('index')  # assuming you have a view named 'index'
            else:
                form.add_error('rating', 'You must enter a rating between 1 and 5!')
    else:
        form = ReviewForm()
    return render(request, 'myapp/review.html', {'form': form})

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(3600)  # Set session expiry to 1 hour
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))

@login_required
def chk_reviews(request, book_id):
    user = request.user
    if user.groups.filter(name='Member').exists():
        reviews = Review.objects.filter(book_id=book_id)
        if reviews.exists():
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            return render(request, 'myapp/chk_reviews.html', {'avg_rating': avg_rating})
        else:
            return render(request, 'myapp/chk_reviews.html', {'message': 'No reviews for this book.'})
    else:
        return render(request, 'myapp/chk_reviews.html', {'message': 'You are not a registered member!'})

def about(request):


    books = Book.objects.all()

    mynum = request.COOKIES.get('lucky_num')
    if not mynum:
        mynum = str(random.randint(1, 100))
    response = render(request, 'myapp/about0.html', {'books':books,'mynum': mynum})
    response.set_cookie('lucky_num', mynum, max_age=300)  # 5 minutes
    return response
