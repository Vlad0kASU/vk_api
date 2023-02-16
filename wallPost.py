import vk_api
from requests_html import HTMLSession
import wget
import os
from PIL import Image, ImageEnhance



def captcha_handler(captcha):
	""" При возникновении капчи вызывается эта функция и ей передается объект
		капчи. Через метод get_url можно получить ссылку на изображение.
		Через метод try_again можно попытаться отправить запрос с кодом капчи
	"""
	key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
	return captcha.try_again(key)


def wallPost(number):
	login, password = '+79012993071', 'qwerASDF1234'
	vk_session = vk_api.VkApi(
		login, password,
		captcha_handler=captcha_handler
	)

	try:
		vk_session.auth(token_only=True)
	except vk_api.AuthError as error_msg:
		print(error_msg)
		return
	vk = vk_session.get_api()


	session = HTMLSession()

	r = session.get('https://www.mos.ru/search?category=newsfeed&hostApplied=false&page=1&q=&types=news')
	r.html.render(timeout=200)
	i = 0
	for sec in r.html.find('section'):
		if "class=('search-result-item',)" in str(sec):

			header = str(sec.text).split('\n')[0] # Заголовок
			section_a = str(sec.find('a')[1])
			href = section_a[section_a.find('href') + 6:section_a.find('target') - 2]
			n = session.get(href)
			n.html.render(timeout=200)
			text = ''
			filename = ''
			post_image = ''
			for section in n.html.find('section'):
				if 'news-article__preview' in str(section): # Первый абзац
					text += section.text
				elif 'news-article__text' in str(section): # Второй абзац
					text += '\n\n▪ ' + section.find('p')[0].text
				elif 'article-image' in str(section): # Картинка к посту
					image_href = str(section.find('img')[0])
					image_href = image_href[image_href.find("'img' src") + 11:image_href.find('srcset') - 2]
					filename = wget.download('https://www.mos.ru' + image_href)
					im = Image.open(filename)
					im = im.transpose(Image.FLIP_LEFT_RIGHT)
					enhancer = ImageEnhance.Brightness(im)
					im = enhancer.enhance(0.9)
					post_image = f'{str(i+1)+filename[filename.rfind("."):]}'
					im.save(post_image)
			post_text = f'''❗{header}❗

▪ {text}

Подробнее можно узнать по ссылке👇
{href}'''
			os.remove(filename)
			upload = vk_api.VkUpload(vk_session)
			photo = upload.photo(
				post_image,
				album_id=291053478
			)
			os.remove(post_image)
			i += 1
			media_id = vk.wall.post(message=post_text,
							   attachments=f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}')['post_id']
			print(media_id)
			# media_id = 213
			# print(vk.messages.send(user_id=182214266,
			# 					   attachments=f'wall732800790_{media_id}'))
			if i == number:
				break


if __name__ == '__main__':
	wallPost(1)
