from django.urls import path
from rental_exchange import views_admin as views

urlpatterns = [
    # admin
    path('', views.admin_home_view, name='admin-home'),
    # car
    path('car/list/', views.admin_car_view, name='admin-cars'),
    path('car/add/', views.CarCreateView.as_view(), name='admin-car-create'),
    path('car/update/<int:pk>/', views.CarUpdateView.as_view(), name='admin-car-update'),
    path('car/fuel/add/', views.FuelBSModalCreateViewOnCar.as_view(), name='admin-fuel-bsm-create-on-car'),
    path('car/brand/add/', views.BrandBSModalCreateViewOnCar.as_view(), name='admin-brand-bsm-create-on-car'),
    path('car/feature/add/', views.FeatureBSModalCreateViewOnCar.as_view(), name='admin-feature-bsm-create-on-car'),
    path('car/details/<int:pk>', views.CarBSModalReadView.as_view(), name='admin-car-details-view-bsm'),
    # Fuel
    path('fuel/list/', views.admin_fuel_view, name='admin-fuels'),
    path('fuel/add/', views.FuelBSModalCreateView.as_view(), name='admin-fuel-bsm-create'),
    path('fuel/update/<int:pk>', views.FuelBSModalUpdateView.as_view(), name='admin-fuel-bsm-update'),
    path('fuel/read/<int:pk>', views.FuelBSModalReadView.as_view(), name='admin-fuel-bsm-read'),
    path('fuel/delete/<int:pk>', views.FuelBSModalDeleteView.as_view(), name='admin-fuel-bsm-delete'),
    # brand
    path('brand/list/', views.admin_brand_view, name='admin-brands'),
    path('brand/add/', views.BrandBSModalCreateView.as_view(), name='admin-brand-bsm-create'),
    path('brand/update/<int:pk>', views.BrandBSModalUpdateView.as_view(), name='admin-brand-bsm-update'),
    path('brand/read/<int:pk>', views.BrandBSModalReadView.as_view(), name='admin-brand-bsm-read'),
    path('brand/delete/<int:pk>', views.BrandBSModalDeleteView.as_view(), name='admin-brand-bsm-delete'),
    # feature
    path('feature/list/', views.admin_feature_view, name='admin-features'),
    path('feature/add/', views.FeatureBSModalCreateView.as_view(), name='admin-feature-bsm-create'),
    path('feature/update/<int:pk>', views.FeatureBSModalUpdateView.as_view(), name='admin-feature-bsm-update'),
    path('feature/read/<int:pk>', views.FeatureBSModalReadView.as_view(), name='admin-feature-bsm-read'),
    path('feature/delete/<int:pk>', views.FeatureBSModalDeleteView.as_view(), name='admin-feature-bsm-delete'),
    # blog
    path('blog/list/', views.admin_blog_view, name='admin-blog'),
    path('blog/add/', views.BlogBSModalCreateView.as_view(), name='admin-blog-bsm-create'),
    path('blog/update/<int:pk>', views.BlogBSModalUpdateView.as_view(), name='admin-blog-bsm-update'),
    path('blog/read/<int:pk>', views.BlogBSModalReadView.as_view(), name='admin-blog-bsm-read'),
    path('blog/delete/<int:pk>', views.BlogBSModalDeleteView.as_view(), name='admin-blog-bsm-delete'),
    # bookings
    path('booking/list/', views.BookingListView.as_view(), name='admin-booking-list'),
    path('booking/request/status/update/<int:b_id>/<str:status>/', views.update_booking_request_status, name='admin-update-booking-request-status'),
    path('booking/payment/status/update/<int:b_id>/<str:status>/', views.update_booking_payment_status, name='admin-update-booking-payment-status'),
    path('booking/details/<int:pk>', views.BookingBSModalReadView.as_view(), name='admin-booking-details-view-bsm'),
    path('booking/delete/<int:pk>', views.BookingBSModalDeleteView.as_view(), name='admin-booking-bsm-delete'),
    # contacts
    path('contacts/', views.admin_contact_view, name='admin-contacts'),
    path('vehicle-add-request/list/', views.VehicleAddRequestListView.as_view(), name='admin-vehicle-add-request-list'),
    path('vehicle-add-request/details/<int:pk>/', views.VehicleAddRequestBSModalReadView.as_view(), name='admin-vehicle-add-request-details-view-bsm'),
    # users
    path('users/admin/list/', views.AdminListView.as_view(), name='admin-admin-list'),
    path('users/owner/list/', views.OwnerListView.as_view(), name='admin-owner-list'),
    path('users/customer/list/', views.CustomerListView.as_view(), name='admin-customer-list'),
    path('user/profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='admin-user-profile-detail-view'),
    path('user/owner/add/', views.OwnerBSModalCreateView.as_view(), name='admin-owner-bsm-create'),

    # Payments and Accounts
    path('payments-and-accounts/payment-history/list/', views.PaymentHistoryListView.as_view(), name='admin-payment-history-list'),
    path('payments-and-accounts/transaction-history/list/', views.TransactionHistoryListView.as_view(), name='admin-transaction-history-list'),
    path('payments-and-accounts/vehicle-owner-account/list/', views.VehicleOwnerAccountListView.as_view(), name='admin-vehicle-owner-account-list'),
    path('payments-and-accounts/transaction-history/payment-status/update/<int:t_id>/', views.update_transaction_payment_status,
         name='admin-update-transaction-payment-status'),

    path('site-default/', views.admin_site_default_view, name='admin-site-default'),
    path('blank/', views.admin_blank_view, name='admin-blank'),

]