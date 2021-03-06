from datetime import date

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalReadView, BSModalDeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, ListView, DetailView, FormView, TemplateView

from RE import settings
from RE.settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from rental_exchange.forms import ContactForm, CarForm, FuelModelFormBS, FeatureModelFormBS, BrandModelFormBS, \
    BlogModelFormBS, SystemForm
from rental_exchange.models import Car, System, Contact, Brand, Blog, Feature, Fuel, CarBooking, CarRegistrationRequest, \
    PaymentHistory, TransactionHistory, VehicleOwnerAccount
from users.forms import UserCreationForm, OwnerCreationForm, LoginForm, AdminCreationForm
from users.models import User


def is_staff(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff, login_url=settings.ADMIN_LOGIN_URL)
def admin_home_view(request):
    context = {
        "title": "Dashboard | Rental Exchange Administration",
        "admin_list": User.objects.filter(user_type='Admin'),
        "owner_list": User.objects.filter(user_type='CarOwner'),
        "customer_list": User.objects.filter(user_type='Customer'),
        "booking_list": CarBooking.objects.filter(request_status='Pending'),
        "system_data": System.objects.all()
    }
    return render(request, 'rental_exchange/admin/containers/home.html', context)


# class DashboardView(TemplateView):
#     template_name = 'rental_exchange/admin/containers/home.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(DashboardView, self).get_context_data(**kwargs)
#         context['admin_list'] = User.objects.filter(user_type='Admin')
#         context['owner_list'] = User.objects.filter(user_type='CarOwner')
#         context['customer_list'] = User.objects.filter(user_type='Customer')
#         context['booking_list'] = CarBooking.objects.filter(request_status='Pending')
#         return context


def admin_car_view(request):
    page_title = "Car | Rental Exchange Administration"
    cars = Car.objects.all()
    context = {
        "title": page_title,
        "cars": cars
    }
    return render(request, 'rental_exchange/admin/containers/car/car-list.html', context)


def admin_brand_view(request):
    page_title = "Brands | Rental Exchange Administration"
    brands = Brand.objects.all()
    context = {
        "title": page_title,
        "brands": brands
    }
    return render(request, 'rental_exchange/admin/containers/brand/brand-list.html', context)


def admin_feature_view(request):
    page_title = "Features | Rental Exchange Administration"
    features = Feature.objects.all()
    context = {
        "title": page_title,
        "features": features
    }
    return render(request, 'rental_exchange/admin/containers/feature/feature-list.html', context)


def admin_fuel_view(request):
    page_title = "Fuel Types | Rental Exchange Administration"
    fuels = Fuel.objects.all()
    context = {
        "title": page_title,
        "fuels": fuels
    }
    return render(request, 'rental_exchange/admin/containers/fuel/fuel-list.html', context)


def admin_blog_view(request):
    page_title = "Blog | Rental Exchange Administration"
    blogs = Blog.objects.all()
    context = {
        "title": page_title,
        "blogs": blogs
    }
    return render(request, 'rental_exchange/admin/containers/blog/blog-list.html', context)


def admin_contact_view(request):
    page_title = "Contacts | Rental Exchange Administration"
    contacts = Contact.objects.all()
    context = {
        "title": page_title,
        "contacts": contacts
    }
    return render(request, 'rental_exchange/admin/containers/contact/contact-list.html', context)


def admin_user_view(request):
    page_title = "Users | Rental Exchange Administration"
    users = User.objects.all()
    context = {
        "title": page_title,
        "users": users
    }
    return render(request, 'rental_exchange/admin/containers/user-list.html', context)


class AdminListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'rental_exchange/admin/containers/user/admin-list.html'

    def get_queryset(self):
        obj = User.objects.filter(user_type='Admin')
        return obj

    def get_context_data(self, **kwargs):
        context = super(AdminListView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class AdminCreateView(FormView):
    template_name = 'rental_exchange/admin/containers/user/admin-create.html'
    form_class = AdminCreationForm
    success_message = 'Admin is successfully added.'
    success_url = reverse_lazy('admin-admin-list')

    def get_initial(self):
        initial = super(AdminCreateView, self).get_initial()
        initial['user_type'] = 'Admin'
        initial['is_staff'] = True
        return initial

    def form_valid(self, form):
        """ process user signup"""
        user = form.save(commit=False)
        user.user_type = 'Admin'
        user.is_staff = True
        user.save()
        messages.success(self.request, 'Admin is successfully added.')
        if user is not None:
            return HttpResponseRedirect(self.success_url)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AdminCreateView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class OwnerListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'rental_exchange/admin/containers/user/owner-list.html'

    def get_queryset(self):
        obj = User.objects.filter(user_type='CarOwner')
        return obj

    def get_context_data(self, **kwargs):
        context = super(OwnerListView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class OwnerCreateView(FormView):
    template_name = 'rental_exchange/admin/containers/user/owner-create.html'
    form_class = OwnerCreationForm
    success_message = 'Owner is successfully registered.'
    success_url = reverse_lazy('admin-owner-list')

    def get_initial(self):
        initial = super(OwnerCreateView, self).get_initial()
        initial['user_type'] = 'CarOwner'
        initial['is_staff'] = True
        return initial

    def form_valid(self, form):
        """ process user signup"""
        user = form.save(commit=False)
        user.user_type = 'CarOwner'
        user.is_staff = True
        user.save()
        messages.success(self.request, 'Owner is successfully registered.')
        if user is not None:
            return HttpResponseRedirect(self.success_url)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OwnerCreateView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class CustomerListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'rental_exchange/admin/containers/user/customer-list.html'

    def get_queryset(self):
        obj = User.objects.filter(user_type='Customer')
        return obj

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class SystemListView(ListView):
    model = System
    context_object_name = 'systems'
    template_name = 'rental_exchange/admin/containers/system/site-default.html'

    def get_context_data(self, **kwargs):
        context = super(SystemListView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class SystemCreateView(SuccessMessageMixin, CreateView):
    model = System
    form_class = SystemForm
    template_name = 'rental_exchange/admin/containers/system/site-default-create.html'
    success_url = reverse_lazy('admin-site-default')
    success_message = 'System Info Added Successfully'

    def get_context_data(self, **kwargs):
        context = super(SystemCreateView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class SystemUpdateView(SuccessMessageMixin, UpdateView):
    model = System
    form_class = SystemForm
    template_name = "rental_exchange/admin/containers/system/site-default-update.html"
    success_url = reverse_lazy('admin-site-default')
    success_message = 'System Info Updated Successfully'

    def get_context_data(self, **kwargs):
        context = super(SystemUpdateView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


def admin_profile_view(request):
    page_title = "Profile | Rental Exchange Administration"
    context = {
        "title": page_title
    }
    return render(request, 'rental_exchange/admin/containers/profile.html', context)


class AdminProfileView(TemplateView):
    template_name = 'rental_exchange/admin/containers/profile.html'


class CarCreateView(SuccessMessageMixin, CreateView):
    model = Car
    # fields = '__all__'
    form_class = CarForm
    template_name = "rental_exchange/admin/containers/car/car-create-view.html"
    success_url = reverse_lazy('admin-cars')
    success_message = 'Car Added Successfully'

    def get_context_data(self, **kwargs):
        context = super(CarCreateView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context
    # def form_valid(self, form):
    #     form.save()
    #     return super(CarCreateView, self).form_valid(form)


class CarUpdateView(SuccessMessageMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = "rental_exchange/admin/containers/car/car-update-view.html"
    success_url = reverse_lazy('admin-cars')
    success_message = 'Car Updated Successfully'

    def get_context_data(self, **kwargs):
        context = super(CarUpdateView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class CarBSModalReadView(BSModalReadView):
    model = Car
    context_object_name = 'car'
    template_name = 'rental_exchange/admin/containers/car/car-details-view-bsm.html'


# < Fuel Type Views >
class FuelBSModalCreateViewOnCar(BSModalCreateView):
    template_name = 'rental_exchange/admin/containers/fuel/fuel-create-view-bs.html'
    form_class = FuelModelFormBS
    success_message = 'Fuel is successfully added.'
    success_url = reverse_lazy('admin-car-create')


class FuelBSModalCreateView(BSModalCreateView):
    template_name = 'rental_exchange/admin/containers/fuel/fuel-create-view-bs.html'
    form_class = FuelModelFormBS
    success_message = 'Fuel is successfully added.'
    success_url = reverse_lazy('admin-fuels')


class FuelBSModalUpdateView(BSModalUpdateView):
    model = Fuel
    template_name = 'rental_exchange/admin/containers/fuel/fuel-update-view-bs.html'
    form_class = FuelModelFormBS
    success_message = 'Fuel is successfully updated.'
    success_url = reverse_lazy('admin-fuels')


class FuelBSModalReadView(BSModalReadView):
    model = Fuel
    template_name = 'rental_exchange/admin/containers/fuel/fuel-read-view-bs.html'


class FuelBSModalDeleteView(BSModalDeleteView):
    model = Fuel
    template_name = 'rental_exchange/admin/containers/fuel/fuel-delete-view-bs.html'
    success_message = 'Fuel Type was deleted.'
    success_url = reverse_lazy('admin-fuels')


# < Fuel Type Views />


# < Features Views >
class FeatureBSModalCreateViewOnCar(BSModalCreateView):
    template_name = 'rental_exchange/admin/containers/feature/feature-create-view-bs.html'
    form_class = FeatureModelFormBS
    success_message = 'Feature is successfully added.'
    success_url = reverse_lazy('admin-car-create')


class FeatureBSModalCreateView(BSModalCreateView):
    template_name = 'rental_exchange/admin/containers/feature/feature-create-view-bs.html'
    form_class = FeatureModelFormBS
    success_message = 'Feature is successfully added.'
    success_url = reverse_lazy('admin-features')


class FeatureBSModalUpdateView(BSModalUpdateView):
    model = Feature
    template_name = 'rental_exchange/admin/containers/feature/feature-update-view-bs.html'
    form_class = FeatureModelFormBS
    success_message = 'Feature is successfully updated.'
    success_url = reverse_lazy('admin-features')


class FeatureBSModalReadView(BSModalReadView):
    model = Feature
    template_name = 'rental_exchange/admin/containers/feature/feature-read-view-bs.html'


class FeatureBSModalDeleteView(BSModalDeleteView):
    model = Feature
    template_name = 'rental_exchange/admin/containers/feature/feature-delete-view-bs.html'
    success_message = 'Feature was deleted.'
    success_url = reverse_lazy('admin-features')


# < Features Views />


# < Brand Views >
class BrandBSModalCreateViewOnCar(BSModalCreateView):
    template_name = 'rental_exchange/admin/containers/brand/brand-create-view-bs.html'
    form_class = BrandModelFormBS
    success_message = 'Brand is successfully added.'
    success_url = reverse_lazy('admin-car-create')


class BrandBSModalCreateView(BSModalCreateView):
    template_name = 'rental_exchange/admin/containers/brand/brand-create-view-bs.html'
    form_class = BrandModelFormBS
    success_message = 'Brand is successfully added.'
    success_url = reverse_lazy('admin-brands')


class BrandBSModalUpdateView(BSModalUpdateView):
    model = Brand
    template_name = 'rental_exchange/admin/containers/brand/brand-update-view-bs.html'
    form_class = BrandModelFormBS
    success_message = 'Brand is successfully updated.'
    success_url = reverse_lazy('admin-brands')


class BrandBSModalReadView(BSModalReadView):
    model = Brand
    template_name = 'rental_exchange/admin/containers/brand/brand-read-view-bs.html'


class BrandBSModalDeleteView(BSModalDeleteView):
    model = Brand
    template_name = 'rental_exchange/admin/containers/brand/brand-delete-view-bs.html'
    success_message = 'Brand was deleted.'
    success_url = reverse_lazy('admin-brands')


# < Brand Views />


# < Blog Views >
class BlogBSModalCreateView(BSModalCreateView):
    template_name = 'rental_exchange/admin/containers/blog/blog-create-view-bs.html'
    form_class = BlogModelFormBS
    success_message = 'Blog is successfully added.'
    success_url = reverse_lazy('admin-blog')


class BlogBSModalUpdateView(BSModalUpdateView):
    model = Blog
    template_name = 'rental_exchange/admin/containers/blog/blog-update-view-bs.html'
    form_class = BlogModelFormBS
    success_message = 'Blog is successfully updated.'
    success_url = reverse_lazy('admin-blog')


class BlogBSModalReadView(BSModalReadView):
    model = Blog
    template_name = 'rental_exchange/admin/containers/blog/blog-read-view-bs.html'


class BlogBSModalDeleteView(BSModalDeleteView):
    model = Blog
    template_name = 'rental_exchange/admin/containers/blog/blog-delete-view-bs.html'
    success_message = 'Blog was deleted.'
    success_url = reverse_lazy('admin-blog')


# < Blog Views />


class VehicleAddRequestListView(ListView):
    model = CarRegistrationRequest
    context_object_name = 'vehicle_add_request_list'
    template_name = 'rental_exchange/admin/containers/contact/vehicle-add-request-list.html'

    def get_context_data(self, **kwargs):
        context = super(VehicleAddRequestListView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class VehicleAddRequestBSModalReadView(BSModalReadView):
    model = CarRegistrationRequest
    context_object_name = 'var'
    template_name = 'rental_exchange/admin/containers/contact/vehicle-add-request-read-view-bsm.html'


class BookingListView(ListView):
    model = CarBooking
    context_object_name = 'bookings'
    template_name = 'rental_exchange/admin/containers/booking/booking-list.html'

    def get_queryset(self):
        obj = CarBooking.objects.all().order_by('-created_at')
        return obj

    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class BookingBSModalReadView(BSModalReadView):
    model = CarBooking
    context_object_name = 'bookings'
    template_name = 'rental_exchange/admin/containers/booking/booking-details-view-bsm.html'


class BookingBSModalDeleteView(BSModalDeleteView):
    model = CarBooking
    context_object_name = 'booking'
    template_name = 'rental_exchange/admin/containers/booking/booking-reject-view-bsm.html'
    success_message = 'Booking request was deleted.'
    success_url = reverse_lazy('admin-booking-list')


def update_booking_request_status(request, b_id, status):
    obj = CarBooking.objects.get(pk=b_id)
    obj.request_status = status
    obj.save()
    messages.success(request, 'Request has been %s' % status)
    return redirect('admin-booking-list')


def update_booking_payment_status(request, b_id, status):
    obj = CarBooking.objects.get(pk=b_id)
    obj.payment_status = status
    obj.request_status = 'Confirmed'
    obj.rent_status = 'On Going'
    obj.save()
    PaymentHistory.objects.create(booking=obj, amount=obj.rental_cost)
    owner_percentage = obj.rental_cost * .75
    TransactionHistory.objects.create(booking=obj, added_amount=owner_percentage)
    messages.success(request, 'Payment has been %s' % status)
    return redirect('admin-booking-list')


class UserProfileDetailView(DetailView):
    model = User
    context_object_name = 'user_profile'
    template_name = 'rental_exchange/admin/containers/user/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class PaymentHistoryListView(ListView):
    model = PaymentHistory
    context_object_name = 'payment_history'
    template_name = 'rental_exchange/admin/containers/payments_and_accounts/payment-history-list.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentHistoryListView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class TransactionHistoryListView(ListView):
    model = TransactionHistory
    context_object_name = 'transaction_history'
    template_name = 'rental_exchange/admin/containers/payments_and_accounts/transaction-history-list.html'

    def get_context_data(self, **kwargs):
        context = super(TransactionHistoryListView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


class VehicleOwnerAccountListView(ListView):
    model = VehicleOwnerAccount
    context_object_name = 'vehicle_owner_accounts'
    template_name = 'rental_exchange/admin/containers/payments_and_accounts/vehicle-owner-account-list.html'

    def get_context_data(self, **kwargs):
        context = super(VehicleOwnerAccountListView, self).get_context_data(**kwargs)
        context['system_data'] = System.objects.all()
        return context


def update_transaction_payment_status(request, t_id):
    obj = TransactionHistory.objects.get(pk=t_id)
    obj.is_paid = True
    obj.save()
    accounts = VehicleOwnerAccount.objects.filter(account_holder=obj.booking.car.owner)
    if accounts.exists():
        for acc in accounts:
            acc.total_income = acc.total_income + obj.added_amount
            acc.last_added_amount = obj.added_amount
            acc.save()
    else:
        VehicleOwnerAccount.objects.create(account_holder=obj.booking.car.owner, total_income=obj.added_amount,
                                           last_added_amount=obj.added_amount)
    messages.success(request, 'Payment has been completed to %s' % obj.booking.car.owner)
    return redirect('admin-transaction-history-list')


def admin_blank_view(request):
    context = {
        "title": "Blank - Rental Exchange"
    }
    return render(request, 'rental_exchange/admin/containers/blank.html', context)
