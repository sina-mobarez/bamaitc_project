import requests




def send_sms(receptor, token):
    key = "	D1vHDvgSNI6f0lQm8XdVYdsnrv5Sl5yIp-h4HaLJPyo="
    pat = '27568ncxwxtio7m'
    url = f'http://ippanel.com:8080/?apikey={key}&pid={pat}&fnum=3000505&tnum=0{receptor}&p1=code&v1={token}'

    response = requests.get(url)
    print(response)