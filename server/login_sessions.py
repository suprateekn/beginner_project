import  requests
	
def login_fn():
	
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
	login_data = {
		'email' : "supra@supra.com",
		'password' : 'supra'
	}
	with requests.Session() as s:
		print('ghjk')
		url = "http://localhost:8004/home"
		r = s.post(url, data = login_data)
		print(r)
# login_fn()