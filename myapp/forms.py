from django import forms
from .models import Book, Order, Review


class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices=FEEDBACK_CHOICES)
    options = forms.MultipleChoiceField(
        choices=[('option1', 'Option 1'), ('option2', 'Option 2')],  # replace with actual options
        widget=forms.CheckboxSelectMultiple
    )


class SearchForm(forms.Form):
    CATEGORY_CHOICES = Book.CATEGORY_CHOICES

    name = forms.CharField(
        max_length=100,
        required=False,
        label='Your Name'
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label='Select a category:'
    )
    max_price = forms.IntegerField(
        label='Maximum Price',
        min_value=0,
        required=True
    )

class OrderFormLab(forms.Form):
    CATEGORY_CHOICES = Book.CATEGORY_CHOICES

    name = forms.CharField(
        max_length=100,
        required=False,
        label='Your Name'
    )
    price = forms.IntegerField(
        label='Maximum Price',
        min_value=0,
        required=True
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {
            'books': forms.CheckboxSelectMultiple(),
            'order_type': forms.RadioSelect
        }
        labels = {
            'member': 'Member name',
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {
            'book': forms.RadioSelect(),
        }
        labels = {
            'reviewer': 'Please enter a valid email',
            'rating': 'Rating: An integer between 1 (worst) and 5 (best)'
        }
