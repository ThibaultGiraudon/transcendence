from django.shortcuts import render, redirect
from django.db import connection
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from users_app.models import Notification


def home(request):
	return render(request, 'home.html')


def pong(request):
	if not request.user.is_authenticated:
		return redirect('sign_in')

	if request.method == 'GET' and 'error' in request.GET:
		return redirect('sign_in')
	return render(request, 'pong_elements/pong.html')


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


def testDBConnection(request):
	try:
		with connection.cursor() as cursor:
			cursor.execute("SELECT 1")
		connection.close()
		return render(request, 'success.html')
	except Exception as error:
		return render(request, 'error.html')


def custom_404(request, exception):
	return render(request, 'errors/404.html', status=404)