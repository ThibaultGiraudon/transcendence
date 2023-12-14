from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from users_app.models import Notification

def notifications(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	# Get notification
	notifs = list(request.user.notifications.all().order_by('-date'))
	request.user.nbNewNotifications = 0
	request.user.save()
	
	# Mark all notifications as read
	request.user.notifications.all().update(read=True)

	return render(request, 'notifications.html', context={ 'notifs':notifs })

@require_POST
def delete_notification(request, notification_id):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	try:
		notification = Notification.objects.get(id=notification_id)
	except ObjectDoesNotExist:
		return redirect('notifications')

	notification.delete()
	return redirect('notifications')

@require_POST
def delete_all_notifications(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	request.user.notifications.all().delete()
	return redirect('notifications')