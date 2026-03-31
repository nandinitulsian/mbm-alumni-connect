from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Connection
from accounts.models import User, AlumniProfile

@login_required
def connections_page(request):
    user = request.user

    if user.role == 'student':
        # Show all alumni
        alumni_list = User.objects.filter(
            role='alumni',
            is_active=True
        ).select_related('alumni_profile')

        # Get connection statuses
        my_connections = Connection.objects.filter(student=user)
        connected_ids = my_connections.filter(
            status='accepted'
        ).values_list('alumni_id', flat=True)
        pending_ids = my_connections.filter(
            status='pending'
        ).values_list('alumni_id', flat=True)

        return render(request, 'connections/browse_alumni.html', {
            'alumni_list'   : alumni_list,
            'connected_ids' : connected_ids,
            'pending_ids'   : pending_ids,
        })

    else:
        # Alumni sees their connection requests
        pending_requests = Connection.objects.filter(
            alumni=user,
            status='pending'
        ).select_related('student')

        accepted_connections = Connection.objects.filter(
            alumni=user,
            status='accepted'
        ).select_related('student')

        return render(request, 'connections/manage_connections.html', {
            'pending_requests'    : pending_requests,
            'accepted_connections': accepted_connections,
        })

@login_required
def send_connection(request, alumni_id):
    if request.user.role != 'student':
        messages.error(request, 'Only students can send connection requests!')
        return redirect('connections_page')

    alumni = get_object_or_404(User, id=alumni_id, role='alumni')

    already_exists = Connection.objects.filter(
        student=request.user,
        alumni=alumni
    ).exists()

    if already_exists:
        messages.error(request, 'Connection request already sent!')
    else:
        Connection.objects.create(
            student=request.user,
            alumni=alumni,
            status='pending'
        )
        messages.success(request, f'Connection request sent to {alumni.full_name}!')

    return redirect('connections_page')

@login_required
def accept_connection(request, connection_id):
    connection = get_object_or_404(Connection, id=connection_id, alumni=request.user)
    connection.status = 'accepted'
    connection.save()
    messages.success(request, f'Connected with {connection.student.full_name}!')
    return redirect('connections_page')

@login_required
def reject_connection(request, connection_id):
    connection = get_object_or_404(Connection, id=connection_id, alumni=request.user)
    connection.status = 'rejected'
    connection.save()
    messages.success(request, 'Connection request rejected.')
    return redirect('connections_page')

@login_required
def withdraw_connection(request, alumni_id):
    alumni = get_object_or_404(User, id=alumni_id, role='alumni')
    Connection.objects.filter(
        student=request.user,
        alumni=alumni
    ).delete()
    messages.success(request, 'Connection request withdrawn.')
    return redirect('connections_page')