from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ilpycon.symposion.proposals.models import ProposalBase


class TargetAudience(models.Model):

    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = _('Target Audience')
        verbose_name_plural = _('Target Audiences')

    def __str__(self):
        return self.name


class Proposal(ProposalBase):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]

    DURATION_CHOICES = (
        (timedelta(minutes=25), _('Standard 25 minutes talk.')),
        (timedelta(minutes=40), _('Long 40 minutes talk.')),
        (timedelta(hours=3.5), _('Half day workshop/sprint (3.5 hours net).')),
        (timedelta(hours=7), _('Full day workshop/sprint (7 hours net).')),
    )

    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    duration = models.DurationField(choices=DURATION_CHOICES,
                                    default=DURATION_CHOICES[0][0],
                                    verbose_name=_('Session Duration'))

    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                default=settings.LANGUAGES[0][0],
                                verbose_name=_('Proposal Language'))
    second_language = models.CharField(
        max_length=5, choices=settings.LANGUAGES, blank=True,
        verbose_name=_('Propsal Lanugauge - 2nd choice'))
    recording_release = models.BooleanField(
        default=True,
        help_text=_("By submitting your proposal, you agree to give permission "
                    "to the conference organizers to record, edit, and release "
                    "audio and/or video of your presentation. If you do not "
                    "agree to this, please uncheck this box."))

    target_audience = models.ManyToManyField(TargetAudience,
                                             related_name='%(class)ss',
                                             verbose_name=_('Target Audience'))
    target_audience_other = models.CharField(
        max_length=200, blank=True, verbose_name=_('Other target audience'))

    specific_props = models.CharField(
        max_length=200, blank=True, verbose_name=_('Specific Props'),
        help_text=_('Any Specific Props Needed?'))

    class Meta:
        abstract = True


class TalkProposal(Proposal):
    class Meta:
        verbose_name = "talk proposal"


class TutorialProposal(Proposal):
    class Meta:
        verbose_name = "tutorial proposal"
