#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http                    import Http404
from django.shortcuts               import render_to_response
from django.template                import RequestContext, TemplateDoesNotExist
from django.views.decorators.csrf   import ensure_csrf_cookie

@ensure_csrf_cookie
def home(request):    
    # Render template without any argument
    return render_to_response('index.html', context_instance=RequestContext(request))

def partial(request, partial_name=None):    
    template_name = 'partials/' + partial_name + '.html';
    try:
        return render_to_response(template_name, context_instance=RequestContext(request))
    except TemplateDoesNotExist:
        raise Http404

def embed(request):
    return render_to_response('embed.html', context_instance=RequestContext(request))
