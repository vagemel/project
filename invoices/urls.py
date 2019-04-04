from django.urls import path, re_path

from .views import (
    users,
    user_add,
    user_delete,

    invoices,
    invoice_add,
    invoice_delete,

    debtor_add,
    debtor_delete
)

urlpatterns = [
    re_path(r'users/$', users),
    re_path(r'user-add/$', user_add),
    re_path(r'user-delete/(?P<pk>[0-9]+)/$', user_delete),

    re_path(r'invoices/$', invoices),
    re_path(r'invoice-add/$', invoice_add),
    re_path(r'invoice-delete/(?P<pk>[0-9]+)/$', invoice_delete),

    re_path(r'debtor-add/(?P<invoice_id>[0-9]+)$', debtor_add),
    re_path(r'debtor-delete/(?P<pk>[0-9]+)/', debtor_delete),
]
