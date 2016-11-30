import json

from chartit import DataPool, Chart

from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Min, Max
from django.views.decorators.csrf import csrf_exempt

from .models import Sensor, Temperature, Humidity

class IndexView(generic.ListView):
    template_name = 'weather/index.html'
    context_object_name = 'sensor_list'

    def get_queryset(self):
        """
        Return all sensor names.
        """
        return Sensor.objects.all()

def temperature_detail(request, sensor_id):
    sensor = get_object_or_404(Sensor, pk=sensor_id)
    sensor_list = sensor.temperature_set.all().order_by('-timestamp')[:100]
    context = {'sensor_list': sensor_list}

    return render(request, 'weather/table.html', context)

def temperature_chart(request, sensor_id):
    sensor = get_object_or_404(Sensor, pk=sensor_id)

    # Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
            series=
                [{'options': {
                    'source': sensor.temperature_set
                              .extra({'date': 'date(timestamp)'})
                              .values('date')
                              .annotate(avg=Avg('value'))
                              .order_by('-date')[:30],},
                  'terms': [
                    'date',
                    'avg']},

                 {'options': {
                     'source': sensor.temperature_set
                               .extra({'date': 'date(timestamp)'})
                               .values('date')
                               .annotate(min=Min('value'))
                               .order_by('-date')[:30],},
                   'terms': [
                     {'date_min': 'date'},
                     'min']},

                 {'options': {
                     'source': sensor.temperature_set
                               .extra({'date': 'date(timestamp)'})
                               .values('date')
                               .annotate(max=Max('value'))
                               .order_by('-date')[:30],},
                   'terms': [
                     {'date_max': 'date'},
                     'max']}
                ])

    # Step 2: Create the Chart object
    cht = Chart(
            datasource = weatherdata,
            series_options =
                [{'options':{
                    'type': 'line',
                    'stacking': False},
                  'terms':{
                    'date': ['avg'],
                    'date_min': ['min'],
                    'date_max': ['max']
                }}],
            chart_options =
                {'title': {
                    'text': 'Weather Data'},
                 'xAxis': {
                    'title': {
                        'text': 'Date'}}})

    context = {'weatherchart': cht}
    # Step 3: Send the chart object to the template.
    return render(request, 'weather/chart.html', context)

def humidity_detail(request, sensor_id):
    sensor = get_object_or_404(Sensor, pk=sensor_id)
    sensor_list = sensor.humidity_set.all().order_by('-timestamp')
    context = {'sensor_list': sensor_list}

    return render(request, 'weather/table.html', context)

def humidity_chart(request, sensor_id):
    sensor = get_object_or_404(Sensor, pk=sensor_id)

    # Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
            series=
                [{'options': {
                    'source': sensor.humidity_set
                              .extra({'date': 'date(timestamp)'})
                              .values('date')
                              .annotate(avg=Avg('value'))
                              .order_by('-date')[:30],},
                  'terms': [
                    'date',
                    'avg']},

                 {'options': {
                     'source': sensor.humidity_set
                               .extra({'date': 'date(timestamp)'})
                               .values('date')
                               .annotate(min=Min('value'))
                               .order_by('-date')[:30],},
                   'terms': [
                     {'date_min': 'date'},
                     'min']},

                 {'options': {
                     'source': sensor.humidity_set
                               .extra({'date': 'date(timestamp)'})
                               .values('date')
                               .annotate(max=Max('value'))
                               .order_by('-date')[:30],},
                   'terms': [
                     {'date_max': 'date'},
                     'max']}
                ])

    # Step 2: Create the Chart object
    cht = Chart(
            datasource = weatherdata,
            series_options =
                [{'options':{
                    'type': 'line',
                    'stacking': False},
                  'terms':{
                    'date': ['avg'],
                    'date_min': ['min'],
                    'date_max': ['max']
                }}],
            chart_options =
                {'title': {
                    'text': 'Weather Data'},
                 'xAxis': {
                    'title': {
                        'text': 'Date'}}})

    context = {'weatherchart': cht}
    # Step 3: Send the chart object to the template.
    return render(request, 'weather/chart.html', context)

@csrf_exempt
def push(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if data['sensor']:
            sensor, created = Sensor.objects.get_or_create(name=data['sensor'])

            if data['temperature']:
                entity = Temperature(sensor=sensor, value=data['temperature'])
                entity.save()

            if data['humidity']:
                entity = Humidity(sensor=sensor, value=data['humidity'])
                entity.save()

        else: return HttpResponse('Invalid information.')

        return HttpResponse('OK')

    else:
        return HttpResponse("You sent 'GET' request.")
