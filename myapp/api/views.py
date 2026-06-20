import json
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.forms import ContactForm

logger = logging.getLogger(__name__)

@csrf_exempt
def contact(request):
    """
    處理聯絡表單的 API view。
    支援 application/json 和 application/x-www-form-urlencoded。
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)

    try:
        # 優先處理 JSON body
        data = json.loads(request.body)
    except json.JSONDecodeError:
        # 若失敗，則退回處理 form-data
        data = request.POST

    form = ContactForm(data)

    if form.is_valid():
        # 驗證通過，先儲存到資料庫
        instance = form.save()

        # 寄送通知信
        try:
            send_mail(
                subject=f"{instance.name} 在個人網頁傳送訊息",
                message=f"From: {instance.email}\n\n{instance.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.SERVER_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            logger.error("send_mail failed: %s", e, exc_info=True)
            return JsonResponse({
                'status': 'warning',
                'message': f'Thank you, {instance.name}! Your message was saved but email notification failed: {e}'
            })

        return JsonResponse({'status': 'success', 'message': f'Thank you, {instance.name}, your message has been sent!'})
    else:
        # 驗證失敗，回傳錯誤給前端
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
