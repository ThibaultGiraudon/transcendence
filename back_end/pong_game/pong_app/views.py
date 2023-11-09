from django.shortcuts import render
from django.http import JsonResponse
from .models import Ball, Paddle

def	updatePosition(request):
	new_x = request.GET.get('x') + 10;
	new_y = request.GET.get('y') + 10;

	return JsonResponse({
		'ball': {'x': new_x, 'y': new_y},
		'paddle': {'x': new_x, 'y': new_y}})