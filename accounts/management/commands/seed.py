# accounts/management/commands/populate_fake_data.py

from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, UserProfile
from vendor.models import Vendor, OpeningHours
from menu.models import Category, FoodItem
from datetime import time


class Command(BaseCommand):
    help = "Generate fake data for the database"

    def handle(self, *args, **kwargs):
        faker = Faker()

        predefined_categories = {
            "Burgers": [
                "Double Burger",
                "Cheese Burger",
                "Veggie Burger",
                "Chicken Burger",
                "Fish Burger",
                "Bacon Burger",
                "Mushroom Burger",
                "BBQ Burger",
                "Black Bean Burger",
                "Turkey Burger",
            ],
            "Pizzas": [
                "Pepperoni Pizza",
                "Margherita Pizza",
                "BBQ Chicken Pizza",
                "Hawaiian Pizza",
                "Veggie Pizza",
                "Meat Lovers Pizza",
                "Cheese Pizza",
                "Buffalo Chicken Pizza",
                "Supreme Pizza",
                "White Pizza",
            ],
            "Salads": [
                "Caesar Salad",
                "Greek Salad",
                "Cobb Salad",
                "Garden Salad",
                "Caprese Salad",
                "Pasta Salad",
                "Chicken Salad",
                "Taco Salad",
                "Quinoa Salad",
                "Fruit Salad",
            ],
            "Sushi": [
                "California Roll",
                "Tuna Roll",
                "Salmon Roll",
                "Avocado Roll",
                "Rainbow Roll",
                "Spicy Tuna Roll",
                "Dragon Roll",
                "Tempura Roll",
                "Philadelphia Roll",
                "Shrimp Tempura Roll",
            ],
            "Desserts": [
                "Chocolate Cake",
                "Cheesecake",
                "Brownie",
                "Ice Cream",
                "Pudding",
                "Apple Pie",
                "Tiramisu",
                "Cupcake",
                "Macarons",
                "Mousse",
            ],
            "Beverages": [
                "Coke",
                "Pepsi",
                "Lemonade",
                "Iced Tea",
                "Coffee",
                "Smoothie",
                "Milkshake",
                "Water",
                "Orange Juice",
                "Apple Juice",
            ],
            "Sandwiches": [
                "BLT",
                "Club Sandwich",
                "Turkey Sandwich",
                "Ham Sandwich",
                "Veggie Sandwich",
                "Grilled Cheese",
                "Chicken Sandwich",
                "Egg Salad Sandwich",
                "Tuna Sandwich",
                "Meatball Sandwich",
            ],
            "Pasta": [
                "Spaghetti Bolognese",
                "Fettuccine Alfredo",
                "Penne Arrabiata",
                "Lasagna",
                "Carbonara",
                "Pesto Pasta",
                "Seafood Pasta",
                "Mac and Cheese",
                "Ravioli",
                "Gnocchi",
            ],
        }

        # Create fake users and profiles
        for _ in range(15):
            user = User.objects.create_user(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                username=faker.user_name(),
                email=faker.unique.email(),  # Ensure unique emails
                password="password123",
            )
            profile = UserProfile.objects.get(user=user)
            profile.phone_number = faker.phone_number()
            profile.bio = faker.text()
            profile.address = faker.address()
            profile.country = faker.country()
            profile.state = faker.state()
            profile.city = faker.city()
            profile.pincode = faker.postcode()
            profile.longitude = faker.longitude()
            profile.latitude = faker.latitude()
            profile.save()

            # Create fake vendor
            vendor = Vendor.objects.create(
                user=user,
                user_profile=profile,
                vendor_name=faker.company(),
                vendor_slug=faker.slug(),
                vendor_license=faker.image_url(),
                is_approved=True,
            )

            # Create fake opening hours
            for day in range(1, 8):  # Days from Monday(1) to Sunday(7)
                OpeningHours.objects.create(
                    vendor=vendor,
                    day=day,
                    from_hour=faker.time(pattern="%I:%M %p"),
                    to_hour=faker.time(pattern="%I:%M %p"),
                    is_closed=faker.boolean(),
                )

            # Create predefined categories and related food items
            for category_name, food_items in predefined_categories.items():
                category = Category.objects.create(
                    vendor=vendor,
                    category_name=category_name,
                    description=faker.text(),
                    slug=faker.slug(),
                )
                for food_item_name in food_items:
                    FoodItem.objects.create(
                        vendor=vendor,
                        category=category,
                        food_name=food_item_name,
                        description=faker.text(),
                        price=faker.random_number(digits=2),
                        image=faker.image_url(),
                        is_available=faker.boolean(),
                        slug=faker.slug(),
                    )

        self.stdout.write(self.style.SUCCESS("Successfully populated fake data"))
