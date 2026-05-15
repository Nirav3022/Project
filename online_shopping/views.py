from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import *
from .models import *
from .decorators import *

# Create your views here.

# def signin_page(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             form = LoginForm(request.POST)
#             if form.is_valid():
#                 uname = request.POST['username']
#                 pwd = form.cleaned_data['password']
#                 user = authenticate(request=request, username=uname, password=pwd)
#                 if user is not None:
#                     login(request, user)
#                     messages.success(request, 'Login Successful')
#                     if request.user.is_superuser:
#                         return redirect('admin_dashboard')
#                     elif request.user.groups.all()[0].name == 'seller':
#                         if request.user.sellerprofile.verified:
#                             return redirect('seller_dashboard')
#                         else:
#                             return redirect('seller_not_verified')
#                     elif request.user.groups.all()[0].name == 'customer':
#                         return redirect('customer_home')
#                 else:
#                     messages.error(request, 'Invalid Credentials')
#         else:
#             form = LoginForm()
#         return render(request, 'signin_page.html', {'form':form})
#     else:
#         if request.user.groups.all()[0].name == 'admin':
#             return redirect('admin_dashboard')
#         elif request.user.groups.all()[0].name == 'seller':
#             if request.user.sellerprofile.verified:
#                 return redirect('seller_dashboard')
#             else:
#                 return redirect('seller_not_verified')
#         elif request.user.groups.all()[0].name == 'customer':
#             return redirect('customer_home')

def signin_page(request):
    form = LoginForm()
    return render(request, 'customer/signin_page.html', {'form':form})

def signup_page(request):
    form = CustomerSignupForm()
    return render(request, 'customer/signup_page.html', {'form':form})

def seller_signup_page(request):
    form = SellerSignupForm()
    return render(request, 'customer/seller_signup_page.html', {'form':form})

def logout_user(request):
    logout(request)
    return redirect('signin_page')


# ---------------------- Admin ----------------------
@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def verify_sellers(request):
    verify_sellers_list = User.objects.filter(groups__name='seller').filter(sellerprofile__verified=False).filter(sellerprofile__rejected=False)
    print(verify_sellers_list)
    return render(request, 'admin/verify_sellers.html', {'verify_sellers_list':verify_sellers_list})


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def seller_details(request, id):
    details = User.objects.get(pk=id)
    return render(request, 'admin/seller_details.html', {'details':details})



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def approve_seller(request, id):
    seller = User.objects.get(pk=id)
    seller_name = seller.username
    seller.sellerprofile.verified = True
    seller.sellerprofile.rejected = False
    seller.sellerprofile.save()
    messages.success(request, f'{seller_name} Verified')
    if seller.sellerprofile.verified:
        return redirect('accepted_sellers')
    elif seller.sellerprofile.rejected:
        return redirect('rejected_sellers')
    else:
        return redirect('verify_sellers')



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def reject_seller(request, id):
    seller = User.objects.get(pk=id)
    seller_name = seller.username
    seller.sellerprofile.verified = False
    seller.sellerprofile.rejected = True
    seller.sellerprofile.save()
    messages.warning(request, f'{seller_name} Rejected')
    if seller.sellerprofile.verified:
        return redirect('accepted_sellers')
    elif seller.sellerprofile.rejected:
        return redirect('rejected_sellers')
    else:
        return redirect('verify_sellers')



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def accepted_sellers(request):
    accepted_sellers_list = User.objects.filter(groups__name='seller').filter(sellerprofile__verified=True)
    return render(request, 'admin/accepted_sellers.html', {'accepted_sellers_list':accepted_sellers_list})



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def rejected_sellers(request):
    rejected_sellers_list = User.objects.filter(groups__name='seller').filter(sellerprofile__rejected=True)
    return render(request, 'admin/rejected_sellers.html', {'rejected_sellers_list':rejected_sellers_list})


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def customers_list(request):
    list_customers = User.objects.filter(groups__name='customer')
    return render(request, 'admin/customers_list.html', {'list_customers':list_customers})


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def customer_details(request, id):
    details = User.objects.get(pk=id)
    print(details)
    return render(request, 'admin/customer_details.html', {'details':details})


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def delete_customer(request, id):
    customer = User.objects.get(pk=id)
    customer.delete()
    messages.warning(request, f'{customer} Deleted')
    return redirect('customers_list')



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def category(request):
    category_list = Category.objects.all()
    return render(request, 'admin/category.html', {'category_list':category_list})


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category')
        if Category.objects.filter(category=category_name).exists():
           messages.error(request, f'{category_name} already exists')
           return redirect('add_category')
        else:
            obj = Category.objects.create(category=category_name)
            obj.save()
            messages.success(request, f'{category_name} added successfully')
            return redirect('category')
    
    return render(request, 'admin/add_category.html')



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def edit_category(request, id):
    category_val = Category.objects.get(pk=id)
    if request.method == 'POST':
       category_name = request.POST.get('category')
       category_val.category = category_name
       category_val.save()
       messages.info(request, f'{category_name} updated successfully')
       return redirect('category')
    return render(request, 'admin/edit_category.html', {'category_val':category_val})


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def delete_category(request, id):
    cat_name = Category.objects.get(pk=id)
    cat_name.delete()
    messages.warning(request, f'{cat_name} Deleted')
    return redirect('category')



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def subcategory(request):
    subcategory_list = Subcategory.objects.all()
    return render(request, 'admin/subcategory.html', {'subcategory_list':subcategory_list})


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def add_subcategory(request):
    if request.method == 'POST':
        form = AddSubcategoryForm(request.POST)
        if form.is_valid():
            cat = form.cleaned_data['category']
            subcat = form.cleaned_data['subcategory']

            if Subcategory.objects.filter(category=cat).filter(subcategory=subcat).exists():
                messages.error(request, f'{subcat} already exists')
                return redirect('add_subcategory')
            else:
                form.save()
                messages.success(request, f'{subcat} added successfully')
                return redirect('subcategory')
    else:
        form = AddSubcategoryForm()
    return render(request, 'admin/add_subcategory.html', {'form':form})



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def edit_subcategory(request, id):
    sub_cat = Subcategory.objects.get(pk=id)
    if request.method == 'POST':
        form = AddSubcategoryForm(request.POST, instance=sub_cat)
        if form.is_valid():
            form.save()
            subcat = form.cleaned_data['subcategory']
            messages.info(request, f'{subcat} updated successfully')
            return redirect('subcategory')
    else:
        form = AddSubcategoryForm(instance=sub_cat)
    return render(request, 'admin/edit_subcategory.html', {'form':form})



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])    
def delete_subcategory(request, id):
    subcat_name = Subcategory.objects.get(pk=id)
    subcat_name.delete()
    messages.warning(request, f'{subcat_name} Deleted')
    return redirect('subcategory')


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def admin_orders(request):
    return render(request, 'admin/admin_orders.html')


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def view_feedback(request):
    list_feedback = Feedback.objects.all()
    return render(request, 'admin/view_feedback.html', {'list_feedback':list_feedback})


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def view_inquiry(request):
    list_inquiry = Inquiry.objects.all()
    return render(request, 'admin/view_inquiry.html', {'list_inquiry':list_inquiry})


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def admin_profile(request):
    if request.method == 'POST':
        form1 = AdminSellerUpdateForm(request.POST, instance=request.user)
        form2 = AdminProfileForm(request.POST, request.FILES, instance=request.user.adminprofile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('admin_profile')
    else:
        form = {
            'form1':AdminSellerUpdateForm(instance=request.user),
            'form2':AdminProfileForm(instance=request.user.adminprofile)
        }
    return render(request, 'admin/admin_profile.html', form)





@login_required(login_url='signin_page')
@allowed_user(allowed_role=['admin'])
def admin_change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request=request, user=request.user)
            messages.success(request, 'Password Changed Successfully')
            return redirect('admin_profile')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'admin/admin_change_password.html', {'form':form})

# ---------------------- seller ----------------------

def seller_signup(request):
    if request.method == 'POST':
        form = SellerSignupForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            shopname = request.POST.get('shopname')
            gstno = request.POST.get('gstno')
            pswd = request.POST.get('pswd')
            cpswd = request.POST.get('cpswd')

        
            if pswd == cpswd:
                try:
                    user = User.objects.get(username=username)
                    messages.error(request, 'Username already exists')
                except User.DoesNotExist:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'Email already exists')
                    else:
                        user = User.objects.create_user(username=username, email=email, password=pswd)
                        group, created = Group.objects.get_or_create(name='seller')
                        user.groups.add(group)
                        user.save()
                        seller_obj = SellerProfile(shop_name=shopname, gst_number=gstno, user=user)
                        seller_obj.save()
                        messages.success(request, f'Account created for {user.username}')
                        return redirect('signin_page')          
            else:
                messages.error(request, 'Both password does not match')
        else:
            print(form.errors)
    else:
        form = SellerSignupForm()
    return render(request, 'seller/seller_signup.html', {'form':form})  



def seller_not_verified(request):
    if request.user.sellerprofile.verified:
        return redirect('seller_dashboard')
    else:
        return render(request, 'seller/seller_not_verified.html')


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['seller'])
def seller_profile(request):
    if request.method == 'POST':
        form1 = AdminSellerUpdateForm(request.POST, instance=request.user)
        form2 = SellerProfileForm(request.POST, request.FILES, instance=request.user.sellerprofile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('seller_profile')
    else:
        form = {
            'form1':AdminSellerUpdateForm(instance=request.user),
            'form2':SellerProfileForm(instance=request.user.sellerprofile)
        }
    return render(request, 'seller/seller_profile.html', form)



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['seller'])
def seller_change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request=request, user=request.user)
            messages.success(request, 'Password Changed Successfully')
            return redirect('seller_profile')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'seller/seller_change_password.html', {'form':form})



@login_required(login_url='signin_page')
@allowed_user(allowed_role=['seller'])
def seller_dashboard(request):
    return render(request, 'seller/seller_dashboard.html')


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['seller'])
def seller_products_list(request):
    return render(request, 'seller/seller_products_list.html')


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['seller'])
def seller_add_products(request):
    return render(request, 'seller/seller_add_products.html')


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['seller'])
def seller_products_details(request):
    return render(request, 'seller/seller_products_details.html')


@login_required(login_url='signin_page')
@allowed_user(allowed_role=['seller'])
def seller_orders(request):
    return render(request, 'seller/seller_orders.html')



# ---------------------- customer ----------------------

def customer_home(request):
    return render(request, 'customer/customer_home.html')


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['pswd']
            cpwd = form.cleaned_data['cpswd']

            if pwd == cpwd:
                try:
                    user = User.objects.get(username=uname)
                    messages.error(request, 'Username already exists')
                except User.DoesNotExist:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'Email already exists')
                    else:
                        user = User.objects.create_user(username=uname, email=email, password=pwd)
                        group, created = Group.objects.get_or_create(name='customer')
                        user.groups.add(group)
                        user.save()
                        seller_obj = CustomerProfile(user=user)
                        seller_obj.save()
                        messages.success(request, f'Account created for {user.username}')
                        return redirect('signin_page')          
            else:
                messages.error(request, 'Both password does not match')
    else:
         form = CustomerSignupForm()   
    return render(request, 'customer/customer_signup.html', {'form':form})



def customer_feedback(request):
    return render(request, 'customer/customer_feedback.html')

def customer_inquiry(request):
    return render(request, 'customer/customer_inquiry.html')

def customer_profile(request):
    return render(request, 'customer/customer_profile.html')

def customer_change_password(request):
    return render(request, 'customer/customer_change_password.html')

def customer_orders(request):
    return render(request, 'customer/customer_orders.html')

def customer_wishlist(request):
    return render(request, 'customer/customer_wishlist.html')

def customer_cart(request):
    return render(request, 'customer/customer_cart.html')


