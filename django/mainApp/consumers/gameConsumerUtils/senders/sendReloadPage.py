async def sendReloadPage(consumer, gameID):
	await consumer.channel_layer.group_send(
		f'game_{gameID}',
		{
			'type': 'reload_page',
		}
	)