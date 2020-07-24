import requests
from bs4 import BeautifulSoup
import json
import sys

APP_ID = '58b39da6'
APP_KEY = '4d8d8a83f3c4b1ba0524c783beb9de2d'

def pos_to_abbr(x):
	link = {
		'noun': 'n.',
		'verb': 'v.',
		'adjective': 'adj.',
		'adverb': 'adv.'
	}
	if x in link:
		return link[x]
	else: return x

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def unique(L):
	result = []

	for x in L:
		if x not in result:
			result.append(x)

	return result 

def get_terms(query, manual_tag):
	language = 'en-gb'
	url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + query.lower()
	r = requests.get(url, headers={"APP_ID": APP_ID, "APP_KEY": APP_KEY})

	response = json.loads(r.text)

	if 'results' in response:
		data = response['results']

		terms = []
		for d in data:
			# if manual_tag:

			# here for multiple search results
			word = d['word']
			lexical_entries = d['lexicalEntries']
			text = ''
			pronunciation_group = []
			part_of_speech_group = []

			for lexical_entry in lexical_entries:
				entries = lexical_entry['entries']
				part_of_speech = pos_to_abbr(lexical_entry['lexicalCategory']['id'])
				part_of_speech_group.append(part_of_speech)
				text += '<p><b>{}</b></p>'.format(part_of_speech)

				for entry in entries:
					pronunciations = entry['pronunciations']
					senses = entry['senses']
					for pronunciation in pronunciations:
						pronunciation_group.append(pronunciation['phoneticSpelling'])

					definitions_w_examples = ''
					sense_idx = 1
					for sense in senses:
						definitions_w_examples += '<p>'

						
						has_definition = 'definitions' in sense
						has_example = 'examples' in sense

						examples = None if not has_example else sense['examples']
						definitions = None if not has_definition else sense['definitions']

						if has_definition:
							for definition in definitions:
								definitions_w_examples += '{}. {}<br />'.format(sense_idx, definition)
								sense_idx += 1
						if has_example:
							for example in examples:
								definitions_w_examples += 'e.g. {}<br />'.format(example['text'])
						definitions_w_examples += '</p>'

					text += definitions_w_examples 

			term = [
				word,
				', '.join(unique(pronunciation_group)),
				', '.join(unique(part_of_speech_group)),
				text
			]
			
			terms.append(term)

		# print(terms)

		return terms
	else:
		eprint(query)

	return []

	# if response['meta']['status'] == 200:
	# 	data = response['data']
	# 	candidates = [d['slug'] for d in data]
	# 	candidates_cnt = len(candidates)
	# 	hint = ' '.join(['[{}] {}'.format('x' if i == 0 else i+1, candidates[i]) for i in range(candidates_cnt)])

	# 	if manual_tag:
	# 		print(hint, end=" ? ")
	# 		choice_raw = input()

	# 	pool = []
	# 	terms = []

	# 	if not manual_tag:
	# 		pool.append(data[0])
	# 	else:
	# 		if choice_raw == '':
	# 			pool.append(data[0])
	# 		else:
	# 			for c in choice_raw:
	# 				if c == '+':
	# 					pool.append(data[0])
	# 				elif int(c) <= candidates_cnt:
	# 					pool.append(data[int(c)-1])  

	# 	for p in pool:
	# 		word = p['slug']
	# 		prononciation = p['japanese'][0]['reading']
	# 		senses = p['senses']
	# 		definitions = []
	# 		part_of_speeches = []
	# 		for sense in senses:
	# 			definitions.append(', '.join(sense['english_definitions']))
	# 			part_of_speeches += sense['parts_of_speech']
	# 		# part_of_speeches.unique()

	# 		sentences_r = requests.get('https://jisho.org/search/{}%20%23sentences'.format(word))
	# 		sentences_soup = BeautifulSoup(sentences_r.text, 'html.parser')

	# 		count = 0
	# 		examples = ''
	# 		for item in sentences_soup.find_all(attrs={'class': 'sentence_content'}):
	# 			jp_text = ''
	# 			for part in item.ul.contents:
	# 				if part.name:
	# 					furigana = part.find(attrs={'class': 'furigana'})
	# 					original = part.find(attrs={'class': 'unlinked'}).string

	# 					if furigana:
	# 						jp_text += '<ruby>{}<rt>{}</rt></ruby>'.format(original, furigana.string)
	# 					else:
	# 						jp_text += original
	# 				else:
	# 					jp_text += str(part)

	# 			en_text = item.find(attrs={'class': 'english'}).string
	# 			example = '<p>'+jp_text.strip()+'<br />'+en_text+'</p>'

	# 			examples += example

	# 			count += 1
	# 			if count > 2: break

	# 		terms.append([
	# 			word,
	# 			'' if word == prononciation else prononciation,
	# 			'0',
	# 			'<br />'.join(['{}. '.format(i+1) + definitions[i] for i in range(len(definitions))]),
	# 			examples
	# 		])

		# return terms
	return []
