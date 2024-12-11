from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from .models import UserInfo,Item
from .forms import UserInfoForm,ItemForm
from django.contrib import messages
from django.db.models import Q



def home(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            print('Data saved:', form.cleaned_data)  # Debugging: print the cleaned data
            return redirect('user_profile')  # Redirect after successful form submission
        else:
            print('Form errors:', form.errors)  # Debugging: print the form errors
    else:
        form = UserInfoForm()  # Empty form for GET request

    return render(request, 'home.html', {'form': form})






from django.utils import timezone

from django.utils import timezone

def user_data(request, id=None):
    customer = None

    # Validate customer ID from the URL parameter
    if id:
        try:
            customer = UserInfo.objects.get(id=id)
            item_date=Item.objects.filter(customer_name=customer)
        except UserInfo.DoesNotExist:
            messages.error(request, "Customer not found.")
            return redirect('user_data')  # Or redirect to a safe page, like the customer list
    else:
        messages.error(request, "Customer ID is required.")
        return redirect('user_data')

    fm = ItemForm()  # Initialize 'fm' with an empty form

    if request.method == 'POST':
        print("POST data:", request.POST)  # Print all POST data for debugging

        # Process dynamic fields
        medicines = request.POST.getlist('medicine[]')
        quantities = request.POST.getlist('quantity[]')
        prices = request.POST.getlist('price[]')
        paid_amounts = request.POST.getlist('paid_amount[]')
        dates = request.POST.getlist('date[]')  # Retrieve date field

        # Ensure lists have the same length by padding if necessary
        max_length = max(len(medicines), len(quantities), len(prices))
        paid_amounts += ['0'] * (max_length - len(paid_amounts))
        dates += [None] * (max_length - len(dates))  # Default missing dates to None

        # Check that lists are not empty and have the same length
        if not medicines or len(medicines) != max_length:
            messages.error(request, "All fields (medicines, quantities, and prices) must be filled.")
            return redirect('user_data')

        # Create Item objects
        for i in range(max_length):
            total = float(quantities[i]) * float(prices[i])  # Calculate total
            item_date = dates[i] if dates[i] else None  # Use date or set to None if empty

            Item.objects.create(
                medicine=medicines[i],
                quantity=quantities[i],
                price=prices[i],
                paid_amount=paid_amounts[i],
                customer_name=customer,
                date=item_date  # Save the date
            )

        messages.success(request, "Successfully added items for the customer.")
        return redirect('/')

    # For GET requests, render the empty form
    users = UserInfo.objects.all()
    context = {'forms': fm, 'users': users, 'customer': customer}
    return render(request, 'user_data.html', context)









def customer_data(request):
    # Retrieve all users initially
    users = UserInfo.objects.all().order_by('-created_at')

    # Handle search functionality
    search_query = request.GET.get('search', '')  # Get search query from URL
    if search_query:
        # Filter users based on the search term (username, phone, or address)
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    # Initialize the Paginator
    paginator = Paginator(users, 10)  # Paginate with 5 users per page

    # Get the page number from the request
    page_number = request.GET.get('page', 1)  # Default to page 1 if not provided

    try:
        # Get the page object for the current page number
        page_obj = paginator.page(page_number)
    except Exception as e:
        # If page is out of range or invalid, show the first page
        page_obj = paginator.page(1)

    # Render the template and pass the page object and search term
    return render(request, 'delete.html', {'page_obj': page_obj, 'search': search_query})

def invoice(request, customer_id):
    customer = UserInfo.objects.get(id=customer_id)
    items = Item.objects.filter(customer_name=customer)
    
    for item in items:
        item.remaining_amount = item.amount - item.paid_amount
    
    total_amount = sum(item.amount for item in items)
    total_paid_amount = sum(item.paid_amount for item in items)
    remaining_amount = total_amount - total_paid_amount
    
    return render(request, 'invoice.html', {
        'customer': customer,
        'items': items,
        'total_amount': total_amount,
        'total_paid_amount': total_paid_amount,
        'remaining_amount': remaining_amount
    })





# def update_paid_amount(request, item_id):
#     item = Item.objects.get(id=item_id)
#     paid_amount = request.POST.get('paid_amount')
#     item.paid_amount = paid_amount
#     item.save()
#     return redirect('invoice', customer_id=item.customer_name.id)

def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    customer_id = item.customer_name.id
    item.delete()
    return redirect('invoice', customer_id=customer_id)

def delete_customer(request, id):


    customer = get_object_or_404(UserInfo, id=id)
    customer.delete()
    messages.success(request, "Customer deleted successfully.")
    return redirect('/')



def user_profile(request,id=id):
    # Retrieve all user profiles, ordered by creation date
    profiles = UserInfo.objects.all().order_by('created_at')

    # Handle search functionality
    search_query = request.GET.get('search', '')  # Get search query from URL
    if search_query:
        # Filter profiles based on the search term (username, phone, or address)
        profiles = profiles.filter(
            Q(username__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    # Paginate with 5 profiles per page
    paginator = Paginator(profiles, 10)

    # Get the page number from the request, default to 1
    page_number = request.GET.get('page', 1)

    try:
        # Get the page object for the current page number
        page_obj = paginator.page(page_number)
    except Exception:
        # If the page number is out of range or invalid, show the first page
        page_obj = paginator.page(1)

    # Pass profiles and pagination info to the template
    return render(request, 'user_profile.html', {
        'page_obj': page_obj,  # Paginated profiles
        'search': search_query,  # Retain the search query in the template
    })

