from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm


def home(request):
    context = {
        "title": "Домашняя страница",
        "hi_user": "Добро пожаловать",
        "sign": "Вход",
        "exit": "Выход",
        "message": "Вход только для зарегистрированных пользователей!",
    }
    return render(request, 'users/home.html', context)


def info(request):
    context = {"student": "Студент: Крылов Эдуард Васильевич",
               "job": "Дипломная работа.",
               "info": "В данном приложении загружать фотографии, обрабатывать их и ознакомиться с результатами уже "
                       "законченной обработки. Результат представляет из себя название класса обнаруженного объекта и "
                       "уверенность в полученном результате. Имеется функция редактировани своего профиля и загружать "
                       "аватар."
               }
    return render(request, 'users/info.html', context)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # перенаправит на домашнюю страницу, если пользователь попытается получить доступ
        # к странице регистрации во время входа в систему
        if request.user.is_authenticated:
            return redirect(to='/')

        # в противном случае обработайте отправку так, как это обычно происходило бы в противном случае
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Зарегистрирован пользователь: {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Представление на основе классов, расширяющее возможности встроенного представления
# входа в систему и добавляющее функцию запоминания
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # установите время истечения сеанса равным 0 секундам. Таким образом,
            # он автоматически закроет сеанс после закрытия браузера.
            self.request.session.set_expiry(0)

            # Установите сеанс как измененный, чтобы принудительно сохранять обновления данных / файлы cookie.
            self.request.session.modified = True

        # в противном случае сеанс браузера будет длиться столько же,
        # сколько время сеанса cookie "SESSION_COOKIE_AGE", определенное в settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = ("Мы отправили вам по электронной почте инструкции по установке вашего пароля, \
    Если существует учетная запись с указанным вами адресом электронной почты. Вы должны получить их в ближайшее время.\
    Если вы не получите электронное письмо, пожалуйста, убедитесь, что вы ввели адрес, на который указывали при "
                       "регистрации, и проверьте свою папку со спамом.")
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Ваш пароль был успешно изменен"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
