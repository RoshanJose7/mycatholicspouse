from django.conf import settings
from django.shortcuts import render

def maintenance_middleware(get_response):
    def middleware(request):
        if settings.MAINTENANCE:
            return render(request, 'main/maintain.html')
        else:
            # try:
            #     if request.user.matrimonyapplication.status == 'Inactive' and timezone.now() > request.user.matrimonyapplication.subs_end:
            #         return render(request, 'main/404.html', {'message': 'Your plan has expired, you can renew your plan "})
            #     elif request.user.matrimonyapplication.status == 'Inactive':
            #         return render(request, 'main/404.html')
            #     else:
            response = get_response(request)
            return response
            # except:
            #     return render(request, 'main/404.html')
    return middleware