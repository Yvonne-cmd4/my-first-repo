from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import TechnicianUpdateForm, CustomUserCreationForm, TicketForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_by_role(user)  # ✅ redirect by role here
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect_by_role(user)  # ✅ redirect by role here
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def redirect_by_role(user):
    if user.is_superuser or getattr(user, 'role', None) == 'Admin':
        return redirect('admin_dashboard')
    elif getattr(user, 'role', None) == 'Technician':
        return redirect('technician_dashboard')
    elif getattr(user, 'role', None) == 'Client':
        return redirect('client_dashboard')
    else:
        return redirect('login')  # fallback

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'Admin':
        tickets = Ticket.objects.all()
        tickets = Ticket.objects.filter(assigned_to__isnull=True)
    elif user.role == 'Technician':
        tickets = Ticket.objects.filter(assigned_to=user)
    else:  # Client
        tickets = Ticket.objects.filter(created_by=user)

    return render(request, 'dashboard.html', {'tickets': tickets, 'user': user})

@login_required
def admin_dashboard(request):
    user = request.user
    # Allow superuser OR users with role Admin
    if user.is_superuser or getattr(user, 'role', None) == 'Admin':
        open_tickets = Ticket.objects.filter(status='Open', assigned_to__isnull=True)
        in_progress_tickets = Ticket.objects.filter(status='In Progress')
        closed_tickets = Ticket.objects.filter(status='Closed')

        return render(request, 'dashboard.html', {
            'user': user,
            'open_tickets': open_tickets,
            'in_progress_tickets': in_progress_tickets,
            'closed_tickets': closed_tickets,
        })
    else:
        return redirect('dashboard')

@login_required
def technician_dashboard(request):
    if request.user.role != 'Technician':
        return redirect('dashboard')  # fallback for wrong role

    tickets = Ticket.objects.filter(assigned_to=request.user)
    return render(request, 'dashboard.html', {'tickets': tickets})

@login_required
def technician_ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, assigned_to=request.user)
    
    # Only allow Technician editing their own tickets, or Admin/Superuser
    if request.user.role != 'Technician' and not (request.user.is_superuser or request.user.role == 'Admin'):
        return redirect('dashboard')

    if request.user.role == 'Technician' and ticket.assigned_to != request.user:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = TechnicianUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            updated_ticket = form.save(commit=False)

            # If ticket is closed, set solved_by
            if updated_ticket.status == 'Closed':
                updated_ticket.solved_by = request.user.get_full_name() or request.user.username

            updated_ticket.save()
            return redirect('dashboard')  # return to main dashboard
    else:
        form = TechnicianUpdateForm(instance=ticket)

    return render(request, 'technician_edit_ticket.html', {'form': form, 'ticket': ticket})


def client_dashboard(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'dashboard.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    if request.user.role != 'Client':
        return redirect('dashboard')

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('dashboard')
    else:
        form = TicketForm()

    return render(request, 'create_ticket.html', {'form': form})

@login_required
def assign_ticket(request, ticket_id):
    if not (request.user.is_superuser or request.user.role == 'Admin'):
        return redirect('dashboard')

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        tech_id = request.POST.get('technician_id')
        technician = get_object_or_404(User, id=tech_id, role='Technician')
        ticket.assigned_to = technician
        ticket.status = 'In Progress'
        ticket.save()
        return redirect('admin_dashboard')

    # ✅ This was missing: send technicians to the template
    technicians = User.objects.filter(role='Technician')
    return render(request, 'assign_ticket.html', {
        'ticket': ticket,
        'technicians': technicians
    })


@login_required
def reassign_ticket(request, ticket_id):
    if not (request.user.is_superuser or request.user.role == 'Admin'):
        return redirect('dashboard')

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        tech_id = request.POST.get('technician_id')
        technician = get_object_or_404(User, id=tech_id, role='Technician')
        ticket.assigned_to = technician
        ticket.save()
        return redirect('admin_dashboard')

    # ✅ Add technician list for reassignment form
    technicians = User.objects.filter(role='Technician')
    return render(request, 'reassign_ticket.html', {
        'ticket': ticket,
        'technicians': technicians
    })