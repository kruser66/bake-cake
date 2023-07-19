import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.

db_costs = {
    'Levels': [0, 400, 750, 1100],
    'Forms': [0, 600, 400, 1000],
    'Toppings': [0, 0, 200, 180, 200, 300, 350, 200],
    'Berries': [0, 400, 300, 450, 500],
    'Decors': [0, 300, 400, 350, 300, 200, 280],
    'Words': 500
}


db_data = {
    'Levels': ['не выбрано', '1', '2', '3'],
    'Forms': ['не выбрано', 'Круг', 'Квадрат', 'Ромб'],
    'Toppings': ['не выбрано', 'Без', 'Белый соус', 'Карамельный', 'Кленовый', 'Черничный', 'Молочный шоколад', 'Клубничный'],
    'Berries': ['нет', 'Ежевика', 'Малина', 'Голубика', 'Клубника'],
    'Decors': [ 'нет', 'Фисташки', 'Безе', 'Фундук', 'Пекан', 'Маршмеллоу', 'Марципан']
}


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["db_costs"] = json.dumps(db_costs)
        context["db_data"] = json.dumps(db_data)
 
        return context

    def get(self, request, **kwargs):

        user, _ = User.objects.get_or_create(username='+79999999999') 
        # login(request, user)  
        
        return self.render_to_response(self.get_context_data(), **kwargs)
