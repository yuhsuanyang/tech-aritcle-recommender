import csv
from first.models import News
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        print ("Loading CSV")
        path='./tnw.csv'
        csv_file=open(path,'r')
        reader = csv.DictReader(csv_file)
        for row in reader:
            obj=News()
            obj.title=row['title']
            obj.link=row['link']
            obj.save()
            #print (obj)