from django.core.management.base import BaseCommand, CommandError
from api.models import OneOff, Item
import datetime

class Command(BaseCommand):
    help = 'Removes all Quick Pads that have expired'

    def handle(self, *args, **options):
        lists = OneOff.objects.all()
        today = datetime.date.today()
        removedLists = []
        for l in lists:
            diff = today-l.date_created
            if(diff.days >= 2):
                Item.objects.filter(assigned_list=l.static_id).delete()
                removedLists.append(l.static_id)
                l.delete()
        self.stdout.write(self.style.SUCCESS('Removed Quick Pads: {}'.format(removedLists)))
