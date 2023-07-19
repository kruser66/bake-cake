from django.db import models
from django.core.validators import MinValueValidator

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



