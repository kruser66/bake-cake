from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class CakeUser(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=255)
    phone = PhoneNumberField(
        'Телефон клиента',
        max_length=20,
    )
    email = models.EmailField(verbose_name='email', max_length=100, blank=True, null=True)
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE, related_name='cake_user')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} - телефон: {self.phone}'


class CategoryCake(models.Model):

    name = models.CharField(
        verbose_name='Наименование категории',
        max_length=100
    )

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
    category = models.ForeignKey(
        CategoryCake,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='cakes',
        null=True,
        blank=True
    )
    price = models.PositiveIntegerField(verbose_name='Цена')
    img = models.ImageField(
        verbose_name='Картинка',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Торт'
        verbose_name_plural = 'Торты'

    def __str__(self):
        return self.title
    
    def str(self):
        return f'{self.id - {self.title}}'


class Order(models.Model):
    client = models.ForeignKey(
        CakeUser,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
        related_name='orders'
    )
    customer_name = models.CharField(verbose_name='Имя получателя', max_length=255, null=True, blank=True)
    customer_phone = PhoneNumberField(
        'Телефон получателя',
        max_length=20,
    )
    customer_email = models.EmailField(verbose_name='email получателя', max_length=100, blank=True, null=True)
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
    address = models.CharField(verbose_name='Адрес доставки', max_length=255)
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
        ordering = ['status', '-date_delivery', '-time_delivery']

    def __str__(self):
        return f'{self.id} - {self.client} - {self.cake}'


class OptionType(models.Model):

    name = models.CharField(
        verbose_name='Название опции',
        max_length=50
    )
    js_name = models.CharField(
        verbose_name='Название поля для JS',
        max_length=10
    )

    class Meta:
        verbose_name = 'опция торта'
        verbose_name_plural = 'опции торта'

    def __str__(self):
        return f'{self.name} ({self.js_name})'


class OptionPrice(models.Model):

    type = models.ForeignKey(OptionType, on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name='Наименование параметра',
        max_length=25
    )
    price = models.PositiveIntegerField(verbose_name='Цена параметра')
    ordering = models.PositiveIntegerField(verbose_name='Порядок отображения')

    class Meta:
        verbose_name = 'цена опции'
        verbose_name_plural = 'цена опций'

    def __str__(self):
        return f'{self.name} - {self.price}'
