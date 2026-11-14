"""
Management command to seed the database with authentic curated Probash Mart data.
"""

from django.core.management.base import BaseCommand
from apps.products.models import Category, Product
from apps.shipping.models import ShippingZone
from apps.payments.models import PaymentMethod
from apps.pages.models import Page
from apps.banners.models import Banner


class Command(BaseCommand):
    help = 'Seed the database with authentic curated Probash Mart products'

    def handle(self, *args, **options):
        self.stdout.write('Seeding authentic Probash Mart catalog...\n')

        # Clean old junk
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Curated Categories
        categories_data = [
            {
                'name': 'খাঁটি খাদ্যপণ্য',
                'slug': 'pure-food',
                'icon': 'utensils',
                'image': 'categories/cat_pure_food_v2.jpg',
                'description': 'প্রাকৃতিক ও স্বাস্থ্যসম্মত খাঁটি দেশি খাদ্যপণ্য',
                'sort_order': 1,
            },
            {
                'name': 'বাবার পাঞ্জাবি',
                'slug': 'fathers-punjabi',
                'icon': 'shirt',
                'image': 'categories/cat_punjabi_v2.jpg',
                'description': 'বাবার জন্য আরামদায়ক সুতি ও স্পেশাল পাঞ্জাবি',
                'sort_order': 2,
            },
            {
                'name': 'শীতের পোশাক',
                'slug': 'winter-wear',
                'icon': 'snowflake',
                'image': 'categories/cat_winter_v2.jpg',
                'description': 'প্রিমিয়াম কাশ্মীরি শাল, জ্যাকেট ও শীতের কাপড়',
                'sort_order': 3,
            },
            {
                'name': 'মায়ের শাড়ি',
                'slug': 'mothers-saree',
                'icon': 'sparkles',
                'image': 'categories/cat_saree_v2.jpg',
                'description': 'মায়ের জন্য ঐতিহ্যবাহী জামদানি ও সুতি তাঁতের শাড়ি',
                'sort_order': 4,
            },
            {
                'name': 'প্রিয়জনের উপহার',
                'slug': 'gift-boxes',
                'icon': 'gift',
                'image': 'categories/cat_gift_v2.jpg',
                'description': 'স্ত্রী ও পরিবারের জন্য স্পেশাল সারপ্রাইজ গিফট কম্বো',
                'sort_order': 5,
            },
            {
                'name': 'ফ্যামিলি বাজার কম্বো',
                'slug': 'family-combo',
                'icon': 'shopping-bag',
                'image': 'categories/cat_grocery_v2.jpg',
                'description': 'পরিবারের পুরো মাসের জরুরি বাজার ও যত্ন প্যাক',
                'sort_order': 6,
            },
        ]

        cat_map = {}
        for c_data in categories_data:
            cat = Category.objects.create(
                name=c_data['name'],
                slug=c_data['slug'],
                icon=c_data['icon'],
                image=c_data['image'],
                description=c_data['description'],
                sort_order=c_data['sort_order'],
                is_active=True,
            )
            cat_map[c_data['slug']] = cat
            self.stdout.write(f"  Category: {cat.name}")

        # Curated Products with Real Images & Realistic BDT Pricing
        products_data = [
            {
                'name': 'সুন্দরবনের প্রাকৃতিক খাঁটি মধু (১ কেজি)',
                'slug': 'sundarban-pure-honey-1kg',
                'category_slug': 'pure-food',
                'price': 1200.0,
                'compare_price': 1400.0,
                'weight': '১ কেজি জার',
                'description': 'সুন্দরবনের গভীর অরণ্য থেকে সংগৃহীত শতভাগ খাঁটি ও প্রাকৃতিক খলিশা ফুলের কাঁচা মধু। কোনো প্রকার চিনি বা প্রিজারভেটিভ মুক্ত।',
                'image': 'products/prod_honey_v2.jpg',
                'is_best_seller': True,
                'is_featured': True,
                'is_flash_deal': False,
            },
            {
                'name': 'কাঠের ঘানি ভাঙা খাঁটি সরিষার তেল (৫ লিটার)',
                'slug': 'cold-pressed-mustard-oil-5l',
                'category_slug': 'pure-food',
                'price': 1450.0,
                'compare_price': 1650.0,
                'weight': '৫ লিটার ক্যান',
                'description': 'দেশি মাঘী সরিষা দিয়ে কাঠের ঘানিতে ভাঙা শতভাগ ঝাঁজালো ও সুস্বাদু খাঁটি সরিষার তেল। পরিবারের রান্নায় স্বাস্থ্যকর সুরক্ষার প্রতীক।',
                'image': 'products/prod_oil_v2.jpg',
                'is_best_seller': True,
                'is_featured': True,
                'is_flash_deal': True,
            },
            {
                'name': 'খাঁটি গাওয়া ঘি (১ কেজি)',
                'slug': 'pure-deshi-ghee-1kg',
                'category_slug': 'pure-food',
                'price': 1650.0,
                'compare_price': 1850.0,
                'weight': '১ কেজি জার',
                'description': 'পাবনার ঐতিহ্যবাহী ঘোষদের হাত দিয়ে তৈরি শতভাগ খাঁটি গাওয়া ঘি। অতুলনীয় সুবাস ও দানাদার খাঁটি টেক্সচার।',
                'image': 'products/prod_ghee_v2.jpg',
                'is_best_seller': True,
                'is_featured': True,
                'is_flash_deal': False,
            },
            {
                'name': 'বাবার আরামদায়ক সুতি এমব্রয়ডারি পাঞ্জাবি',
                'slug': 'fathers-cotton-punjabi',
                'category_slug': 'fathers-punjabi',
                'price': 1850.0,
                'compare_price': 2200.0,
                'weight': 'সাইজ: 40/42/44',
                'description': 'বাবার জন্য ১০০% পিওর সুতি ফেব্রিক, পরিশীলিত কলার এমব্রয়ডারি কাজ ও অত্যন্ত আরামদায়ক কাটিং। দেশে বাবার সেরা উপহার।',
                'image': 'products/prod_punjabi_v2.jpg',
                'is_best_seller': True,
                'is_featured': True,
                'is_flash_deal': True,
            },
            {
                'name': 'প্রিমিয়াম কাশ্মীরি পশমিনা শাল (শীতের উপহার)',
                'slug': 'kashmiri-pashmina-shawl',
                'category_slug': 'winter-wear',
                'price': 2200.0,
                'compare_price': 2600.0,
                'weight': 'স্ট্যান্ডার্ড সাইজ',
                'description': 'কাশ্মীরি সূক্ষ্ম উলের তৈরি নরম, হালকা কিন্তু অত্যন্ত উষ্ণ প্রিমিয়াম শাল। মা কিংবা বাবার শীতের জন্য নিখুঁত উপহার।',
                'image': 'products/prod_shawl_v2.jpg',
                'is_best_seller': True,
                'is_featured': True,
                'is_flash_deal': True,
            },
            {
                'name': 'মায়ের ঐতিহ্যবাহী ঢাকাই জামদানি শাড়ি',
                'slug': 'mothers-dhakai-jamdani-saree',
                'category_slug': 'mothers-saree',
                'price': 3450.0,
                'compare_price': 4000.0,
                'weight': '১২ হাত ব্লাউজ পিসসহ',
                'description': 'রূপগঞ্জের তাঁতিদের হাতে বোনা ৮৪ কাউন্টের আরামদায়ক সফট ঢাকাই জামদানি শাড়ি। মায়ের মুখের হাসি ফুটিয়ে তোলার শ্রেষ্ঠ উপহার।',
                'image': 'products/prod_saree_v2.jpg',
                'is_best_seller': True,
                'is_featured': True,
                'is_flash_deal': False,
            },
            {
                'name': 'প্রবাসী স্পেশাল উইন্টার প্যাডেড জ্যাকেট',
                'slug': 'mens-winter-padded-jacket',
                'category_slug': 'winter-wear',
                'price': 2800.0,
                'compare_price': 3200.0,
                'weight': 'সাইজ: M/L/XL/XXL',
                'description': 'উচ্চমানের উইন্ডপ্রুফ ও ওয়াটার রিপেলেন্ট আউটার এবং থার্মাল প্যাডিং সহ স্টাইলিশ শীতের জ্যাকেট। ছোট ভাই কিংবা নিজের পরিবারের জন্য সেরা।',
                'image': 'products/prod_jacket_v2.jpg',
                'is_best_seller': False,
                'is_featured': True,
                'is_flash_deal': False,
            },
            {
                'name': 'স্ত্রীর জন্য সারপ্রাইজ প্রিমিয়াম গিফট বক্স',
                'slug': 'surprise-gift-box-for-wife',
                'category_slug': 'gift-boxes',
                'price': 2650.0,
                'compare_price': 3100.0,
                'weight': 'লাক্সারি গিফট প্যাক',
                'description': 'প্রবাসী ভাইয়ের প্রিয়তমা স্ত্রীর জন্য ভালোবাসা মাখা স্পেশাল বক্স: প্রিমিয়াম চকলেট, পারফিউম, অর্গানিক স্কিন কেয়ার ও ভালোবাসার চিরকুট।',
                'image': 'products/prod_giftbox_v2.jpg',
                'is_best_seller': True,
                'is_featured': True,
                'is_flash_deal': True,
            },
            {
                'name': 'মায়ের সংসারের মাসিক বাজার ও কেয়ার প্যাক',
                'slug': 'mothers-monthly-care-grocery-pack',
                'category_slug': 'family-combo',
                'price': 4500.0,
                'compare_price': 5200.0,
                'weight': 'পুরো মাসের মেগা প্যাক',
                'description': 'মিনিকেট চাল, সয়াবিন তেল, মসুর ডাল, খাঁটি মসলা, চিনি ও চা পাতা সহ প্রবাসীদের পরিবারের পূর্ণাঙ্গ মাসিক বাজার কম্বো।',
                'image': 'products/prod_grocery_v2.jpg',
                'is_best_seller': True,
                'is_featured': True,
                'is_flash_deal': False,
            },
            {
                'name': 'প্রিমিয়াম ড্রাই ফ্রুটস ও বাদাম গিফট বক্স',
                'slug': 'premium-dry-fruits-nuts-box',
                'category_slug': 'gift-boxes',
                'price': 1950.0,
                'compare_price': 2300.0,
                'weight': '৮০০ গ্রাম লাক্সারি প্যাক',
                'description': 'আমন্ড, কাজুবাদাম, পেস্তা বাদাম, কিশমিশ ও প্রিমিয়াম ইরানি জাফরানি বাদামের পুষ্টিকর ও সুস্বাদু কম্বো।',
                'image': 'products/prod_nuts_v2.jpg',
                'is_best_seller': False,
                'is_featured': True,
                'is_flash_deal': False,
            },
            {
                'name': 'নকশিকাঁথা স্পেশাল শীতের কম্বল / লেপ',
                'slug': 'traditional-cozy-winter-quilt',
                'category_slug': 'winter-wear',
                'price': 2500.0,
                'compare_price': 2900.0,
                'weight': 'ডাবল বেড সাইজ',
                'description': 'সফট মাইক্রোফাইবার ফিলিং ও নকশিকাঁথা স্টাইলের ঐতিহ্যবাহী আরামদায়ক শীতের হালকা উষ্ণ কম্বল।',
                'image': 'products/prod_blanket_v2.jpg',
                'is_best_seller': False,
                'is_featured': True,
                'is_flash_deal': False,
            },
            {
                'name': 'ছোট ভাই-বোনের জন্য নিউ ইয়ার উইন্টার হুডি',
                'slug': 'winter-warm-fleece-hoodie',
                'category_slug': 'winter-wear',
                'price': 1350.0,
                'compare_price': 1600.0,
                'weight': 'সাইজ: S/M/L/XL',
                'description': '৩৫০ জিএসএম হেভি ফ্লিস কাপড়ের অত্যন্ত আরামদায়ক ও স্টাইলিশ ইউনিসেক্স উইন্টার হুডি।',
                'image': 'products/prod_hoodie_v2.jpg',
                'is_best_seller': False,
                'is_featured': True,
                'is_flash_deal': False,
            },
        ]

        for p_data in products_data:
            cat = cat_map.get(p_data.pop('category_slug'))
            p_data['category'] = cat
            p_data['status'] = 'active'
            p_data['stock'] = 50
            p_data['short_description'] = p_data['description'][:100]

            prod = Product.objects.create(**p_data)
            self.stdout.write(f"  Product: {prod.name} -> {prod.image}")

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

        # Payment Methods
        payment_data = [
            {'name': 'WhatsApp Order (Direct)', 'description': 'Confirm order and payment via WhatsApp.', 'sort_order': 1},
        ]
        for pm_data in payment_data:
            pm, created = PaymentMethod.objects.get_or_create(
                name=pm_data['name'], defaults=pm_data
            )

        self.stdout.write(self.style.SUCCESS('\n✅ Probash Mart database seeded successfully with authentic curated data!'))
