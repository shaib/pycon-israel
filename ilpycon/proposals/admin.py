from django.contrib import admin

from .models import TalkProposal, TutorialProposal, TargetAudience


admin.site.register(TargetAudience)
admin.site.register(TalkProposal)
admin.site.register(TutorialProposal)
