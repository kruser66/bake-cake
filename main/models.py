from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class CakeUser(User):
    name = models.CharField(verbose_name='Имя', max_length=255)
    phone = PhoneNumberField(
        'Номер клиента',
        blank=True,
        max_length=20,
    )
    address = models.CharField(verbose_name='Адрес', max_length=255)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.phone


class CategoryCake(models.Model):

    name = models.CharField('Наименование категории', max_length=100)

    class Meta:
        verbose_name = 'категория торта'
        verbose_name_plural = 'категории тортов'

    def __str__(self):
        return self.name


class Cake(models.Model):
    
    title = models.CharField(verbose_name='Название торта', max_length=255)
    description = models.TextField(
        verbose_name='Описание торта',
        max_length=500
    )
    standard = models.BooleanField(verbose_name='Торт стандартный?')
    category = models.ForeignKey(CategoryCake, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='Цена')


class Order(models.Model):
    client = models.ForeignKey(
        CakeUser,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
        related_name='orders'
    )
    cake = models.ForeignKey(
        Cake,
        on_delete=models.CASCADE,
        verbose_name='Торт'
    )
    date_delivery = models.DateField(
        verbose_name='Дата доставки',
    )
    time_delivery = models.TimeField(
        verbose_name='Время доставки',
    )
    comment = models.CharField(
        verbose_name='Комментарий',
        blank=True,
        default='',
        max_length=255
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        'Статус заказа',
        max_length=20,
        choices=[
            ('done', 'Выполнен'),
            ('delivery', 'В доставке')
        ]
    )
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.id - {self.client} - {self.ca}}'


class OptionType(models.Model):

    name = models.CharField('Название опции', max_length=50)
    js_name = models.CharField('Название поля для JS', max_length=10)

    class Meta:
        verbose_name = 'опция торта'
        verbose_name_plural = 'опции торта'

    def __str__(self):
        return f'{self.name} ({self.js_name})'


class OptionPrice(models.Model):

    type = models.ForeignKey(OptionType, on_delete=models.CASCADE)
    name = models.CharField('Наименование параметра', max_length=25)
    price = models.IntegerField('Цена параметра', validators=[MinValueValidator(0)])
    ordering = models.IntegerField('Порядок отображения')

    class Meta:
        verbose_name = 'цена опции'
        verbose_name_plural = 'цена опций'

    def __str__(self):
        return f'{self.name} - {self.price}'
