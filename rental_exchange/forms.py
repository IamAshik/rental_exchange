from datetime import date

from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.forms import ModelForm, CheckboxSelectMultiple

from rental_exchange.models import Car, System, Contact, Feature, Fuel, Brand, Blog, CarRegistrationRequest, CarBooking, \
    Comment
from users.forms import UserCreationForm
from users.models import User


class CarForm(ModelForm):
    # features = forms.ModelMultipleChoiceField(
    #     queryset=Feature.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True)
    owner = forms.ModelChoiceField(queryset=User.objects.filter(user_type='CarOwner'))

    class Meta:
        model = Car
        widgets = {
            'fuels': CheckboxSelectMultiple(),
            'features': CheckboxSelectMultiple(),
        }
        fields = '__all__'


class SystemForm(forms.ModelForm):
    # email_from_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = System
        widgets = {
            'email_from_password': forms.PasswordInput(),
        }
        fields = '__all__'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['customer', 'is_seen']


class CarRegistrationRequestForm(forms.ModelForm):
    class Meta:
        model = CarRegistrationRequest
        fields = '__all__'
        exclude = ['is_seen']


# class CustomerRegistrationForm(UserCreationForm.Meta):
#     class Meta(UserCreationForm.Meta):
#         model = Customer
#         # I've tried both of these 'fields' declaration, result is the same
#         # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
#         fields = UserCreationForm.Meta.fields
#         exclude = ['user', 'created_by', 'updated_by']


# class CustomerRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         # I've tried both of these 'fields' declaration, result is the same
#         # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
#         fields = '__all__'
#         exclude = ['user', 'created_by', 'updated_by']

class FuelModelFormBS(BSModalModelForm):
    class Meta:
        model = Fuel
        fields = ['title', 'description']


class FeatureModelFormBS(BSModalModelForm):
    class Meta:
        model = Feature
        fields = ['title', 'description']


class BrandModelFormBS(BSModalModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'logo']


class BlogModelFormBS(BSModalModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'short_description', 'description']


class CreateBookingBSModalModelForm(BSModalModelForm):
    class Meta:
        model = CarBooking
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(format=('%m/%d/%Y'),
                                             attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                    'type': 'date', 'min': date.today()}),
        }


class CreateBookingForm(forms.ModelForm):
    class Meta:
        model = CarBooking
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(format=('%m/%d/%Y'),
                                             attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                    'type': 'date', 'min': date.today()}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'


