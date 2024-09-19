from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from .models import UserInfo,Item
from .forms import UserInfoForm,ItemForm
from django.contrib import messages



def home(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            print('Data saved:', form.cleaned_data)  # Debugging: print the cleaned data
            return redirect('user_data')  # Redirect after successful form submission
        else:
            print('Form errors:', form.errors)  # Debugging: print the form errors
    else:
        form = UserInfoForm()  # Empty form for GET request

    return render(request, 'home.html', {'form': form})






def user_data(request):
    fm = ItemForm()  # Initialize 'fm' with an empty form

    if request.method == 'POST':
        print("POST data:", request.POST)  # Print all POST data for debugging

        # Validate and process customer_name
        customer_id = request.POST.get('customer_name')
        try:
            customer = UserInfo.objects.get(id=customer_id)
        except UserInfo.DoesNotExist:
            messages.error(request, "Customer not found.")
            return redirect('user_data')

        # Process dynamic fields
        medicines = request.POST.getlist('medicine[]')
        quantities = request.POST.getlist('quantity[]')
        prices = request.POST.getlist('price[]')
        paid_amounts = request.POST.getlist('paid_amount[]')

        # Validate that the lists are not empty and have the same length
        if not medicines or not quantities or not prices:
            messages.error(request, "All fields (medicines, quantities, and prices) must be filled.")
            return redirect('user_data')

        if len(medicines) != len(quantities) or len(quantities) != len(prices):
            messages.error(request, "The number of medicines, quantities, and prices must be equal.")
            return redirect('/')

        # Ensure paid_amounts list is the same length as others, default missing values to 0
        paid_amounts += ['0'] * (len(medicines) - len(paid_amounts))

        # If validation passes, create Item objects
        for i in range(len(medicines)):
            total = float(quantities[i]) * float(prices[i])  # Calculate total

            Item.objects.create(
                medicine=medicines[i],
                quantity=quantities[i],
                price=prices[i],
                paid_amount=paid_amounts[i],
                customer_name=customer
            )

        messages.success(request, "Successfully added customer and items.")
        return redirect('/')

    # For GET requests, render the empty form
    users = UserInfo.objects.all()
    context = {'forms': fm, 'users': users}
    return render(request, 'user_data.html', context)





def customer_data(request):
    users = UserInfo.objects.all()  # Retrieve all users

    # Initialize the Paginator (change instance name to `paginator`)
    paginator = Paginator(users, 5)  # Paginate with 10 users per page

    # Get the page number from the request
    page_number = request.GET.get('page')

    # Get the page object for the current page number
    page_obj = paginator.get_page(page_number)

    # Render the template and pass the page object
    return render(request, 'delete.html', {'users': users, 'page_obj': page_obj})

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
    return redirect('home')



