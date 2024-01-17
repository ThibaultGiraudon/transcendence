from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string


def is_ajax(request):
	return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def renderPage(request, page, pageContext={}, userStatus="online"):
	# Set user status to online
	if request.user.is_authenticated:
		request.user.status = userStatus
		request.user.save()

	# Context
	context = {'request': request}
	if pageContext:
		context.update(pageContext)

	# Generate header HTML
	header_html = render_to_string('header.html', context)
	context['header'] = header_html

	# AJAX and HTML response
	if is_ajax(request):
		html = render_to_string(page, context)
		return JsonResponse({'html': html, 'header': header_html})
	else:
		context['page_content'] = render_to_string(page, context)
		return render(request, 'base.html', context)


def renderHeader(request):
	# Context
	context = {'request': request}

	# Generate header HTML
	header_html = render_to_string('header.html', context)

	# AJAX and HTML response
	if is_ajax(request):
		return JsonResponse({'header': header_html})
	else:
		return renderPage(request, 'base.html')


def renderError(request, status, pageContext={}):
	# Context
	context = {'request': request, 'status': status}
	if pageContext:
		context.update(pageContext)

	# Generate header HTML
	header_html = render_to_string('header.html', context)
	context['header'] = header_html

	# AJAX and HTML response
	if is_ajax(request):
		html = render_to_string(f"errors.html", context)
		return JsonResponse({'html': html, 'header': header_html})
	else:
		context['page_content'] = render_to_string(f"errors.html", context)
		return render(request, "base.html", context)


def redirectPage(request, page):
	# AJAX and HTML response
	if is_ajax(request):
		return JsonResponse({'redirect': page})
	else:
		return redirect(page)