#!/usr/bin/env python
"""
Test script to verify color functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
django.setup()

from store.models import Product, ProductColor, ProductImage

def test_color_functionality():
    print("🔍 Testing Color Functionality...")
    
    # Test 1: Check if products exist
    products = Product.objects.all()
    print(f"✅ Found {products.count()} products")
    
    # Test 2: Check products with colors
    products_with_colors = Product.objects.filter(colors__isnull=False).distinct()
    print(f"✅ Found {products_with_colors.count()} products with colors")
    
    # Test 3: Check individual product colors
    for product in products_with_colors[:3]:  # Test first 3 products
        colors = product.colors.all()
        print(f"📱 {product.name}: {colors.count()} colors")
        
        for color in colors:
            images = color.images.all()
            print(f"   🎨 {color.name} (Stock: {color.stock}): {images.count()} images")
            
            # Check if color has hex code
            if color.hex_code:
                print(f"      Hex: {color.hex_code}")
    
    # Test 4: Check features and specs format
    products_with_features = Product.objects.filter(features__isnull=False).exclude(features={})
    print(f"✅ Found {products_with_features.count()} products with features")
    
    for product in products_with_features[:2]:
        print(f"📋 {product.name} features format:")
        if isinstance(product.features, dict):
            if 'device' in product.features:
                print(f"   Device: {product.features['device']}")
            if 'features' in product.features:
                print(f"   Features count: {len(product.features['features'])}")
    
    # Test 5: Check specs format
    products_with_specs = Product.objects.filter(specs__isnull=False).exclude(specs={})
    print(f"✅ Found {products_with_specs.count()} products with specs")
    
    for product in products_with_specs[:2]:
        print(f"📊 {product.name} specs format:")
        if isinstance(product.specs, dict):
            if 'device' in product.specs:
                print(f"   Device: {product.specs['device']}")
            if 'specifications' in product.specs:
                specs = product.specs['specifications']
                print(f"   Specification categories: {list(specs.keys())}")
    
    print("\n🎉 Color functionality test completed!")
    print("\nTo test the web interface:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://localhost:8000/store/")
    print("3. Click on a product with colors")
    print("4. Test the color selector and image updates")

if __name__ == "__main__":
    test_color_functionality()