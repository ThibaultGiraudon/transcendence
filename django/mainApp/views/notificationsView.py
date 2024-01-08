from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from ..models import Notification
from mainApp.views.utils import renderPage

def notifications(request):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})

	# Get notification
	notifs = list(request.user.notifications.all().order_by('-date'))
	request.user.nbNewNotifications = 0
	request.user.save()
	
	# Mark all notifications as read
	request.user.notifications.all().update(read=True)

	return renderPage(request, 'notifications.html', { 'notifs':notifs })


@require_POST
def delete_notification(request, notification_id):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})

	try:
		notification = Notification.objects.get(id=notification_id)
	except ObjectDoesNotExist:
		return JsonResponse({'redirect': '/notifications/'})

	notification.delete()
	return JsonResponse({'redirect': '/notifications/'})


@require_POST
def delete_all_notifications(request):
	if not request.user.is_authenticated:
		return JsonResponse({'redirect': '/sign_in/'})

	request.user.notifications.all().delete()
	return JsonResponse({'redirect': '/notifications/'})