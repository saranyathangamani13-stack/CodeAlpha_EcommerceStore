from django.db import migrations


PRODUCTS = [
    {
        'name': 'Ripple ceramic lamp', 'slug': 'ripple-ceramic-lamp', 'category': 'Home',
        'description': 'A softly sculpted ceramic base and warm linen shade bring an easy glow to bedside tables and quiet corners.',
        'price': '84.00', 'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1000&q=85', 'stock': 12,
    },
    {
        'name': 'Daily pour-over set', 'slug': 'daily-pour-over-set', 'category': 'Home',
        'description': 'A considered little ritual: a handmade stoneware dripper with a matching cup, made for slow mornings.',
        'price': '48.00', 'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1000&q=85', 'stock': 18,
    },
    {
        'name': 'Form desk tray', 'slug': 'form-desk-tray', 'category': 'Desk',
        'description': 'Keep the small things in their place with this solid oak catchall, finished by hand with natural oil.',
        'price': '36.00', 'image_url': 'https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?auto=format&fit=crop&w=1000&q=85', 'stock': 9,
    },
    {
        'name': 'Field notes tote', 'slug': 'field-notes-tote', 'category': 'Travel',
        'description': 'A generously sized everyday carryall in sturdy cotton canvas, with an inside pocket for the essentials.',
        'price': '42.00', 'image_url': 'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=1000&q=85', 'stock': 15,
    },
    {
        'name': 'Tide glass carafe', 'slug': 'tide-glass-carafe', 'category': 'Home',
        'description': 'A hand-blown glass carafe with a satisfying weight and a clean silhouette for the table or nightstand.',
        'price': '54.00', 'image_url': 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?auto=format&fit=crop&w=1000&q=85', 'stock': 7,
    },
    {
        'name': 'Everyday wool cap', 'slug': 'everyday-wool-cap', 'category': 'Wear',
        'description': 'A soft, lightweight wool cap with a relaxed shape, knitted in a versatile deep moss shade.',
        'price': '38.00', 'image_url': 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?auto=format&fit=crop&w=1000&q=85', 'stock': 11,
    },
]


def seed_products(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    for product in PRODUCTS:
        Product.objects.get_or_create(slug=product['slug'], defaults=product)


def remove_products(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    Product.objects.filter(slug__in=[product['slug'] for product in PRODUCTS]).delete()


class Migration(migrations.Migration):
    dependencies = [('store', '0001_initial')]
    operations = [migrations.RunPython(seed_products, remove_products)]