from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, TemplateView
from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryUpdateFormAdmin, ProductsForm
from authapp.models import User
from mainapp.mixin import BaseClassContextMixin, CustomDispatchMixin
from mainapp.models import Product, ProductCategory

# @user_passes_test(lambda u: u.is_superuser)
# def index(request):
#     return render(request, 'admins/admin.html')
#
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
#     context = {
#         'users': User.objects.all()
#     }
#     return render(request,'admins/admin-users-read.html',context)
#
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST,files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminRegisterForm()
#     context = {
#         'title': 'Geekshop - Админ | Регистрация',
#         'form':form
#     }
#     return render(request,'admins/admin-users-create.html',context)
#
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request,pk):
#
#     user_select = User.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST,instance=user_select,files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=user_select)
#     context = {
#         'title': 'Geekshop - Админ | Обновление',
#         'form':form,
#         'user_select':user_select
#     }
#     return render(request, 'admins/admin-users-update-delete.html',context)
#
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_delete(request,pk):
#     if request.method == 'POST':
#         user = User.objects.get(pk=pk)
#         user.is_active=False
#         user.save()
#
#     return HttpResponseRedirect(reverse('admins:admin_users'))

class IndexTemplateView(TemplateView):
    template_name = 'admins/admin.html'

#Users
class UserListView(ListView,BaseClassContextMixin,CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    title = 'Админка | Пользователи'

class UserCreateView(CreateView,BaseClassContextMixin,CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Создать пользователя'

class UserUpdateView(UpdateView,BaseClassContextMixin,CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Обновить пользователя'

class UserDeleteView(DeleteView,BaseClassContextMixin,CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Удалить пользователя'

    def delete(self, request, *args, **kwargs):
        self.object =self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# Category
class CategoryListView(ListView,BaseClassContextMixin,CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    title = 'Админка | Список категорий'

class CategoryDeleteView(DeleteView,BaseClassContextMixin,CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if  self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class CategoryUpdateView(UpdateView,BaseClassContextMixin,CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    form_class = CategoryUpdateFormAdmin
    title = 'Админка | Обновления категории'
    success_url = reverse_lazy('admins:admin_category')

class CategoryCreateView(CreateView,BaseClassContextMixin,CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-create.html'
    success_url = reverse_lazy('admins:admin_category')
    form_class = CategoryUpdateFormAdmin
    title = 'Админка | Создание категории'

# # Product
# class ProductListView(ListView,BaseClassContextMixin,CustomDispatchMixin):
#     model = Product
#     template_name = 'admins/admin-product-read.html'
#     title = 'Админка | Обновления категории'
#
#     # def get_queryset(self):
#     #     return Product.objects.all().select_related()
#
#
# class ProductCreateView(CreateView,BaseClassContextMixin, CustomDispatchMixin):
#     model = Product
#     template_name = 'admins/admin-product-create.html'
#     form_class = ProductAdminRegisterForm
#     success_url = reverse_lazy('admins:admin_product')
#     title = 'Админка | Создание товара'
#
#     # def get_context_data(self, *, object_list=None, **kwargs):
#     #     context = super(ProductCreateView, self).get_context_data(**kwargs)
#     #     context['title'] = 'Админка | Создание товара'
#     #     return context
#
#
# class ProductUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
#     model = Product
#     template_name = 'admins/admin-product-update-delete.html'
#     form_class = ProductAdminRegisterForm
#     success_url = reverse_lazy('admins:admin_product')
#     title = 'Админка | Обновление информации о товаре'
#
#     # def get_context_data(self, *, object_list=None, **kwargs):
#     #     context = super(ProductUpdateView, self).get_context_data(**kwargs)
#     #     context['title'] = 'Админка | Обновление информации о товаре'
#     #     return context
#
#
# class ProductDeleteView(DeleteView, BaseClassContextMixin, CustomDispatchMixin):
#     model = Product
#     template_name = 'admins/admin-product-read.html'
#     success_url = reverse_lazy('admins:admin_product')
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         if self.object.is_active:
#             self.object.is_active = False
#         else:
#             self.object.is_active = True
#         self.object.save()
#         return HttpResponseRedirect(self.get_success_url())

# Product
class ProductListView(ListView,BaseClassContextMixin,CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-read.html'
    title = 'Админка | Обновления категории'

class ProductsUpdateView(UpdateView, BaseClassContextMixin,CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    form_class = ProductsForm
    title = 'Админка | Обновление продукта'
    success_url = reverse_lazy('admins:admins_product')

class ProductsCreateView(CreateView, BaseClassContextMixin,CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-create.html'
    form_class = ProductsForm
    title = 'Админка | Создание продукта'
    success_url = reverse_lazy('admins:admins_product')

class ProductsDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-read.html'
    success_url = reverse_lazy('admins:admins_product')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False if self.object.is_active else True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())