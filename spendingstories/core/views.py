from django.utils.translation import ugettext as _
from django.shortcuts         import render_to_response, redirect
from django.template          import RequestContext


def index(request):
    context = {}
    return render_to_response('index.html', context, RequestContext(request))
