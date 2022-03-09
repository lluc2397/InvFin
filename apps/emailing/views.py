from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import base64
from django.utils import timezone
from django.http.response import HttpResponseRedirect, HttpResponse

def email_opened_view(request, uidb64):
    
    pixel_gif = base64.b64decode(b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=')
    
    if request.method == 'GET':
        id_title = force_text(urlsafe_base64_decode(uidb64))
        id = id_title.split("-")[0]
        title = id_title.split("-")[1]
        # if Newsletter.objects.filter(title = title).exists():
        #     newsletter = Newsletter.objects.get(title = title)
        #     NEWSLETTER_ACCURACY.objects.filter(email_related=newsletter, id = id).update(opened = True, date_opened=timezone.now())
           
        # else:
        #     EMAILS_ACCURACY.objects.filter(id = id).update(opened = True, date_opened=timezone.now())
            
        return HttpResponse(pixel_gif, content_type='image/gif')


# from django.core.mail import send_mail
# send_mail('subject', 'message', 'Dont Reply <do_not_reply@domain.com>', ['youremail@example.com'])