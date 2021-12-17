
from django.urls import path

from baskets.views import basket_add, basket_remove, basket_edit

app_name = 'baskets'
urlpatterns = [

    path('add/<int:id>/', basket_add,name='basket_add'),
    path('remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('edit/<int:id_basket>/<int:quantity>/', basket_edit, name='basket_edit'),

    # path('add/<int:id>/', basket_add.as_view(), name='basket_add'),
    # path('remove/<int:basket_id>/', basket_remove.as_view(), name='basket_remove'),
    # path('edit/<int:id_basket>/<int:quantity>/', basket_edit.as_view(), name='basket_edit'),

]
