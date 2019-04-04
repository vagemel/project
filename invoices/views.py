from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum


from .models import User, Invoice, Debtor
from .forms import InvoiceForm, DebtorForm


def users(request):
    users = User.objects.annotate(balance=Sum(Coalesce('invoice__sum', 0)) - Sum(Coalesce('debtor__sum', 0)))
    context = {
        'users': users
    }
    return render(request, 'users.html', context)


def user_add(request):
    if request.method == 'POST':
        user_name = request.POST['name']

        if user_name:
            User.objects.create(name=user_name)
            return redirect('/users')
        else:
            context = {
                'error': 'Данное поле обязательно для заполнения'
            }
            return render(request, 'user-add.html', context)

    return render(request, 'user-add.html')


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('/users')


def invoices(request):
    invoices = Invoice.objects.all()
    context = {
        'invoices': invoices
    }

    return render(request, 'invoices.html', context)


def invoice_add(request):

    if request.method == "POST":
        invoice_form = InvoiceForm(request.POST)

        if invoice_form.is_valid():
            invoice_instance = invoice_form.save(commit=False)
            invoice_instance.save()

            return redirect('/invoices')
    else:
        invoice_form = InvoiceForm()

        return render(request, "invoice-add.html", {
            'invoice_form': invoice_form,
        })

    return render(request, 'invoice-add.html')


def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    return redirect('/invoices')


def debtor_add(request, invoice_id):

    if request.method == "POST":
        debtor_form = DebtorForm(request.POST)

        invoice = get_object_or_404(Invoice, id=invoice_id)

        if debtor_form.is_valid():
            debtor_instance = debtor_form.save(commit=False)

            debtors = Debtor.objects.filter(invoice=invoice).aggregate(sum=Sum('sum'))

            if (debtors['sum'] or 0) + debtor_instance.sum > invoice.sum:
                return render(request, "debtor-add.html", {
                    'debtor_form': debtor_form,
                    'error': 'Сумма должников превышает сумму счета'
                })

            debtor_instance.invoice = invoice
            debtor_instance.save()

            return redirect('/invoices')
    else:
        debtor_form = DebtorForm()

        return render(request, "debtor-add.html", {
            'debtor_form': debtor_form,
        })

    return render(request, 'debtor-add.html')


def debtor_delete(request, pk):
    debtor = get_object_or_404(Debtor, pk=pk)
    debtor.delete()
    return redirect('/invoices')




