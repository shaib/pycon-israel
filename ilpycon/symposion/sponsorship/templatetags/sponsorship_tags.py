import random

from django import template
from django.template.defaultfilters import linebreaks, urlize

from ilpycon.symposion.conference.models import current_conference
from ilpycon.symposion.sponsorship.models import Sponsor, SponsorLevel


register = template.Library()


class SponsorsNode(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 3 and bits[1] == "as":
            return cls(bits[2])
        elif len(bits) == 4 and bits[2] == "as":
            return cls(bits[3], bits[1])
        else:
            raise template.TemplateSyntaxError("%r takes 'as var' or 'level as var'" % bits[0])

    def __init__(self, context_var, level=None):
        if level:
            self.level = template.Variable(level)
        else:
            self.level = None
        self.context_var = context_var

    def render(self, context):
        conference = current_conference()
        if self.level:
            level = self.level.resolve(context)
            queryset = Sponsor.objects.filter(
                level__conference=conference, level__name__iexact=level, active=True)\
                .order_by("added")
        else:
            queryset = Sponsor.objects.filter(level__conference=conference, active=True)\
                .order_by("level__order", "added")
        context[self.context_var] = queryset
        return u""

class RandomSponsorNode(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 3 and bits[1] == "as":
            return cls(bits[2])
        else:
            raise template.TemplateSyntaxError("%r takes 'as var'" % bits[0])

    def __init__(self, context_var):
        self.context_var = context_var

    def render(self, context):
        conference = current_conference()
        queryset = (
            Sponsor.objects.filter(level__conference=conference, active=True)
                           .order_by("level__order", "added")
                           .select_related("level")
        )
        sponsors = [sp for sp in queryset]  # if sp.annotation]
        max_level = max(sp.level.order for sp in sponsors)
        # Prepare a lottery set, where smaller order means more occurrences
        lottery = sum([(max_level+1-sp.level.order)*[sp] for sp in sponsors], [])
        context[self.context_var] = random.choice(lottery)
        return u""


class SponsorLevelNode(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 3 and bits[1] == "as":
            return cls(bits[2])
        else:
            raise template.TemplateSyntaxError("%r takes 'as var'" % bits[0])

    def __init__(self, context_var):
        self.context_var = context_var

    def render(self, context):
        conference = current_conference()
        context[self.context_var] = SponsorLevel.objects.filter(conference=conference)
        return u""


@register.tag
def sponsors(parser, token):
    """
    {% sponsors as all_sponsors %}
    or
    {% sponsors "gold" as gold_sponsors %}
    """
    return SponsorsNode.handle_token(parser, token)


@register.tag
def random_sponsor(parser, token):
    """
    {% random_sponsor as sponsor %}
    """
    return RandomSponsorNode.handle_token(parser, token)


@register.tag
def sponsor_levels(parser, token):
    """
    {% sponsor_levels as levels %}
    """
    return SponsorLevelNode.handle_token(parser, token)


class LocalizedTextNode(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 3:
            return cls(bits[2], bits[1][1:-1])
        elif len(bits) == 5 and bits[-2] == "as":
            return cls(bits[2], bits[1][1:-1], bits[4])
        else:
            raise template.TemplateSyntaxError("%r takes 'as var'" % bits[0])

    def __init__(self, sponsor, content_type, context_var=None):
        self.sponsor_var = template.Variable(sponsor)
        self.content_type = content_type
        self.content_var = context_var

    def render(self, context):
        s = ''
        try:
            sponsor = self.sponsor_var.resolve(context)
            content_type = '%s_%s' % (self.content_type, context['request'].LANGUAGE_CODE)
            texts = sponsor.sponsor_benefits.filter(benefit__content_type=content_type)
            if texts.count() > 0:
                s = linebreaks(urlize(texts[0].text, autoescape=True))
            if self.content_var:
                context[self.content_var] = s
                s = ''
        except:
            pass
        return s


@register.tag
def localized_text(parser, token):
    """
    {% localized_text "content_type" sponsor %}
    {% localized_text "content_type" sponsor as localized_text %}
    """
    return LocalizedTextNode.handle_token(parser, token)
