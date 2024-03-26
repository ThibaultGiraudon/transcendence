from django.contrib.auth import get_user_model
import json

def set_all_users_offline():
	try:
		User = get_user_model()
		for user in User.objects.all():
			user.set_status("offline")
	except:
		pass


def containBadwords(message):
	# List of languages
	languages = ['fr', 'en']

	# Initialize the list of badwords
	badwords = []

	# Load badwords from the files
	for language in languages:
		with open(f'/home/app/web/staticfiles/badwords/{language}.json', 'r') as f:
			data = json.load(f)
			badwords.extend(data['words'])

	# Add a list of some first names
	badwordsNames = [
		"adolph",
		"hitler",
		"staline",
		"mussolini",
		"pétain",
		"poutine",
		"kimjongun",
		"benladen",
		"daesh",
		"alqaeda",
	]

	# Convert the message to lowercase
	message = message.lower()

	for word in badwords:
		# Convert the word to lowercase and check if it's in the message
		if message.find(word.lower()) != -1:
			return True

	for word in badwordsNames:
		# Convert the word to lowercase and check if it's in the message
		if message.find(word.lower()) != -1:
			return True

	return False