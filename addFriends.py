import vk_api
from wallPost import captcha_handler


def addFriends(login, password):
	# login, password = '+79012993071', 'qwerASDF1234'
	vk_session = vk_api.VkApi(
		login, password,
		captcha_handler=captcha_handler
	)

	try:
		vk_session.auth(token_only=True)
	except vk_api.AuthError as error_msg:
		print(error_msg)
		return
	'''
	Отправление заявок в друзья рекомендованным пользователям
	'''
	with vk_api.VkRequestsPool(vk_session) as pool:
		friends = pool.method('friends.getSuggestions')

	# count_requests = friends.result['count']
	list_requests = friends.result['items']
	number_friends = 40
	for i in range(number_friends):
		with vk_api.VkRequestsPool(vk_session) as pool:
			pool.method('friends.add', {
				'user_id': list_requests[i]['id']
			})
	print(f'Отправлено {number_friends} заявок в друзья')

	'''
	Одобрение всех заявок в друзья, которые есть на данный момент
	'''
	with vk_api.VkRequestsPool(vk_session) as pool:
		friends = pool.method('friends.getRequests', {
			'count': 1000
		})
	count_requests = friends.result['count']
	list_requests = friends.result['items']
	with vk_api.VkRequestsPool(vk_session) as pool:
		for i in range(count_requests):
			pool.method('friends.add', {
				'user_id': list_requests[i]
			})
	print(f'Принято {count_requests} заявок в друзья')


if __name__ == '__main__':
	addFriends('+79012993071', 'qwerASDF1234')