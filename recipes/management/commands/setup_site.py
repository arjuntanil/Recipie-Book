from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Set up the default site for django-allauth'

    def handle(self, *args, **options):
        # Check if site with ID 1 exists
        try:
            site = Site.objects.get(pk=1)
            site.domain = '127.0.0.1:8000'
            site.name = 'Recipe Book'
            site.save()
            self.stdout.write(self.style.SUCCESS(f'Updated site: {site.domain}'))
        except Site.DoesNotExist:
            # Create a new site with ID 1
            site = Site.objects.create(
                pk=1,
                domain='127.0.0.1:8000',
                name='Recipe Book'
            )
            self.stdout.write(self.style.SUCCESS(f'Created site: {site.domain}'))
            
        # Check if any other sites exist with the same domain
        same_domain = Site.objects.filter(domain='127.0.0.1:8000').exclude(pk=1).count()
        if same_domain:
            self.stdout.write(self.style.WARNING(
                f'Found {same_domain} other site(s) with the same domain. This could cause issues.'
            )) 