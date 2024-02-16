from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {
        'form' : form,
    }
    return render(request, 'registration/register.html', context)
