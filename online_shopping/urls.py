from django.urls import path
from . import views

urlpatterns = [
    path('signin_page/', views.signin_page, name='signin_page'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('seller_signup_page/', views.seller_signup_page, name='seller_signup_page'),
    path('logout_user/', views.logout_user, name='logout_user'),

    # ----------------------- START Admin ----------------------------
    
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('verify_sellers/', views.verify_sellers, name='verify_sellers'),
    path('seller_details/<int:id>/', views.seller_details, name='seller_details'),
    path('approve_seller/<int:id>/', views.approve_seller, name='approve_seller'),
    path('reject_seller/<int:id>/', views.reject_seller, name='reject_seller'),
    path('accepted_sellers/', views.accepted_sellers, name='accepted_sellers'),
    path('rejected_sellers/', views.rejected_sellers, name='rejected_sellers'),
    path('customers_list/', views.customers_list, name='customers_list'),
    path('customer_details/<int:id>/', views.customer_details, name='customer_details'),
    path('delete_customer/<int:id>/', views.delete_customer, name='delete_customer'),

    path('category/', views.category, name='category'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),

    path('subcategory/', views.subcategory, name='subcategory'),
    path('add_subcategory/', views.add_subcategory, name='add_subcategory'),
    path('edit_subcategory/<int:id>', views.edit_subcategory, name='edit_subcategory'),
    path('delete_subcategory/<int:id>/', views.delete_subcategory, name='delete_subcategory'),

    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path('view_feedback/', views.view_feedback, name='view_feedback'),
    path('view_inquiry/', views.view_inquiry, name='view_inquiry'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('admin_change_password/', views.admin_change_password, name='admin_change_password'),

    # ------------------------------ seller ----------------------------------

    path('seller_not_verified/', views.seller_not_verified, name='seller_not_verified'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller_profile/', views.seller_profile, name='seller_profile'),
    path('seller_change_password/', views.seller_change_password, name='seller_change_password'),
    path('seller_signup/', views.seller_signup, name='seller_signup'),
    path('seller_products_list/', views.seller_products_list, name='seller_products_list'),
    path('seller_add_products/', views.seller_add_products, name='seller_add_products'),
    path('seller_products_details/', views.seller_products_details, name='seller_products_details'),
    path('seller_orders/', views.seller_orders, name='seller_orders'),

    # ------------------------------ Customer ----------------------------------

    path('home/', views.customer_home, name='customer_home'),
    path('customer_signup/', views.customer_signup, name='customer_signup'),
    path('customer_feedback/', views.customer_feedback, name='customer_feedback'),
    path('customer_inquiry/', views.customer_inquiry, name='customer_inquiry'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('customer_change_password/', views.customer_change_password, name='customer_change_password'),
    path('customer_orders/', views.customer_orders, name='customer_orders'),
    path('customer_wishlist/', views.customer_wishlist, name='customer_wishlist'),
    path('customer_cart/', views.customer_cart, name='customer_cart'),
    
]
