from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Publisher, Book, Order
from django.http import HttpResponse
from .forms import FeedbackForm, SearchForm, OrderForm, OrderFormLab, ReviewForm


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'booklist': booklist})



def about(request):
    books = Book.objects.all()
    return render(request, 'myapp/about0.html', {'books': books})


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