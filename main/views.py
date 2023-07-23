import json
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseNotModified, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from main.models import OptionType, OptionPrice, Cake, CakeUser, CategoryCake, Order


def catalog(request):
    cakes = Cake.objects.filter(standard=True)
    return render(request, 'catalog.html', {'cakes': cakes})


def catalog_detail(request, pk):
    cakes = Cake.objects.filter(standard=True, category=pk)
    title = CategoryCake.objects.get(pk=pk)
    return render(request, 'catalog.html', {'cakes': cakes, 'title': title})


def footer_categories(request):
    
    return {'categories': CategoryCake.objects.all()}


def cabinet(request):
    
    try:
        client = CakeUser.objects.get(user=request.user)
    except CakeUser.DoesNotExist:
        # заглушка для admin
        client = CakeUser.objects.create(
            name=request.user.username,
            phone='+70000000000',
            user=request.user,
        )

    if request.method == 'POST':
        client.name = request.POST.get('NAME')
        client.phone = request.POST.get('PHONE')
        client.email = request.POST.get('EMAIL')
        client.save()

    context = {}
    context['orders'] = client.orders.all().order_by('status')
    context['js_client'] = json.dumps(
        {
            'name': client.name,
            'phone': str(client.phone),
            'email': client.email,
        }
    )

    
    return render(request, 'lk.html', context=context)


def delivery(request):
    return render(request, 'delivery.html')


def user_login(request):
    reg_parameter = request.POST.get('REG')
    if reg_parameter:
        step = request.POST.get('STEP')
        if step == 'phone':
            request.session['phone'] = reg_parameter
            return HttpResponseNotModified()
        elif step == 'code':
            phone = request.session['phone']
            base_user, base_user_created = User.objects.get_or_create(username=phone)
            if base_user_created:
                CakeUser.objects.create(name=phone, user=base_user, phone=phone)
            login(request, base_user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def user_logout(request):
    logout(request)
    return redirect('index')


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

        categories = CategoryCake.objects.prefetch_related('cakes')
        context['categories'] = [
            {
                'pk': category.pk,
                'name': category.name,
                'img': category.cakes.all().first().img.url
            } for category in categories
        ]

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


def new_order(request, cake_id=None):
    # вcе данные по торту собранному по конструктору - прилетают (все в POST)
    if not cake_id:
        # индивидуальный торт
        cake = Cake.objects.create(
            title='Индивидуальный торт',
            description=request.POST['DESCR'],
            standard=False,
            price=request.POST['PRICE']
        )
    else:
        cake = get_object_or_404(Cake, pk=cake_id)
    if request.user.is_authenticated and not cake_id:
        # на фронте сделан запрет на заказ без авторизации. Здесь на всякий случай убеждаемся
        # но вообще заказ должны иметь возможность сделать и те, кто не зарегистрирован - это здесь не реализовано пока
        order = Order.objects.create(
            client=request.user.cake_user,
            cake=cake,
            date_delivery=request.POST['DATE'],
            time_delivery=request.POST['TIME'],
            comment=request.POST['DELIVCOMMENTS'],
            address=request.POST['ADDRESS'],
            customer_name=request.POST['NAME'],
            customer_phone=request.POST['PHONE'],
            customer_email=request.POST['EMAIL']
        )
    else:
        # пока не реализован заказ торта из каталога
        return HttpResponseBadRequest('Заказ торта из каталога не доработан')
    return HttpResponseNotModified()