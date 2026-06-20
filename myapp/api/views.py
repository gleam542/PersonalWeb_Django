import json
import logging
import resend
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.forms import ContactForm

logger = logging.getLogger(__name__)

@csrf_exempt
def contact(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    form = ContactForm(data)

    if form.is_valid():
        instance = form.save()

        try:
            resend.api_key = settings.RESEND_API_KEY
            logger.error("RESEND_API_KEY prefix: %s", str(settings.RESEND_API_KEY)[:10] if settings.RESEND_API_KEY else 'NOT SET')
            resend.Emails.send({
                'from': settings.DEFAULT_FROM_EMAIL,
                'to': [settings.SERVER_EMAIL],
                'subject': f"{instance.name} 在個人網頁傳送訊息",
                'text': f"From: {instance.email}\n\n{instance.message}",
            })
        except Exception as e:
            logger.error("resend failed: %s", e, exc_info=True)
            return JsonResponse({
                'status': 'warning',
                'message': f'Thank you, {instance.name}! Your message was saved but email notification failed: {e}'
            })

        return JsonResponse({'status': 'success', 'message': f'Thank you, {instance.name}, your message has been sent!'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
