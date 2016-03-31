import requests

class Instagram:
    url_tag = 'https://api.instagram.com/v1/tags/'

    def __init__(self):
        pass

    def post_hashtag(self, hashtag, token):
        #{tag-name}?access_token=ACCESS-TOKEN
        url_tag_final = self.url_tag + hashtag
        data = {
            'access_token': token
        }
        r = requests.get(url_tag_final, data)
        return r.json()
        #return render(request, 'social/instagram_follows.html', {'dati':r.json()})
