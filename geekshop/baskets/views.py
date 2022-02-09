from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from mainapp.mixin import CustomDispatchMixin, UserDispatchMixin
# Create your views here.
from django.db import connection
from django.db.models import F
from baskets.models import Basket
from mainapp.models import Product

@login_required
def basket_add(request,id):
    user_select = request.user
    product = Product.objects.get(id=id)
    baskets = Basket.objects.filter(user=user_select, product=product)
    if baskets:
        basket = baskets.first()
        basket.quantity +=1
        # baskets.quantity = F('quantity')+1
        basket.save()
    else:
        Basket.objects.create(user=user_select, product=product, quantity=1)

        update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
        print(f'basket_add {update_queries} ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# @login_required
# def basket_add(request,id):
#     if request.is_ajax():
#         user_select = request.user
#         product = Product.objects.get(id=id)
#         baskets = Basket.objects.filter(user=user_select,product=product)
#         if baskets:
#             basket = baskets.first()
#             basket.quantity +=1
#             basket.save()
#         else:
#             Basket.objects.create(user=user_select,product=product,quantity=1)
#
#         products = Product.objects.all()
#         context = {'products': products}
#         result = render_to_string('mainapp/includes/card.html', context)
#         return JsonResponse({'result': result})


# class basket_add(CreateView, UserDispatchMixin):
#     model = Basket
#     template_name = 'baskets/basket.html'
#     success_url = reverse_lazy('authapp:profile')
    # fields = ['product']
    # template_name = 'mainapp/products.html'
    # success_url = reverse_lazy('authapp:profile')
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     if 'product_id' in kwargs:
    #         product_id = self.kwargs['product_id']
    #         if product_id:
    #             product = Product.objects.get(id=product_id)
    #             baskets = Basket.objects.filter(user=request.user, product=product)
    #             if not baskets.exists():
    #                 Basket.objects.create(user=request.user, product=product, quantity=1)
    #             else:
    #                 basket = baskets.first()
    #                 basket.quantity += 1
    #                 basket.save()
    #
    #     return redirect(self.success_url)


    # def get(self, request, *args, **kwargs):
    #     if request.is_ajax():
    #         user_select = request.user
    #         product = Product.objects.get(id=self.kwargs['product_id'])
    #         baskets = Basket.objects.filter(user=user_select, product=product)
    #         if not baskets.exists():
    #             Basket.objects.create(user=user_select, product=product, quantity=1)
    #         else:
    #             basket = baskets.first()
    #             basket.quantity += 1
    #             # baskets.quantity = F('quantity')+1
    #             basket.save()
    #
    #             return redirect(self.success_url)



# class basket_remove(DeleteView, UserDispatchMixin):
#     model = Basket
#     # success_url = reverse_lazy('authapp:profile')
#
#     def get(self, request, **kwargs):
#         basket_id = self.kwargs['pk']
#         Basket.objects.get(id=basket_id).delete()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request,basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_edit(request,id_basket,quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id_basket)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets':baskets}
        result = render_to_string('baskets/basket.html',context)
        test = JsonResponse({'result':result})
        return test

# class basket_edit(UserDispatchMixin):
#     model = Basket
#
#     def get(self, request, *args, **kwargs):
#         if request.is_ajax():
#             basket = Basket.objects.get(id=self.kwargs['id'])
#             if self.kwargs['quantity'] > 0:
#                 basket.quantity = self.kwargs['quantity']
#                 basket.save()
#             else:
#                 basket.delete()
#
#             baskets = Basket.objects.filter(user=request.user)
#             context = {
#                 'baskets': baskets
#             }
#             result = render_to_string('baskets/baskets.html', context)
#             return JsonResponse({'result': result})
