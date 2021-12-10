from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse, reverse_lazy
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfilerForm
from baskets.models import Basket
from authapp.models import User
from mainapp.mixin import BaseClassContextMixin, CustomDispatchMixin, UserDispatchMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, FormView, UpdateView


class login(LoginView, BaseClassContextMixin):
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    # success_url = reverse_lazy('index')
    title = 'Geekshop - Авторизация'

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#         # else:
#         #     print(form.errors)
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'Geekshop | Авторизация',
#         'form': form
#     }
#     return render(request, 'authapp/login.html', context)


class register(FormView, BaseClassContextMixin):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('authapp:login')
    title = 'Geekshop | Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались.')
            return redirect(self.success_url)
        return redirect(self.success_url)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'Вы успешно зарегистрировались')
#             return HttpResponseRedirect(reverse('authapp:login'))
#         else:
#             print(form.errors)
#     else:
#         form = UserRegisterForm()
#     context = {
#         'title': 'Geekshop | Регистрация',
#         'form': form
#     }
#     return render(request, 'authapp/register.html', context)

class profile(UpdateView,BaseClassContextMixin,UserDispatchMixin):
    model = User
    template_name = 'authapp/profile.html'
    form_class = UserProfilerForm
    success_url = reverse_lazy('authapp:profile')
    title = 'Geekshop | Профайл'

    # def get_object(self, queryset=None):
    #     return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(profile, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user = self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST,files=request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return redirect(self.success_url)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfilerForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             messages.set_level(request, messages.SUCCESS)
#             messages.success(request, 'Вы успешно сохранили профайл')
#             form.save()
#         else:
#             messages.set_level(request, messages.ERROR)
#             messages.error(request, form.errors)
#
#     context = {
#         'title': 'Geekshop | Профайл',
#         'form': UserProfilerForm(instance=request.user),
#         'baskets': Basket.objects.filter(user=request.user),
#     }
#     return render(request, 'authapp/profile.html', context)


class logout(LogoutView):
    template_name = 'mainapp/index.html'

# def logout(request):
#     auth.logout(request)
#     return render(request, 'mainapp/index.html')
