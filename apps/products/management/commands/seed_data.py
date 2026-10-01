"""
Management command to seed the database with initial data from the website.
Creates categories, products, shipping zones, payment methods, and pages.
"""

from django.core.management.base import BaseCommand
from apps.products.models import Category, Product
from apps.shipping.models import ShippingZone
from apps.payments.models import PaymentMethod
from apps.pages.models import Page
from apps.banners.models import Banner


class Command(BaseCommand):
    help = 'Seed the database with initial Probash Mart data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...\n')

        # Categories
        categories_data = [
            {'name': 'Fresh Vegetables', 'icon': 'Leaf', 'sort_order': 1},
            {'name': 'Frozen Fish', 'icon': 'Fish', 'sort_order': 2},
            {'name': 'Meat & Poultry', 'icon': 'Drumstick', 'sort_order': 3},
            {'name': 'Rice & Grains', 'icon': 'Wheat', 'sort_order': 4},
            {'name': 'Spices & Masala', 'icon': 'Flame', 'sort_order': 5},
            {'name': 'Snacks & Biscuits', 'icon': 'Cookie', 'sort_order': 6},
            {'name': 'Beverages', 'icon': 'CupSoda', 'sort_order': 7},
            {'name': 'Household', 'icon': 'Home', 'sort_order': 8},
            {'name': 'Personal Care', 'icon': 'Smile', 'sort_order': 9},
            {'name': 'Sweets & Desserts', 'icon': 'Cake', 'sort_order': 10},
            {'name': 'Other', 'icon': 'MoreHorizontal', 'sort_order': 11},
        ]

        cat_map = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            cat_map[cat_data['name']] = cat
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  Category: {cat.name} [{status}]')

        # Products (sample from website mockData)
        products_data = [
            {'name': 'Hilsa Fish (Frozen)', 'price': 12.99, 'weight': '(৳/কেজি)', 'category': 'Frozen Fish', 'is_best_seller': True, 'stock': 50},
            {'name': 'Teer Aatar Rice', 'price': 14.99, 'weight': '(5kg)', 'category': 'Rice & Grains', 'stock': 100},
            {'name': 'Fortune Soybean Oil', 'price': 3.99, 'weight': '(1L)', 'category': 'Household', 'stock': 200},
            {'name': 'Teer Tea', 'price': 2.99, 'weight': '(200g)', 'category': 'Beverages', 'stock': 150},
            {'name': 'Britannia Marie Gold', 'price': 1.99, 'weight': '(250g)', 'category': 'Snacks & Biscuits', 'stock': 300},
            {'name': 'PRAN Garam Masala', 'price': 2.49, 'weight': '(100g)', 'category': 'Spices & Masala', 'stock': 200},
            {'name': 'PRAN Potato Crackers', 'price': 1.20, 'weight': '(50g)', 'category': 'Snacks & Biscuits', 'stock': 500},
            {'name': 'PRAN Chanachur', 'price': 1.50, 'weight': '(150g)', 'category': 'Snacks & Biscuits', 'stock': 400},
            {'name': 'Kalo Jam', 'price': 6.50, 'weight': '(500g)', 'category': 'Sweets & Desserts', 'stock': 60},
            {'name': 'Golap Jamun', 'price': 6.50, 'weight': '(500g)', 'category': 'Sweets & Desserts', 'stock': 60},
            {'name': 'Roshmalai', 'price': 8.50, 'weight': '(500g)', 'category': 'Sweets & Desserts', 'stock': 40},
            {'name': 'Pui Shak', 'price': 1.50, 'weight': '(1 Bunch)', 'category': 'Fresh Vegetables', 'stock': 80},
            {'name': 'Lal Shak', 'price': 1.50, 'weight': '(1 Bunch)', 'category': 'Fresh Vegetables', 'stock': 80},
            {'name': 'Bottle Gourd (Lau)', 'price': 3.50, 'weight': '(1 pc)', 'category': 'Fresh Vegetables', 'stock': 50},
            {'name': 'Radhuni Chilli Powder', 'price': 2.99, 'weight': '(200 gm)', 'category': 'Spices & Masala', 'stock': 300},
            {'name': 'Radhuni Turmeric Powder', 'price': 2.49, 'weight': '(200 gm)', 'category': 'Spices & Masala', 'stock': 300},
            {'name': 'Radhuni Coriander Powder', 'price': 2.29, 'weight': '(200 gm)', 'category': 'Spices & Masala', 'stock': 300},
            {'name': 'Radhuni Biryani Masala', 'price': 1.30, 'weight': '(40 gm)', 'category': 'Spices & Masala', 'stock': 500},
            {'name': 'Rohu (G)', 'price': 12.99, 'weight': '(2kg up)', 'category': 'Frozen Fish', 'stock': 30},
            {'name': 'Katla (G)', 'price': 12.99, 'weight': '(4kg up)', 'category': 'Frozen Fish', 'stock': 25},
            {'name': 'Hilsa (W)', 'price': 12.99, 'weight': '(1000-1200g)', 'category': 'Frozen Fish', 'stock': 20},
            {'name': 'Ruchi Chanachur - Bar-B-Q', 'price': 3.49, 'weight': '(140 gm)', 'category': 'Snacks & Biscuits', 'stock': 200},
            {'name': 'Ruchi Chanachur - Hot', 'price': 3.49, 'weight': '(140 gm)', 'category': 'Snacks & Biscuits', 'stock': 200},
            {'name': 'Radhuni Firni Mix', 'price': 3.49, 'weight': '(150 gm)', 'category': 'Sweets & Desserts', 'stock': 150},
        ]

        for p_data in products_data:
            category = cat_map.get(p_data.pop('category'))
            p_data['category'] = category
            p_data['status'] = 'active'
            p_data['is_featured'] = True

            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                weight=p_data.get('weight', ''),
                defaults=p_data
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  Product: {product.name} [{status}]')

        # Shipping Zones
        shipping_data = [
            {'name': 'Inside Dhaka', 'estimated_time': '2-3 Days', 'fee': 60},
            {'name': 'Outside Dhaka', 'estimated_time': '3-5 Days', 'fee': 120},
            {'name': 'Express Delivery (Dhaka City)', 'estimated_time': 'Same Day', 'fee': 150},
        ]
        for s_data in shipping_data:
            zone, created = ShippingZone.objects.get_or_create(
                name=s_data['name'], defaults=s_data
            )
            self.stdout.write(f'  Shipping Zone: {zone.name} [{"Created" if created else "Exists"}]')

        # Payment Methods
        payment_data = [
            {'name': 'Cash on Delivery (COD)', 'description': 'Pay in cash upon delivery.', 'sort_order': 1},
            {'name': 'bKash', 'description': 'Automated bKash merchant payments.', 'sort_order': 2},
            {'name': 'Nagad', 'description': 'Nagad mobile payments.', 'sort_order': 3},
            {'name': 'Credit/Debit Card', 'description': 'Credit and debit card processing.', 'sort_order': 4},
            {'name': 'iDEAL', 'description': 'iDEAL bank transfer.', 'sort_order': 5},
        ]
        for pm_data in payment_data:
            pm, created = PaymentMethod.objects.get_or_create(
                name=pm_data['name'], defaults=pm_data
            )
            self.stdout.write(f'  Payment Method: {pm.name} [{"Created" if created else "Exists"}]')

        # Static Pages
        pages_data = [
            {'title': 'About Us', 'content': 'Probash Mart - Your trusted Bangladeshi grocery store.', 'status': 'published'},
            {'title': 'Privacy Policy', 'content': 'Your privacy is important to us.', 'status': 'published'},
            {'title': 'Terms & Conditions', 'content': 'Terms and conditions of using Probash Mart.', 'status': 'published'},
            {'title': 'Return Policy', 'content': 'Our return and refund policy.', 'status': 'published'},
            {'title': 'Shipping Information', 'content': 'Shipping and delivery information.', 'status': 'published'},
            {'title': 'FAQ', 'content': 'Frequently asked questions.', 'status': 'published'},
        ]
        for page_data in pages_data:
            page, created = Page.objects.get_or_create(
                title=page_data['title'], defaults=page_data
            )
            self.stdout.write(f'  Page: {page.title} [{"Created" if created else "Exists"}]')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
