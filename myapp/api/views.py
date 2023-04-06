from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import ContactForm
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            print(request.POST)
            contact_form = ContactForm(name=name, email=email, message=message)
            contact_form.save()
            send_mail(
                name+'在個人網頁傳送訊息',message, 
            settings.DEFAULT_FROM_EMAIL,[settings.DEFAULT_TO_EMAIL],
            fail_silently=False,
            )
            return JsonResponse({'status': 'success','name': name})
        else:
            print(request.POST)
            return JsonResponse({'status': 'error', 'message': 'Please fill in all fields'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

