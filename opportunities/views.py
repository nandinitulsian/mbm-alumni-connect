from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Opportunity, Application
from .forms import OpportunityForm

@login_required
def opportunities_list(request):
    type_filter = request.GET.get('type', '')
    domain_filter = request.GET.get('domain', '')

    opportunities = Opportunity.objects.all().select_related('posted_by')

    if type_filter:
        opportunities = opportunities.filter(type=type_filter)
    if domain_filter:
        opportunities = opportunities.filter(domain__icontains=domain_filter)

    applied_ids = []
    if request.user.role == 'student':
        applied_ids = Application.objects.filter(
            student=request.user
        ).values_list('opportunity_id', flat=True)

    return render(request, 'opportunities/list.html', {
        'opportunities' : opportunities,
        'type_filter'   : type_filter,
        'domain_filter' : domain_filter,
        'applied_ids'   : applied_ids,
    })

@login_required
def post_opportunity(request):
    if request.user.role != 'alumni':
        messages.error(request, 'Only alumni can post opportunities!')
        return redirect('opportunities_list')

    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opp = form.save(commit=False)
            opp.posted_by = request.user
            opp.save()
            messages.success(request, 'Opportunity posted successfully!')
            return redirect('opportunities_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = OpportunityForm()

    return render(request, 'opportunities/post_opportunity.html', {'form': form})

@login_required
def opportunity_detail(request, opp_id):
    opportunity = get_object_or_404(Opportunity, id=opp_id)
    has_applied = False

    if request.user.role == 'student':
        has_applied = Application.objects.filter(
            student=request.user,
            opportunity=opportunity
        ).exists()

    applications = None
    if request.user == opportunity.posted_by:
        applications = opportunity.applications.all().select_related('student')

    return render(request, 'opportunities/detail.html', {
        'opportunity' : opportunity,
        'has_applied' : has_applied,
        'applications': applications,
    })

@login_required
def apply_opportunity(request, opp_id):
    if request.user.role != 'student':
        messages.error(request, 'Only students can apply!')
        return redirect('opportunities_list')

    opportunity = get_object_or_404(Opportunity, id=opp_id)
    already_applied = Application.objects.filter(
        student=request.user,
        opportunity=opportunity
    ).exists()

    if already_applied:
        messages.error(request, 'You have already applied for this opportunity!')
    else:
        Application.objects.create(
            student=request.user,
            opportunity=opportunity
        )
        messages.success(request, f'Successfully applied to {opportunity.company}!')

    return redirect('opportunity_detail', opp_id=opp_id)