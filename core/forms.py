from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Ticket

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [
            ('Client', 'Client'),
            ('Technician', 'Technician'),
        ]
    # Remove default help texts
        for field in [ 'password2']:
            self.fields[field].help_text = ''
            
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'category',
            'client_contact',
            'priority',
            'account_number',
            'location',
            'connection_type',
        ]

class AssignTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['assigned_to', 'priority']

    def __init__(self, *args, **kwargs):
        super(AssignTicketForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(role='Technician')

class TechnicianUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'comments']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        ticket = super().save(commit=False)
        if ticket.status == 'Closed' and self.user:
            ticket.solved_by = self.user.get_full_name() or self.user.username
        if commit:
            ticket.save()
        return ticket
