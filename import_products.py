import json
import os
import shutil
import django
import sys

sys.path.append('/Users/mehedihasanmridul/Backend/Probash-Mart-Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, Category

# Load JSON
with open('/tmp/products.json', 'r') as f:
    products_data = json.load(f)

# Ensure media directory exists
os.makedirs('/Users/mehedihasanmridul/Backend/Probash-Mart-Backend/media/products', exist_ok=True)

for p_data in products_data:
    cat_name = p_data.get('category')
    if not cat_name:
        cat_name = "Uncategorized"
        
    cat, _ = Category.objects.get_or_create(name=cat_name)

    image_path = p_data.get('image', '')
    new_image_path = ''
    if image_path:
        # Source path: /Users/mehedihasanmridul/website/Probash-Mart/public + image_path
        src = f"/Users/mehedihasanmridul/website/Probash-Mart/public{image_path}"
        if os.path.exists(src):
            filename = os.path.basename(src)
            dest = f"/Users/mehedihasanmridul/Backend/Probash-Mart-Backend/media/products/{filename}"
            shutil.copy2(src, dest)
            new_image_path = f"products/{filename}"
    
    price_val = str(p_data.get('price')).replace(',', '')
    weight_val = p_data.get('weight', '')
    
    Product.objects.update_or_create(
        name=p_data['name'],
        defaults={
            'category': cat,
            'price': price_val,
            'weight': weight_val,
            'is_best_seller': p_data.get('isBestSeller', False),
            'image': new_image_path if new_image_path else '',
            'is_featured': True
        }
    )

print(f"Imported {len(products_data)} products.")
