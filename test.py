import vk_api
from requests_html import HTMLSession
import wget
import os


def captcha_handler(captcha):
	""" При возникновении капчи вызывается эта функция и ей передается объект
		капчи. Через метод get_url можно получить ссылку на изображение.
		Через метод try_again можно попытаться отправить запрос с кодом капчи
	"""

	key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

	# Пробуем снова отправить запрос с капчей
	return captcha.try_again(key)


def main(number):
	# """ Пример обработки капчи """
	#
	login, password = '+79012993071', 'qwerASDF1234'
	vk_session = vk_api.VkApi(
		login, password,
		captcha_handler=captcha_handler  # функция для обработки капчи
	)

	try:
		vk_session.auth()
	except vk_api.AuthError as error_msg:
		print(error_msg)
		return
	vk = vk_session.get_api()


	session = HTMLSession()

	r = session.get('https://www.mos.ru/search?category=newsfeed&hostApplied=false&page=1&q=&types=news')
	r.html.render(timeout=20)  # this call executes the js in the page
	i = 0
	for sec in r.html.find('section'):
		if "class=('search-result-item',)" in str(sec):
			# print(sec)
			# print(sec.text)
			header = str(sec.text).split('\n')[0]
			section_a = str(sec.find('a')[1])
			href = section_a[section_a.find('href') + 6:section_a.find('target') - 2]
			# print(href)
			n = session.get(href)
			n.html.render(timeout=20)  # this call executes the js in the page
			text = ''
			# print(n.html.find('section'))
			for section in n.html.find('section'):

				if 'news-article__preview' in str(section):
					text += section.text
				elif 'news-article__text' in str(section):
					text += '\n\n▪ ' + section.find('p')[0].text
				elif 'article-image' in str(section):
					image_href = str(section.find('img')[0])
					image_href = image_href[image_href.find("'img' src") + 11:image_href.find('srcset') - 2]
					filename = wget.download('https://www.mos.ru' + image_href)

			post_text = f'''❗{header}❗

▪ {text}

Подробнее можно узнать по ссылке👇
{href}'''
			# print(post_text)

			# print(n.html.find('section'))
			# print(vk.wall.post(message=post_text, attachments=))
			with open(f'output{os.sep}{i+1}.txt', 'w', encoding='utf-8') as f:
				f.write(post_text)
			os.replace(filename, f'output{os.sep}{str(i+1)+filename[filename.rfind("."):]}')
			i += 1

			print(vk.wall.post(message=post_text))

			if i == number:
				break


if __name__ == '__main__':
	main(3)
