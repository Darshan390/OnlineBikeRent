from django.urls import path
from RentBikeCarapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('bike_type_list/', views.bike_type_list, name='bike_type_list'),
    path('bike_type_detail/<int:rid>/', views.bike_type_detail, name='bike_type_detail'),
    path('bike_type_create/', views.bike_type_create, name='bike_type_create'),
    path('bike_type_update/<int:rid>/', views.bike_type_update, name='bike_type_update'),
    path('bike_type_delete/<int:rid>/', views.bike_type_delete, name='bike_type_delete'),
    path('bike_list/', views.bike_list, name='bike_list'),
    path('bike_detail/<int:rid>/', views.bike_detail, name='bike_detail'),
    path('bike_create/', views.bike_create, name='bike_create'),
    path('bike_update/<int:rid>/', views.bike_update, name='bike_update'),
    path('bike_delete/<int:rid>/', views.bike_delete, name='bike_delete'),
    path('rental_list/', views.rental_list, name='rental_list'),
    path('rental_detail/<int:rid>/', views.rental_detail, name='rental_detail'),
    path('payment_list/', views.payment_list, name='payment_list'),
    path('payment_detail/<int:rid>/', views.payment_detail, name='payment_detail'),
    path('more/',views.more, name='more'),
    path('gallery/',views.gallery, name='gallery'),
    path('rentbycategory/<str:category>/', views.rentbycategory, name='rentbycategory'),
     path('contact/', views.contact, name='contact'),
     path('Register', views.user_register),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('forgot_passward',views.forgot_passward),
    path('otp_verification',views.otp_verification),
    path('newpassword',views.newpassword),
    path('vehicledetails/<int:rid>/', views.vehicledetails, name='vehicledetails'),
    path('book-now/<int:rid>/', views.book_now, name='book_now'),
    path('upload_documents/<int:bike_id>/', views.upload_documents, name='upload_documents'),
    path('submit_pickup_time/<int:bike_id>/', views.submit_pickup_time, name='submit_pickup_time'),
    path('process_payment/<int:rental_id>/', views.process_payment, name='process_payment'),
    path('create_review/<rid>/', views.create_review, name='create_review'),
    path('mybooking/', views.mybooking, name='mybooking'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
