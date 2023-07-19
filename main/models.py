from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    fullname = models.CharField(verbose_name='Имя', max_length=255)
    phone = PhoneNumberField(
        'Номер клиента',
        blank=True,
        max_length=20,
    )
    address = models.CharField(verbose_name='Адрес', max_length=255)

    class Meta:
        verbose_name = ('Клиент')
        verbose_name_plural = ('Клиенты')

    def __str__(self):
        return self.fullname


class Cake(models.Model):
    CATEGORIES = [
        ('Birthday', 'День рождение'),
        ('Teaparty', 'Чаепитие'),
        ('Wedding', 'Свадьба')
    ]
    LEVELS = [
        ('One level', '1 уровень'),
        ('Two level', '2 уровня'),
        ('Three level', '3 уровня')
    ]
    FORMS = [
        ('Square', 'Квадрат'),
        ('Circle', 'Круг'),
        ('Rectangle', 'Прямоугольник')
    ]
    TOPPINGS = [
        ('Without', 'Без топпинга'),
        ('White Sauce', 'Белый соус'),
        ('Caramel syrup', 'Карамельный сироп'),
        ('Maple syrup', 'Кленовый сироп'),
        ('Blueberry syrup', 'Черничный сироп'),
        ('Milk chocolate', 'Молочный шоколад'),
    ]
    BERRIES = [
        ('Blackberry', 'Ежевика'),
        ('Raspberry', 'Малина'),
        ('Blueberry', 'Голубика'),
        ('Strawberry', 'Клубника'),
    ]
    DECORS = [
        ('Pistachios', 'Фисташки'),
        ('Meringue', 'Безе'),
        ('Hazelnuts', 'Фундук'),
        ('Pecan', 'Пекан'),
        ('Marshmallow', 'Маршмеллоу'),
        ('Marzipan', 'Марципан'),
    ]
    title = models.CharField(verbose_name='Название торта', max_length=255)
    description = models.CharField(
        verbose_name='Описание торта',
        max_length=255
    )
    standard = models.BooleanField(verbose_name='Торт стандартный?')
    category = models.CharField(
        verbose_name='Категория',
        max_length=10,
        choices=CATEGORIES,
    )
    price = models.PositiveIntegerField(verbose_name='Цена')
    level = models.CharField(
        verbose_name='Кол-во уровней',
        max_length=10,
        choices=LEVELS,
    )
    form = models.CharField(
        verbose_name='Форма торта',
        max_length=10,
        choices=FORMS,
    )
    topping = models.CharField(
        verbose_name='Топпинг',
        max_length=10,
        choices=TOPPINGS,
    )
    berry = models.CharField(
        verbose_name='Ягоды',
        max_length=10,
        choices=BERRIES,
        blank=True,
        default='',
    )
    decor = models.CharField(
        verbose_name='Декор',
        max_length=10,
        choices=DECORS,
        blank=True,
        default='',
    )
    caption = models.CharField(
        verbose_name='Мы можем разместить на торте любую надпись,\
            например: «С днем рождения!»', max_length=255)


class Order(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Клиент'
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

    class Meta:
        verbose_name = ('Заказ')
        verbose_name_plural = ('Заказы')

    def __str__(self):
        return str(self.id)


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
