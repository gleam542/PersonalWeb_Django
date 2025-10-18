import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.forms import ContactForm

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

        # 嘗試寄送通知信
        try:
            send_mail(
                subject=f"{instance.name} 在個人網頁傳送訊息",
                message=f"From: {instance.email}\n\n{instance.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_TO_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            # 即使寄信失敗，也應告知使用者訊息已收到
            # 後台需要有機制監控這類錯誤
            print(f"!!! Mail sending failed: {e}")
            return JsonResponse({
                'status': 'warning',
                'message': 'Message saved, but notification email could not be sent.'
            })
        
        return JsonResponse({'status': 'success', 'message': f'Thank you, {instance.name}, your message has been sent!'})
    else:
        # 驗證失敗，回傳錯誤給前端
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)