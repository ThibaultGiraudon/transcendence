from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string


def renderPage(request, page, pageContext={}):
	# Context
	context = {'request': request}
	if pageContext:
		context.update(pageContext)
	
	# Generate header HTML
	header_html = render_to_string('header.html', context)
	context['header'] = header_html

	# AJAX and HTML response
	if request.is_ajax():
		html = render_to_string(page, context)
		return JsonResponse({'html': html, 'header': header_html})
	else:
		context['page_content'] = render_to_string(page, context)
		return render(request, 'base.html', context)