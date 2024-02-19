import datetime
from django.contrib.auth import logout

class SessionTimeoutMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if request.user.is_authenticated:
			# Get the last activity time from the session
			current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			last_activity = request.session.get('last_activity', None)
			
			if last_activity:
				last_activity = datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')

				# Timeout duration before logout (in seconds)
				if (datetime.datetime.now() - last_activity).seconds > 3600:
					logout(request)
			
			request.session['last_activity'] = current_time
		
		response = self.get_response(request)

		# Delete the sessionid cookie if the user is not authenticated
		if not request.user.is_authenticated:
			response.delete_cookie('sessionid')

		return response