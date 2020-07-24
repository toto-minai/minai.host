import requests
from bs4 import BeautifulSoup
import json

def get_terms(query, manual_tag):
	r = requests.get('https://jisho.org/api/v1/search/words?keyword={}'.format(query))
	response = json.loads(r.text)
	if response['meta']['status'] == 200:
		data = response['data']
		candidates = [d['slug'] for d in data]
		candidates_cnt = len(candidates)
		hint = ' '.join(['[{}] {}'.format('x' if i == 0 else i+1, candidates[i]) for i in range(candidates_cnt)])

		if manual_tag:
			print(hint, end=" ? ")
			choice_raw = input()

		pool = []
		terms = []

		if not manual_tag:
			pool.append(data[0])
		else:
			if choice_raw == '':
				pool.append(data[0])
			else:
				for c in choice_raw:
					if c == '+':
						pool.append(data[0])
					elif int(c) <= candidates_cnt:
						pool.append(data[int(c)-1])  

		for p in pool:
			word = p['slug']
			prononciation = p['japanese'][0]['reading']
			senses = p['senses']
			definitions = []
			part_of_speeches = []
			for sense in senses:
				definitions.append(', '.join(sense['english_definitions']))
				part_of_speeches += sense['parts_of_speech']
			# part_of_speeches.unique()

			sentences_r = requests.get('https://jisho.org/search/{}%20%23sentences'.format(word))
			sentences_soup = BeautifulSoup(sentences_r.text, 'html.parser')

			count = 0
			examples = ''
			for item in sentences_soup.find_all(attrs={'class': 'sentence_content'}):
				jp_text = ''
				for part in item.ul.contents:
					if part.name:
						furigana = part.find(attrs={'class': 'furigana'})
						original = part.find(attrs={'class': 'unlinked'}).string

						if furigana:
							jp_text += '<ruby>{}<rt>{}</rt></ruby>'.format(original, furigana.string)
						else:
							jp_text += original
					else:
						jp_text += str(part)

				en_text = item.find(attrs={'class': 'english'}).string
				example = '<p>'+jp_text.strip()+'<br />'+en_text+'</p>'

				examples += example

				count += 1
				if count >= 2: break

			terms.append([
				word,
				'' if word == prononciation else prononciation,
				'0',
				'<br />'.join(['{}. '.format(i+1) + definitions[i] for i in range(len(definitions))]),
				examples
			])

		# print(terms)

		return terms

	return []

	# r = requests.get('https://dictionary.goo.ne.jp/word/en/{}'.format(word))
	# soup = BeautifulSoup(r.text, 'html.parser')

	# element = soup.find(attrs={'class': 'list-data-b-in'})
	# definition = soup.find(attrs={'class': 'in-ttl-b'})
	# prononciation = soup.find(attrs={'class': 'contents-wrap-b-in'}).div.h2.string.strip().split('【')[0]
	# jp_ex = element.find(attrs={'class': 'text-jejp'}).string
	# en_ex_raw = element.find(attrs={'class': 'text-jeen'}).contents
	# en_ex = ''.join([str(x) for x in en_ex_raw]).replace('i>', 'b>')

	# term = [
	#     word,
	#     prononciation,
	#     '0',
	#     definition,
	#     jp_ex + '\n    ' + en_ex
	# ]


# print(get_terms('喫茶'))
