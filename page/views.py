import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext

from apartmentawesome.page.models import Event

def index(request):
    events = Event.objects.filter(date__gte=datetime.datetime.now()).order_by("-date")
    event = events[0]
    
    date = event.date.strftime("%d.%m.%Y")
    
    return render_to_response("events.html", locals(), context_instance=RequestContext(request))
