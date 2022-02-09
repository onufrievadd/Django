from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse, reverse_lazy
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfilerForm, UserProfileEditForm
from baskets.models import Basket
from authapp.models import User
from mainapp.mixin import BaseClassContextMixin, CustomDispatchMixin, UserDispatchMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, FormView, UpdateView
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


class login(LoginView, BaseClassContextMixin):
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    # success_url = reverse_lazy('index')
    title = 'Geekshop - Авторизация'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('authapp:login'))

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

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Вы успешно зарегистрировались.')
    #         return redirect(self.success_url)
    #     return redirect(self.success_url)
    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Вы успешно зарегистрировались!')
                return HttpResponseRedirect(reverse('authapp:login'))
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})


    def send_verify_link(self,user):
        verify_link = reverse('authapp:verify',args=[user.email,user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username}  на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject,message,settings.EMAIL_HOST_USER,[user.email],fail_silently=False)


    def verify(self,email,activate_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self,user)
            return render(self,'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))


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
    template_name = 'authapp/profile.html'
    form_class = UserProfilerForm
    success_url = reverse_lazy('authapp:profile')
    title = 'Geekshop | Профайл'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    def form_valid(self, form):
        messages.set_level(self.request,messages.SUCCESS)
        messages.success(self.request, "Вы успешно зарегистрировались")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    # @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = UserProfilerForm(data=request.POST,files=request.FILES,instance=request.user)
        profile_form = UserProfileEditForm(request.POST,instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(profile, self).get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(profile, self).get_context_data(**kwargs)
    #     context['baskets'] = Basket.objects.filter(user = self.request.user)
    #     return context

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
