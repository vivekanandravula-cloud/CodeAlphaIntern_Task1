from django.core.management.base import BaseCommand
from store.models import Product

SAMPLES = [
    ("Wireless Headphones", "Comfortable wireless headphones with clear sound and long battery life.", "1499.00", "Electronics", 25, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80"),
    ("Everyday Backpack", "A durable everyday backpack with room for your laptop and essentials.", "1899.00", "Accessories", 18, "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80"),
    ("Classic Wristwatch", "A clean, versatile wristwatch designed for everyday use.", "2299.00", "Accessories", 12, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80"),
    ("Running Shoes", "Lightweight trainers for walking, workouts, and daily movement.", "2799.00", "Fashion", 20, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80"),
    ("Ceramic Coffee Mug", "A simple ceramic mug for your morning coffee or tea.", "349.00", "Home", 40, "https://images.unsplash.com/photo-1514228742587-6b1558f?auto=format&fit=crop&w=900&q=80"),
    ("Desk Lamp", "A modern desk lamp for focused work and study.", "999.00", "Home", 15, "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80"),
]

class Command(BaseCommand):
    help = "Create sample products for the store."

    def handle(self, *args, **options):
        created = 0
        for name, description, price, category, stock, image_url in SAMPLES:
            _, was_created = Product.objects.get_or_create(
                name=name,
                defaults={"description": description, "price": price, "category": category,
                          "stock": stock, "image_url": image_url},
            )
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Seed complete. Added {created} new products."))
