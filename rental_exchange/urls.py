from django.urls import path
from rental_exchange import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/details/<int:pk>/', views.BlogDetailView.as_view(), name='blog-details'),
    path('customer/profile/<int:pk>/', views.ProfileDetailView.as_view(), name='customer-profile'),
    path('customer/booking/list/', views.BookingListView.as_view(), name='customer-bookings'),
    # path('customer/booking/create/<int:car_id>/', views.CarBookingBSModalCreateView.as_view(), name='customer-booking-create-bsm'),
    # path('blog-detail', views.blog_detail_view, name='blog-detail'),
    path('pricing', views.pricing_view, name='pricing'),
    path('contact', views.contact_view, name='contact'),
    path('car/', views.CarListView.as_view(), name='car'),
    # path('car/<id>/', views.car_detail_view, name='car-detail'),
    # path('car-detail', views.car_detail_view, name='car-detail'),
    path('car/details/<int:pk>/', views.CarDetailView.as_view(), name='car-detail'),
    path('contact/create/', views.ContactCreate.as_view(), name='contact_create'),
    path('request/car/registration/', views.home_view, name='car-registration-request'),
]