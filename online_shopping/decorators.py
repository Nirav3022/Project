from django.shortcuts import redirect
# from django.contrib.auth.models import Group

# def admin_only(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_superuser:
#             return view_func(request, *args, **kwargs)
#         else:
#             return redirect('signin_page')        
#     return wrapper_func


def allowed_user(allowed_role=[]):
    def decorator_func(view_func):
        def inner_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_role:
                if group == 'seller':
                    if request.user.sellerprofile.verified:
                        return view_func(request, *args, **kwargs)
                    else:
                        return redirect('seller_not_verified')
                return view_func(request, *args, **kwargs)
            else:
                return redirect('signin_page')           

        return inner_func
    return decorator_func