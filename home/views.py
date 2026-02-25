from django.shortcuts import render
from django.contrib import messages


def index(request):
    """Homepage with banner-stack layout."""
    return render(request, 'home/index.html')


def about(request):
    """About the artist page."""
    return render(request, 'home/about.html')


def contact(request):
    """Contact page with form."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and message_text:
            # In production, send email via send_mail or store in DB
            messages.success(
                request,
                'Thanks for reaching out! Joe will get back to you soon.'
            )
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'home/contact.html')