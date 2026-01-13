from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from ade.models import Products, Store, Order

class Command(BaseCommand):
    help = 'Setup user roles and permissions'

    def handle(self, *args, **kwargs):
        # Create Groups
        customer_group, created = Group.objects.get_or_create(name='Customer')
        seller_group, created = Group.objects.get_or_create(name='Seller')
        admin_group, created = Group.objects.get_or_create(name='Admin')

        self.stdout.write(self.style.SUCCESS('Groups ensured.'))

        # Grant is_staff to users in Admin and Seller groups
        # This allows them to login to the admin panel
        
        # 1. Update Admin Users
        admin_users = User.objects.filter(groups__name='Admin')
        count = admin_users.update(is_staff=True)
        self.stdout.write(self.style.SUCCESS(f'Updated {count} Admin users to is_staff=True'))

        # 2. Update Seller Users
        # Sellers might need admin access if they don't have a frontend dashboard. 
        # For now, we enable it.
        seller_users = User.objects.filter(groups__name='Seller')
        count = seller_users.update(is_staff=True)
        self.stdout.write(self.style.SUCCESS(f'Updated {count} Seller users to is_staff=True'))

        self.stdout.write(self.style.SUCCESS('Successfully verified roles and staff status.'))
