from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommissionForm
from .models import CommissionRequest


def _calculate_price(commission_type, size, desc_length):
    """Server-side price calculation (never trust client-side values)."""
    base = 120 if commission_type == 'portrait' else 80
    size_mult = 2.0 if ('large' in size.lower() or 'a3' in size.upper()) else 1.0
    complexity = 1.5 if desc_length > 300 else 1.0
    return round(base * size_mult * complexity, 2)


@login_required
def commission_create(request):
    """Create a new commission request with live JS price preview."""
    if request.method == 'POST':
        form = CommissionForm(request.POST, request.FILES)
        if form.is_valid():
            commission = form.save(commit=False)
            commission.user = request.user
            commission.estimated_price = _calculate_price(
                commission.commission_type,
                commission.size,
                len(commission.description),
            )
            commission.save()
            messages.success(
                request,
                f'Commission request #{commission.id} submitted! '
                f'Estimated \u20ac{commission.estimated_price}'
            )
            return redirect('dashboard')
    else:
        form = CommissionForm()

    return render(request, 'commissions/commission_form.html', {'form': form})


@login_required
def commission_edit(request, pk):
    """Edit an existing commission (only if still editable)."""
    commission = get_object_or_404(
        CommissionRequest, pk=pk, user=request.user
    )
    if not commission.is_editable_by_user():
        messages.error(request, 'This commission can no longer be edited.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = CommissionForm(request.POST, request.FILES, instance=commission)
        if form.is_valid():
            commission = form.save(commit=False)
            commission.estimated_price = _calculate_price(
                commission.commission_type,
                commission.size,
                len(commission.description),
            )
            commission.save()
            messages.success(request, 'Commission updated successfully.')
            return redirect('dashboard')
    else:
        form = CommissionForm(instance=commission)

    return render(request, 'commissions/commission_form.html', {
        'form': form,
        'editing': True,
        'commission': commission,
    })


@login_required
def commission_delete(request, pk):
    """Delete a commission request (only if editable)."""
    commission = get_object_or_404(
        CommissionRequest, pk=pk, user=request.user
    )
    if not commission.is_editable_by_user():
        messages.error(request, 'This commission can no longer be deleted.')
        return redirect('dashboard')

    if request.method == 'POST':
        commission.delete()
        messages.success(request, 'Commission request deleted.')
        return redirect('dashboard')

    return render(request, 'commissions/commission_confirm_delete.html', {
        'commission': commission,
    })
