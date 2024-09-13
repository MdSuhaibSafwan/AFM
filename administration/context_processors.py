def current_pi_user(request):
    from personal_information.models import CustomUserPersonalInformation
    try:
        user = CustomUserPersonalInformation.objects.using('afm_personal_information').get(user_slug=request.user.slug)
    except:
        user = None
    return {'current_pi_user':user}

def current_user(request):
    from administration.models import CustomUser
    try:
        user = CustomUser.objects.get(slug=request.user.slug)
    except:
        user = None
    return {'current_user': user}