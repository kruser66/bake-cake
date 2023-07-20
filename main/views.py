import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseNotModified
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from main.models import OptionType, OptionPrice, Cake,CakeUser


def catalog(request):
    cakes = Cake.objects.filter(standard=True)
    return render(request, 'catalog.html', {'cakes': cakes})


def cabinet(request):
    return render(request, 'lk.html')


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
        reg_parameter = request.GET.get('REG')
        if reg_parameter:
            step = request.GET.get('STEP')
            if step == 'phone':
                request.session['phone'] = reg_parameter
                return HttpResponseNotModified()
            elif step == 'code':
                phone = request.session['phone']
                base_user, base_user_created = User.objects.get_or_create(username=phone)
                if base_user_created:
                    user, _ = CakeUser.objects.get_or_create(name=phone, defaults={'user': base_user, 'phone': phone})
                login(request, base_user)
        # раскомментируйте логаут чтобы выйти из системы (заглушка до реализации логаута)
        # logout(request)
        return self.render_to_response(self.get_context_data(), **kwargs)
