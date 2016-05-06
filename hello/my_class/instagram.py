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
        return r.json()['data']
        #return render(request, 'social/instagram_follows.html', {'dati':r.json()})

    def search_hashtags_union(self, hashtags, token):
        dati = []
        id_controllati = []

        for hashtag in hashtags:
            # Creo dinamicamente l'url per le API
            url_tag_final = self.url_tag + hashtag + "/media/recent"
            # Inserisco il Token
            data = {
                'access_token': token
            }
            # Invio la richiesta
            r = requests.get(url_tag_final, data)

            for post in r.json()['data']:
                if post['caption']['id'] not in id_controllati:
                    id_controllati.append(post['caption']['id'])
                    dati.append(post)
        return dati

    def search_hashtags_intersect(self, hashtags, token):
        dati = []
        id_controllati = []

        for hashtag in hashtags:
            #Creo dinamicamente l'url per le API
            url_tag_final = self.url_tag + hashtag+"/media/recent"
            #Inserisco il Token
            data = {
                'access_token': token
            }
            #Invio la richiesta
            r = requests.get(url_tag_final, data)

            #Considero ogni post trovato
            for post in r.json()['data']:
                #Prendo l'ID
                id_post = post['caption']['id']

                #Controllo se l'id l'ho gia controllato
                if id_post not in id_controllati:
                    id_controllati.append(id_post)
                    all = True
                    for hash in hashtags:
                        if hash not in post['tags']:
                            all = False
                    if all:
                        dati.append(post)
                        #dati.append(url_tag_final)
                        #dati.extend(r.json()['data'])
        return dati

    def filter_hashtag(self, posts, filter_hashtags):
        dati = []

        #Per ogni post, che ho trovato con gli hashtag di ricerca, controllo se contiene hashtag non voluti
        for post in posts:
            salva = True
            for filtro in filter_hashtags:
                if filtro in post['tags']:
                    salva = False

            if salva:
                dati.append(post)
        return dati

    def search_user(self, username, token):
        url_usr_search = self.url_usr+'search'
        data = {
            'access_token':token,
            'q':username
        }

        r = requests.get(url_usr_search, data)
        if 'data' not in r.json():
            return None

        people = r.json()['data']
        for person in people:
            if person['username'] == username:
                return person

        return None

    def search_users(self, names, token):
        dati = []
        id_controllati = []
        url_usr_search = self.url_usr + 'search'

        for name in names:
            data = {
                'access_token': token,
                'q': name
            }
            r = requests.get(url_usr_search, data)

            for user in r.json()['data']:
                if user['id'] not in id_controllati:
                    id_controllati.append(user['id'])
                    dati.append(user)

        return dati

    def posts_from_username(self,username,token):
        user = self.search_user(username, token)
        if user is None:
            return []
        return self.posts(user['id'], token)

    def posts(self,id,token):
        url_user = self.url_usr+id+'/media/recent'
        data = {
            'access_token':token
        }
        r = requests.get(url_user,data)
        return r.json()['data']

    def profile(self,id,token):
        url_user = self.url_usr+id
        data = {
            'access_token':token
        }
        r = requests.get(url_user, data)
        return r.json()['data']