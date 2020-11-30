from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin, FormView

from RE import settings
from RE.settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from rental_exchange.forms import ContactForm, CarRegistrationRequestForm, CreateBookingBSModalModelForm, \
    CreateBookingForm, CommentForm
from rental_exchange.models import Car, System, Contact, CarRegistrationRequest, Blog, CarBooking, Comment
from users.forms import UserCreationForm
from users.models import User


def home_view(request):
    cars = Car.objects.filter(is_active=True, is_published=True, is_featured=True)
    car_registration_request_form = CarRegistrationRequestForm(request.POST or None)
    if car_registration_request_form.is_valid():
        car_registration_request_form.save()
        messages.success(request, 'Request has been submitted successfully')
        return redirect('home')
    context = {
        "title": "Home | Rental Exchange",
        "cars": cars,
        "car_registration_request_form": car_registration_request_form
    }
    return render(request, 'rental_exchange/containers/home.html', context)


def about_view(request):
    context = {
        "title": "About | Rental Exchange"
    }
    return render(request, 'rental_exchange/containers/about.html', context)


def blog_view(request):
    blog_list = Blog.objects.all()
    context = {
        "title": "Blog | Rental Exchange",
        "blog_list": blog_list
    }
    return render(request, 'rental_exchange/containers/blog.html', context)


def blog_detail_view(request):
    context = {
        "title": "Blog Details | Rental Exchange"
    }
    return render(request, 'rental_exchange/containers/blog-single.html', context)


def contact_view(request):
    system_info = System.objects.all()
    form = ContactForm
    context = {
        "system_info": system_info.first(),
        "title": "Contact | Rental Exchange",
        "form": form
    }
    return render(request, 'rental_exchange/containers/contact.html', context)


def pricing_view(request):
    context = {
        "title": "Pricing | Rental Exchange"
    }
    return render(request, 'rental_exchange/containers/pricing.html', context)


def car_view(request):
    context = {
        "title": "Car | Rental Exchange"
    }
    return render(request, 'rental_exchange/containers/car.html', context)


def car_detail_view(request):
    context = {
        "title": "Car Detail | Rental Exchange"
    }
    return render(request, 'rental_exchange/containers/car-single.html', context)


def is_staff(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff, login_url=settings.ADMIN_LOGIN_URL)
def admin_home_view(request):
    context = {
        "title": "Dashboard | Rental Exchange Administration"
    }
    return render(request, 'rental_exchange/admin/containers/home.html', context)


def admin_car_view(request):
    page_title = "Car | Rental Exchange Administration"
    context = {
        "title": page_title
    }
    return render(request, 'rental_exchange/admin/containers/car-list.html', context)


def admin_brand_view(request):
    page_title = "Brands | Rental Exchange Administration"
    context = {
        "title": page_title
    }
    return render(request, 'rental_exchange/admin/containers/brand-list.html', context)


def admin_feature_view(request):
    page_title = "Features | Rental Exchange Administration"
    context = {
        "title": page_title
    }
    return render(request, 'rental_exchange/admin/containers/feature-list.html', context)


def admin_blog_view(request):
    page_title = "Blog | Rental Exchange Administration"
    context = {
        "title": page_title
    }
    return render(request, 'rental_exchange/admin/containers/blog-list.html', context)


def admin_contact_view(request):
    page_title = "Contacts | Rental Exchange Administration"
    context = {
        "title": page_title
    }
    return render(request, 'rental_exchange/admin/containers/contact-list.html', context)


def admin_user_view(request):
    page_title = "Users | Rental Exchange Administration"
    context = {
        "title": page_title
    }
    return render(request, 'rental_exchange/admin/containers/user-list.html', context)


def admin_site_default_view(request):
    page_title = "Site Default | Rental Exchange Administration"
    context = {
        "title": page_title
    }
    return render(request, 'rental_exchange/admin/containers/site-default.html', context)


def admin_profile_view(request):
    page_title = "Profile | Rental Exchange Administration"
    context = {
        "title": page_title
    }
    return render(request, 'rental_exchange/admin/containers/profile.html', context)


def admin_blank_view(request):
    context = {
        "title": "Blank - Rental Exchange"
    }
    return render(request, 'rental_exchange/admin/containers/blank.html', context)


class CarDetailView(FormMixin, generic.DetailView):
    model = Car
    template_name = 'rental_exchange/containers/car-single.html'
    form_class = CreateBookingForm
    success_message = 'Your Booking Request Has Been Sent Successfully'

    def get_success_url(self):
        # return reverse('car-detail', kwargs={'pk': self.object.id})
        return reverse_lazy('customer-bookings')

    def get_context_data(self, **kwargs):
        context = super(CarDetailView, self).get_context_data(**kwargs)
        context['form'] = CreateBookingForm(initial={'car': self.object, 'customer': self.request.user})
        # , 'customer': self.request.user
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        rent_for = int(form.cleaned_data['rent_for'])
        car = Car.objects.get(pk=self.kwargs['pk'])
        rental_price = car.rental_price.amount
        form.instance.rental_cost = round((rent_for * rental_price), 2)
        form.save()
        messages.success(self.request, 'Your Booking Request Has Been Sent Successfully')
        return super(CarDetailView, self).form_valid(form)


class ContactCreate(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "rental_exchange/containers/contact.html"
    success_url = reverse_lazy('contact')
    success_message = "Message has been sent successfully"

    def form_valid(self, form):
        # return HttpResponseRedirect(self.get_success_url())
        # form.send_email()
        email_from = DEFAULT_FROM_EMAIL
        email_to = DEFAULT_TO_EMAIL
        system_data = System.objects.all().first()
        # if system_data is not None:
        #     email_from = system_data.email_from
        #     email_to = system_data.email_to
        send_mail(
            form.cleaned_data['subject'],
            form.cleaned_data['message'],
            email_from,
            [email_to],
            fail_silently=False,
        )
        return super(ContactCreate, self).form_valid(form)


# class CarRegistrationRequestCreateView(SuccessMessageMixin, CreateView):
#     model = CarRegistrationRequest
#     form_class = CarRegistrationRequestForm
#     template_name = "rental_exchange/containers/home.html"
#     success_url = reverse_lazy('home')
#     success_message = "Request has been submitted successfully"


class BlogDetailView(FormMixin, DetailView):
    # specify the model to use
    model = Blog
    form_class = CommentForm
    template_name = 'rental_exchange/containers/blog-single.html'

    def get_success_url(self):
        return reverse_lazy('blog-details', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm(initial={'blog': self.object, 'created_by': self.request.user})
        context['comment_list'] = Comment.objects.filter(blog=self.object)
        context['recent_blog_list'] = Blog.objects.all().order_by('-created_by')[:5]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your Comment Is Successfully Posted')
        return super(BlogDetailView, self).form_valid(form)


class ProfileDetailView(DetailView):
    # specify the model to use
    model = User
    context_object_name = 'user_profile'
    template_name = 'rental_exchange/containers/profile.html'


class BookingListView(ListView):
    # specify the model to use
    model = CarBooking
    context_object_name = 'bookings'
    template_name = 'rental_exchange/containers/bookings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking_requests'] = CarBooking.objects.filter(customer=self.request.user, request_status__in=['Pending', 'Accepted'])
        context['booked_cars'] = CarBooking.objects.filter(customer=self.request.user, rent_status='On Going')
        return context


class CarListView(ListView):
    model = Car
    context_object_name = 'cars'
    template_name = 'rental_exchange/containers/car.html'

    def get_queryset(self):
        # qs = super().get_queryset()
        # filter by a variable captured from url, for example
        bookings = CarBooking.objects.filter(Q(rent_status='On Going') | Q(request_status='Pending') | Q(request_status='Accepted'))
        arr = []
        for b in bookings:
            arr.append(b.car.pk)
        obj = Car.objects.filter(is_active=True, is_published=True).exclude(id__in=arr)
        # return qs.filter(name__startswith=self.kwargs['name'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_cars'] = Car.objects.filter(is_active=True, is_published=True, is_featured=True)
        return context
