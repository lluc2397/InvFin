

def keep_email(request):
    email = ''
    if request.user.is_anonymous:
        try:
            email = request.session['F-E']
        except:
            email = email
            
    return ({'anon_email':email})