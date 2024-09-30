import random
from datetime import datetime, timedelta
from django.shortcuts import render
from django.utils import timezone

# Sample menu items
MENU_ITEMS = {
    'Burger': 9.99,
    'Salad': 7.99,
    'Pasta': 11.99,
    'Pizza': 12.99
}


DAILY_SPECIALS = [
    'Chicken Parm',
    'Pasta Carbonara',
    'Spaghetti e Vongole'
]
images = ['https://media-cdn.tripadvisor.com/media/photo-s/0e/b7/b4/95/a-40-year-old-classic.jpg']


def main(request):
    context = {
        "image": random.choice(images)  # Randomly choose an image from the list
    }
    return render(request, 'restaurant/main.html', context)


def order(request):
    # Choose a random daily special from the list
    daily_special_name = random.choice(DAILY_SPECIALS)
    
    # Assign a price to the daily special
    daily_special_price = round(random.uniform(10.0, 20.0), 2)
    
    context = {
        'menu_items': MENU_ITEMS,
        'daily_special': {
            'name': daily_special_name,
            'price': daily_special_price
        }
    }
    return render(request, 'restaurant/order.html', context)


def confirmation(request):
    if request.method == 'POST':
        # Retrieve form data
        customer_name = request.POST.get('name', '')
        customer_phone = request.POST.get('phone', '')
        customer_email = request.POST.get('email', '')
        special_instructions = request.POST.get('instructions', '')

        # Determine ordered items
        ordered_items = []
        total_price = 0.0

        # Loop through menu items and check if any are selected
        for item, price in MENU_ITEMS.items():
            if request.POST.get(item):  # Only add item if checkbox is selected
                ordered_items.append({'name': item, 'price': price})
                total_price += price

        # Handle Daily Special (only if selected)
        if request.POST.get('daily_special_checkbox'):  # Check if daily special is selected
            daily_special = request.POST.get('daily_special')
            special_price = float(request.POST.get('daily_special_price', 0))
            ordered_items.append({'name': daily_special, 'price': special_price})
            total_price += special_price

        # Calculate expected ready time (30-60 minutes from now)
        now = timezone.now()
        ready_in_minutes = random.randint(30, 60)
        ready_time = now + timedelta(minutes=ready_in_minutes)

        context = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,  # Pass selected items only
            'total_price': total_price,  # If no items selected, total will be 0.0
            'ready_time': ready_time
        }

        return render(request, 'restaurant/confirmation.html', context)
    else:
        return render(request, 'restaurant/order.html')
