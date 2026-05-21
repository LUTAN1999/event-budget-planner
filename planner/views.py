
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Category, Expense, Vendor
from django import forms
import csv
from django.http import HttpResponse

# ── Auth Views ──────────────────────────────────────────

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'planner/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'planner/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# ── Dashboard ───────────────────────────────────────────

@login_required
def dashboard(request):
    events = Event.objects.filter(user=request.user)
    return render(request, 'planner/dashboard.html', {'events': events})

# ── Event Views ─────────────────────────────────────────

@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user)
    return render(request, 'planner/event_list.html', {'events': events})

@login_required
def event_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']
        venue = request.POST.get('venue', '')
        total_budget = request.POST['total_budget']
        Event.objects.create(user=request.user, name=name, date=date, venue=venue, total_budget=total_budget)
        messages.success(request, 'Event created successfully!')
        return redirect('event_list')
    return render(request, 'planner/event_form.html')

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    categories = event.categories.all()
    vendors = event.vendors.all()
    return render(request, 'planner/event_detail.html', {'event': event, 'categories': categories, 'vendors': vendors})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event.name = request.POST['name']
        event.date = request.POST['date']
        event.venue = request.POST.get('venue', '')
        event.total_budget = request.POST['total_budget']
        event.save()
        messages.success(request, 'Event updated!')
        return redirect('event_detail', pk=pk)
    return render(request, 'planner/event_form.html', {'event': event})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'planner/event_confirm_delete.html', {'event': event})

# ── Category Views ──────────────────────────────────────

@login_required
def category_add(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk, user=request.user)
    if request.method == 'POST':
        name = request.POST['name']
        allocated_budget = request.POST['allocated_budget']
        Category.objects.create(event=event, name=name, allocated_budget=allocated_budget)
        messages.success(request, 'Category added!')
        return redirect('event_detail', pk=event_pk)
    return render(request, 'planner/category_form.html', {'event': event})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    event_pk = category.event.pk
    if request.method == 'POST':
        category.delete()
        return redirect('event_detail', pk=event_pk)
    return render(request, 'planner/category_confirm_delete.html', {'category': category})

# ── Expense Views ───────────────────────────────────────

@login_required
def expense_add(request, cat_pk):
    category = get_object_or_404(Category, pk=cat_pk)
    if request.method == 'POST':
        title = request.POST['title']
        amount = request.POST['amount']
        date = request.POST['date']
        status = request.POST['status']
        note = request.POST.get('note', '')
        Expense.objects.create(category=category, title=title, amount=amount, date=date, status=status, note=note)
        messages.success(request, 'Expense added!')
        return redirect('event_detail', pk=category.event.pk)
    return render(request, 'planner/expense_form.html', {'category': category})

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.date = request.POST['date']
        expense.status = request.POST['status']
        expense.note = request.POST.get('note', '')
        expense.save()
        messages.success(request, 'Expense updated!')
        return redirect('event_detail', pk=expense.category.event.pk)
    return render(request, 'planner/expense_form.html', {'expense': expense, 'category': expense.category})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    event_pk = expense.category.event.pk
    if request.method == 'POST':
        expense.delete()
        return redirect('event_detail', pk=event_pk)
    return render(request, 'planner/expense_confirm_delete.html', {'expense': expense})

# ── Vendor Views ────────────────────────────────────────

@login_required
def vendor_add(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk, user=request.user)
    if request.method == 'POST':
        name = request.POST['name']
        service = request.POST['service']
        amount = request.POST['amount']
        contact = request.POST.get('contact', '')
        paid = request.POST.get('paid') == 'on'
        Vendor.objects.create(event=event, name=name, service=service, amount=amount, contact=contact, paid=paid)
        messages.success(request, 'Vendor added!')
        return redirect('event_detail', pk=event_pk)
    return render(request, 'planner/vendor_form.html', {'event': event})

@login_required
def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    event_pk = vendor.event.pk
    if request.method == 'POST':
        vendor.delete()
        return redirect('event_detail', pk=event_pk)
    return render(request, 'planner/vendor_confirm_delete.html', {'vendor': vendor})

# ── Export Views ────────────────────────────────────────

@login_required
def export_csv(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{event.name}_budget.csv"'
    writer = csv.writer(response)
    writer.writerow(['Category', 'Expense', 'Amount', 'Date', 'Status'])
    for cat in event.categories.all():
        for exp in cat.expenses.all():
            writer.writerow([cat.name, exp.title, exp.amount, exp.date, exp.status])
    return response

@login_required
def export_pdf(request, pk):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    event = get_object_or_404(Event, pk=pk, user=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{event.name}_budget.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Event Budget Report: {event.name}")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Total Budget: Rs.{event.total_budget}")
    p.drawString(50, height - 100, f"Total Spent: Rs.{event.total_spent()}")
    p.drawString(50, height - 120, f"Remaining: Rs.{event.remaining_budget()}")
    y = height - 160
    for cat in event.categories.all():
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, f"Category: {cat.name}")
        y -= 20
        p.setFont("Helvetica", 11)
        for exp in cat.expenses.all():
            p.drawString(70, y, f"{exp.title} - Rs.{exp.amount} - {exp.status}")
            y -= 18
            if y < 60:
                p.showPage()
                y = height - 50
    p.save()
    return response