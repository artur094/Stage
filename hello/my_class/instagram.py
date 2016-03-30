import requests

class Instagram:
    url_tag = 'https://api.instagram.com/v1/tags/'

    def __init__(self):
        pass

    def post_hashtag(self, hashtag, token):
        data = {
            'q': hashtag,
            'access_token': token
        }
        r = requests.get(self.url_tag+'search'+hashtag,data)
        return r.json()
        #return render(request, 'social/instagram_follows.html', {'dati':r.json()})