from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import UserInfo, Item
from .forms import UserInfoForm, ItemForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to the homepage after successful login
            else:
                return HttpResponse("Invalid login credentials.")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logoutUser(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")

@login_required
def home(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Form submitted successfully!")
            return redirect('user_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserInfoForm()

    return render(request, 'home.html', {'form': form})

@login_required
def user_data(request, id=None):
    customer = None
    if id:
        try:
            customer = UserInfo.objects.get(id=id)
            item_date = Item.objects.filter(customer_name=customer)
        except UserInfo.DoesNotExist:
            messages.error(request, "Customer not found.")
            return redirect('user_data')
    else:
        messages.error(request, "Customer ID is required.")
        return redirect('user_data')

    fm = ItemForm()

    if request.method == 'POST':
        medicines = request.POST.getlist('medicine[]')
        quantities = request.POST.getlist('quantity[]')
        prices = request.POST.getlist('price[]')
        paid_amounts = request.POST.getlist('paid_amount[]')
        dates = request.POST.getlist('date[]')

        max_length = max(len(medicines), len(quantities), len(prices))
        paid_amounts += ['0'] * (max_length - len(paid_amounts))
        dates += [None] * (max_length - len(dates))

        if not medicines or len(medicines) != max_length:
            messages.error(request, "All fields must be filled.")
            return redirect('user_data')

        for i in range(max_length):
            total = float(quantities[i]) * float(prices[i])
            item_date = dates[i] if dates[i] else None

            Item.objects.create(
                medicine=medicines[i],
                quantity=quantities[i],
                price=prices[i],
                paid_amount=paid_amounts[i],
                customer_name=customer,
                date=item_date
            )

        messages.success(request, "Successfully added items for the customer.")
        return redirect('/')

    users = UserInfo.objects.all()
    context = {'forms': fm, 'users': users, 'customer': customer}
    return render(request, 'user_data.html', context)

@login_required
def customer_data(request):
    users = UserInfo.objects.all().order_by('-created_at')
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    paginator = Paginator(users, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except Exception:
        page_obj = paginator.page(1)

    return render(request, 'delete.html', {'page_obj': page_obj, 'search': search_query})

@login_required
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

@login_required
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    customer_id = item.customer_name.id
    item.delete()
    return redirect('invoice', customer_id=customer_id)

@login_required
def delete_customer(request, id):
    customer = get_object_or_404(UserInfo, id=id)
    customer.delete()
    messages.success(request, "Customer deleted successfully.")
    return redirect('/')

@login_required
def user_profile(request):
    profiles = UserInfo.objects.all().order_by('created_at')
    search_query = request.GET.get('search', '')
    if search_query:
        profiles = profiles.filter(
            Q(username__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    paginator = Paginator(profiles, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except Exception:
        page_obj = paginator.page(1)

    return render(request, 'user_profile.html', {
        'page_obj': page_obj,
        'search': search_query,
    })
