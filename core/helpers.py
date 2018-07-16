from re import match

def is_num(value):
	return isinstance(value, int)

def check_name(name):
	if match('^.*__.*$', name): return False
	return bool(match('^[a-zA-Z0-9_]{3,400}$', name))

def translite(text):
	dictionary = {
		'а':'a','б':'b','в':'v','г':'g','д':'d',
		'е':'e','ё':'yo','ж':'zh','з':'z','и':'i',
		'й':'y','к':'k','л':'l','м':'m','н':'n',
		'о':'o','п':'p','р':'r','с':'s','т':'t',
		'у':'u','ф':'f','х':'h','ц':'c','ч':'ch',
		'ш':'sh','щ':'shch','ъ':'y','ы':'y','ь':"",
		'э':'e','ю':'yu','я':'ya'
	}
	for s in text:
		if s in dictionary:
			text = text.replace(s, dictionary[s])
	return text

def modify_text(text):
	if not(match('[a-zA-Zа-яёА-ЯЁ\_]', text[0])):
		text = 'a' + text
	return text