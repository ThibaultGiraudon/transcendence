from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def renderPage(request, page, pageContext={}):
	# Context
	context = {}
	context['request'] = request
	context.update(pageContext)

	# AJAX and HTML response
	if request.is_ajax():
		html = render_to_string(page, context)
		return JsonResponse({'html': html})
	else:
		content = render_to_string(page, context)
		context['page_content'] = content
		return render(request, 'base.html', context)