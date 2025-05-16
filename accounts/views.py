from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from .models import User, Teacher


# Create your views here.
def login_view(request):
    if 'user_id' in request.session:
        return redirect('/dashboard/')
    return render(request, 'accounts/login.html')


def login_auth_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        raw_password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(raw_password, user.password):
                request.session['user_id'] = user.username
                teacher = Teacher.objects.get(user=user)
                request.session['name'] = teacher.name
                request.session['ma'] = teacher.ma
                return JsonResponse({"success": True, "message": "Login bem-sucedido."})
            else:
                return JsonResponse({"success": False, "message": "Senha incorreta."}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "Usuário não encontrado."}, status=403)

    return JsonResponse({"success": False, "message": "Método não permitido."}, status=405)


def logout_view(request):
    request.session.flush()
    return redirect('/')


def register_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        matricula = request.POST.get('matricula')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message": "Usuário já existe."}, status=400)

        try:
            teacher = Teacher.objects.get(ma=matricula)
        except Teacher.DoesNotExist:
            teacher = Teacher(ma=matricula, name=name, course_id=1)
            teacher.save()

        if User.objects.filter(teacher=teacher).exists():
            return JsonResponse({"success": False, "message": "Esse professor já tem um usuário."}, status=400)

        hashed_password = make_password(raw_password)
        user = User(username=username, password=hashed_password, teacher=teacher)
        user.save()

        request.session['user_id'] = user.username
        request.session['name'] = name
        request.session['ma'] = matricula
        return JsonResponse({"success": True, "message": "Usuário registrado com sucesso."})

    return JsonResponse({"success": False, "message": "Método não permitido."}, status=405)
