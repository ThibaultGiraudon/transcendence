from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.exceptions import ObjectDoesNotExist

from ..models import Notification
from mainApp.views.utils import renderPage, redirectPage

def notifications(request):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	# Get notification
	notifs = list(request.user.notifications.all().order_by('-date'))
	request.user.nbNewNotifications = 0
	request.user.save()
	
	# Mark all notifications as read
	request.user.notifications.all().update(read=True)

	return renderPage(request, 'notifications.html', { 'notifs': notifs })


@ensure_csrf_cookie
def delete_notification(request, notification_id):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	try:
		notification = Notification.objects.get(id=notification_id)
	except ObjectDoesNotExist:
		return redirectPage(request, '/notifications/')

	notification.delete()

	return redirectPage(request, '/notifications/')


def delete_all_notifications(request):
	if not request.user.is_authenticated:
		return redirectPage(request, '/sign_in/')

	request.user.notifications.all().delete()
	return redirectPage(request, '/notifications/')