from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            '/login/',
            '/login/auth/',
            '/register/',
            '/',
        ]

    def __call__(self, request):
        path = request.path

        if not request.session.get('user_id') and path not in self.exempt_urls:
            return redirect('/login/')

        return self.get_response(request)