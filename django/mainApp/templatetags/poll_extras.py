from django import template


# Create a template tag
register = template.Library()


@register.filter(name="previousMessageSenderID")
def previousMessageSenderID(messages, message):
	if message in messages:
		index = messages.index(message)

		if index > 0:
			return messages[index - 1]['sender']
	
	return None