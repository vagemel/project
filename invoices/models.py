from django.db import models


class User(models.Model):
    name = models.CharField('Имя пользователя', max_length=64)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    user = models.ForeignKey(User, verbose_name='Плательщик', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Счет', max_length=64)
    sum = models.IntegerField(verbose_name='Сумма', default=0)


class Debtor(models.Model):
    user = models.ForeignKey(User, verbose_name='Должник', on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    sum = models.IntegerField('Сумма')

