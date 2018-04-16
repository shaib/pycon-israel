import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import TalkProposal, TutorialProposal


HEADERS = [
    'Timestamp',
    'Email address',
    'First Name',
    'Last Name',
    'Contact Phone Number',
    'Speaker Bio',
    'Financial Assistance',
    'Session Length',
    'Session Type',
    'Session Title',
    'Session Abstract',
    'Session Language',
    'Second Choice Session Language (optional)',
    'Required Experience Level of Participants',
    'Target Audience',
    'Any Specific Props Needed for Your Session?',
    'Additional Notes',
    'By submitting this form I agree to allow PyCon Israel organizers to record my presentation during PyCon Israel, 3–6 June 2018. I understand that the organizers may share this recording and/or my slides with the conveners and other conference organizers for the benefit of the Python community. The material may also be placed onto the PyCon Israel web site, http://il.pycon.org, and other cooperating sites for public viewing. All content is shared under Creative Commons Attribution 4.0 International (CC BY 4.0) license as explained here: https://creativecommons.org/licenses/by/4.0',
]


def make_user(email, first, last):
    username = email
    counter = 0
    while User.objects.filter(username=username).exists():
        counter += 1
        username = '{email}-{counter}'.format(**locals())
    user = User.objects.create_user(username=username, email=email,
                                    first_name=first, last_name=last)
    return user


def make_speaker(user, phone, bio, financial_assistance):
    return Speaker.objects.create(
        user=user,
        phone_number=phone,
        biography=bio,
        financial_assistance=financial_assistance,
        name=user.get_full_name(),
    )


def make_proposal(speaker, duration, kind,
                  title, abstract, language, second_language,
                  audience_level, target_audiences,
                  specific_props, additional_notes,
                  recording_release, submitted):
    # Sorry, it's past 3AM

class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(args[0], newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter='\t')
            for row in reader:
                # This little exercise allows referencing in Englist
                # the rows from the Hebrew form as well
                row = dict(zip(HEADERS, row))
                with transaction.atomic():
                    email = row['Email address'].strip()
                    first = row['First Name'].strip()
                    last = row['Last Name'].strip()

                    user = make_user(email, first, last)

                    phone = row['Contact Phone Number']
                    bio = row['Speaker Bio']
                    financial_assistance = bool(row['Financial Assistance'])
                
                    speaker = make_speaker(user, phone, bio, financial_assistance)
                
                    duration = row['Session Length']
                    kind = row['Session Type']
                    title = row['Session Title']
                    abstract = row['Session Abstract']
                    language = row['Session Language']
                    language2 = row['Second Choice Session Language (optional)']
                    audience_level = row['Required Experience Level of Participants']
                    target_audiences = row['Target Audience'].split()
                    specific_props = row['Any Specific Props Needed for Your Session?']
                    additional_notes = row['Additional Notes']
                    recording_release = bool(row[HEADERS[-1]]) # Not repeating text...
                    submitted = row['Timestamp']

                    proposal = make_proposal(
                        speaker=speaker, duration=duration, kind=kind,
                        title=title, abstract=abstract,
                        language=language, second_language=language2,
                        audience_level=audience_level, target_audiences=target_audiences,
                        specific_props=specific_props, additional_notes=additional_notes,
                        recording_release=recording_release,
                        submitted=submitted,
                    )
                    
     
                                  
            
        except:
            pass

        csv_file = csv.writer(
            open(os.path.join(os.getcwd(), "build", "sponsors.csv"), "wb")
        )
        csv_file.writerow(["Name", "URL", "Level", "Description"])

        for sponsor in Sponsor.objects.all():
            path = os.path.join(os.getcwd(), "build", slugify(sponsor.name))
            try:
                os.makedirs(path)
            except:
                pass
