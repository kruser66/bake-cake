import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from main.models import OptionType, OptionPrice

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

def fetch_options_data():

    db_costs = {}
    db_data = {}
    
    for option_type in OptionType.objects.all():        
        options = OptionPrice.objects.filter(type__js_name=option_type.js_name)
        if option_type.js_name == 'Words':
            db_costs.update({option_type.js_name: [option.price for option in options][0]})
        else:
            db_data.update({option_type.js_name: [option.name for option in options]})
            db_costs.update({option_type.js_name: [option.price for option in options]})

    return db_costs, db_data


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        db_costs, db_data = fetch_options_data()
        # для Vue.js
        context["db_costs"] = json.dumps(db_costs)
        context["db_data"] = json.dumps(db_data)
        # для Django templates
        context['prices'] = db_costs
        context['options'] = db_data

        return context

    def get(self, request, **kwargs):

        user, _ = User.objects.get_or_create(username='+79999999999') 
        # login(request, user)  
        
        return self.render_to_response(self.get_context_data(), **kwargs)
