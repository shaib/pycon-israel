import mimetypes

from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.decorators.cache import cache_control

from .models import DBFile


@cache_control(max_age=86400)
def serve(request, name):
    connection = getattr(settings, 'DBFILES_CONNECTION', 'default')
    try:
        f = DBFile.objects.using(connection).get_for_read(name)
    except DBFile.DoesNotExist:
        raise Http404("File '{name}' not found".format(name=name))
    mimetype, encoding = mimetypes.guess_type(name)
    
    mimetype = mimetype or 'application/octet-stream'
    response = HttpResponse(content_type=mimetype)
    if encoding:
        response['Content-Encoding'] = encoding
    response.write(f.content)
    return response
