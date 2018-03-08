"""
A refinement of Django's default set_language view

If the URL contains a language prefix, and it does not
fit the chosen language, change that.
"""
import re
from urllib.parse import unquote, urlparse

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path  #, translate_url
from django.utils.http import is_safe_url
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, check_for_language, get_language,
)
from django.views.i18n import LANGUAGE_QUERY_PARAMETER


def translate_url(url, lang_code):
    # Inaccurate and dirty but will work for now
    for code,_ in settings.LANGUAGES:
        prefix = '/{code}/'.format(locals())
        if prefix in url:
            return url.replace(prefix, '/{lang_code}/'.format(locals()))
    # No language prefix found
    return url


def site_host(request):
    # this is required for proxied sites
    site = get_current_site(request)
    # site.domain can include a path prefix
    return site.domain.split('/')[0]


def set_language(request):
    """
    Redirect to a given URL while setting the chosen language in the session or
    cookie. The URL and the language code need to be specified in the request
    parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    # Support correct allowed_hosts under dev env and under proxy
    good_hosts = {request.get_host(), site_host(request)}
    next = request.POST.get('next', request.GET.get('next'))
    if ((next or not request.is_ajax()) and
            not is_safe_url(url=next, allowed_hosts=good_hosts, require_https=request.is_secure())):
        next = request.META.get('HTTP_REFERER')
        if next:
            next = unquote(next)  # HTTP_REFERER may be encoded.
            if settings.DEBUG:
                # Maybe it's just the node dev front-end not being detected
                referrer_host = urlparse(next)[1]
                if referrer_host in('127.0.0.1:3000', 'localhost:3000'):
                    good_hosts.add(referrer_host)
                # End special addition for node dev front-end
        if not is_safe_url(url=next, allowed_hosts=good_hosts, require_https=request.is_secure()):
            next = '/'
    response = HttpResponseRedirect(next) if next else HttpResponse(status=204)
    if request.method == 'POST':
        lang_code = request.POST.get(LANGUAGE_QUERY_PARAMETER)
        if lang_code and check_for_language(lang_code):
            if next:
                next_trans = translate_url(next, lang_code)
                if next_trans != next:
                    response = HttpResponseRedirect(next_trans)
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response.set_cookie(
                    settings.LANGUAGE_COOKIE_NAME, lang_code,
                    max_age=settings.LANGUAGE_COOKIE_AGE,
                    path=settings.LANGUAGE_COOKIE_PATH,
                    domain=settings.LANGUAGE_COOKIE_DOMAIN,
                )
    return response


urlpatterns = [
    path('setlang/', set_language, name='set_language'),
]

