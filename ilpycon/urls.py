from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from sitetree.sitetreeapp import (
    register_dynamic_trees, compose_dynamic_tree, register_i18n_trees
)

from .symposion.views import dashboard

WIKI_SLUG = r"(([\w-]{2,})(/[\w-]{2,})*)"

urlpatterns = i18n_patterns(
    path("", TemplateView.as_view(template_name="homepage.html"), name="home"),
)

urlpatterns += [
    path("admin/", admin.site.urls),
    path("i18n/", include('ilpycon.i18n')),
    path("account/", include("account.urls")),

    path("proposals/", include("ilpycon.symposion.proposals.urls")),
    path("sponsors/", include("ilpycon.symposion.sponsorship.urls")),
    path("boxes/", include("pinax.boxes.urls")),
    path("teams/", include("ilpycon.symposion.teams.urls")),
    path("reviews/", include("ilpycon.symposion.reviews.urls")),
    path("schedule/", include("ilpycon.symposion.schedule.urls")),
    path(r"blog/", include("pinax.blog.urls", namespace="pinax_blog")),
    path(r"ajax/images/", include("pinax.images.urls",
                                   namespace="pinax_images")),
    path("", include("pinax.pages.urls", namespace="pinax_pages"))
]

urlpatterns += i18n_patterns(
    path("speakers/", include("ilpycon.symposion.speakers.urls")),
    path("dashboard/", dashboard, name="dashboard"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

register_dynamic_trees(compose_dynamic_tree('ilpycon'), reset_cache=True)
register_i18n_trees(['main'])
