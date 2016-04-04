import requests

class Instagram:
    url_tag = 'https://api.instagram.com/v1/tags/'
    url_usr = 'https://api.instagram.com/v1/users/'

    def __init__(self):
        pass

    def post_hashtag(self, hashtag, token):
        #{tag-name}?access_token=ACCESS-TOKEN
        url_tag_final = self.url_tag + hashtag+"/media/recent"
        data = {
            'access_token': token
        }
        r = requests.get(url_tag_final, data)
        return r.json()
        #return render(request, 'social/instagram_follows.html', {'dati':r.json()})

    def post_hashtags(self, hashtags, token):
        dati = []
        for hashtag in hashtags:
            url_tag_final = self.url_tag + hashtag+"/media/recent"
            data = {
                'access_token': token
            }
            r = requests.get(url_tag_final, data)
            #dati.append(url_tag_final)
            dati.extend(r.json()['data'])
        return dati

    def search_user(self, name, token):
        url_usr_search = self.url_usr+'search'
        data = {
            'access_token':token,
            'q':name
        }
        r = requests.get(url_usr_search, data)
        return r.json()['data']

    def posts(self,id,token):
        url_user = self.url_usr+id+'/media/recent'
        data = {
            'access_token':token
        }
        r = requests.get(url_user,data)
        return r.json()['data']