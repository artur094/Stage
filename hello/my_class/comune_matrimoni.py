from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from ..models import Coppia

class Matrimoni:
    url_trento = "http://webapps.comune.trento.it/pretorioMatrimonio/ArkAccesso.do"
    url_pergine = "http://servizi.comune.pergine.tn.it/openweb/albo/albo_pretorio_matrimonio.php"
    url_arco = "http://www.servizi.comune.arco.tn.it:30080/publishing/PM/index.do"
    url_rovereto = "http://www2.comune.rovereto.tn.it/iride/extra/cerca_albo/"
    url_pinzolo = "http://www.comune.pinzolo.tn.it/homepage"

    def __init__(self):
        pass

    def trento(self):

        vettore_sposi = []

        driver = webdriver.PhantomJS()
        driver.get(self.url_trento)

        driver.find_element_by_xpath('//form[@id="menuContextForm"]//tr[2]/td/a').click()

        next = True

        while next:
            next = False

            atti = driver.find_elements_by_xpath("//tr[@class='td-celladark' or @class='td-cellalight']/td[3]")

            vettore_sposi.extend(self.trento_scraping(atti))

            try:
                succ = driver.find_element_by_xpath("//a[@class='pagerSucc']")
                succ.click()
                next = True
            except NoSuchElementException:
                pass

        driver.quit()
        return vettore_sposi

    def trento_scraping(self, atti):
        """
        Given an array of string which contains the message of mariage, this function return an array dict with key 'sposo' and 'sposa'
        and the value of these is the name of the girl and of the boy, scraped from the text
        @type atti: list
        @param atti: a list of string that contains the text of the mariage
        :return: an array dict which contains the name of him and the name of her
        """
        vettore_sposi = []
        for atto in atti:
            lui = ""
            lei = ""
            stringhe = atto.text.split(" ")

            for i in range(0, len(stringhe)):
                if stringhe[i] == "tra":
                    j = i+1
                    while(stringhe[j] != "nato"):
                        lui += stringhe[j].capitalize()
                        lui += " "
                        j+=1
                if stringhe[i] == "e":
                    j = i+1
                    while(stringhe[j] != "nata"):
                        lei += stringhe[j].capitalize()
                        lei +=" "
                        j+=1
            lui = lui[:len(lui)-1]
            lei = lei[:len(lei)-1]

            #sposi = {'sposo':lui, 'sposa':lei}

            sposi = Coppia.add_coppia(lui,lei,'Trento')

            vettore_sposi.append(sposi)
        return vettore_sposi

    def arco(self):
        vettore_sposi = []

        driver = webdriver.PhantomJS()
        driver.get(self.url_arco)

        #next = True

        #while next:
        #    next = False
        atti = driver.find_elements_by_xpath('//table[@id="documentList"]/tbody//td[3]')

        vettore_sposi.extend(self.arco_scraping(atti))


            #try:
            #    succ = driver.find_element_by_xpath("//a[@class='pagerSucc']")
            #    succ.click()
            #    next = True
            #except NoSuchElementException:
            #    pass

        driver.quit()
        return vettore_sposi

    def arco_scraping(self,atti):
        vettore_sposi = []
        for atto in atti:
            lui = ""
            lei = ""
            stringhe = atto.text.split(",")

            for str in stringhe[0].split(' '):
                lui+=' '+str.capitalize()

            for str in stringhe[1].split(' '):
                if str != '':
                    lei+=' '+str.capitalize()

            lui = lui[1:]
            lei = lei[1:]

            #sposi = {'sposo': lui, 'sposa': lei}
            sposi = Coppia.add_coppia(lui,lei,'Arco')

            vettore_sposi.append(sposi)
        return vettore_sposi

    def pinzolo(self):

        vettore_sposi = []

        driver = webdriver.PhantomJS()
        driver.get(self.url_pinzolo)

        # I am on the page of the district, and I click the link for 'Pubblicazioni di matrimonio'
        link = driver.find_element_by_xpath('//table[@class="risultati"]/tbody/tr[1]/td[1]/h2[3]/a').get_attribute('href')

        driver.get(link)

        # If I am right, now I should be on the page which I'm looking for
        # I could scrape names from this page, but I am not sure if they put the full name or they cut it with dots...
        vett_link = driver.find_elements_by_xpath('//table[@id="table-pubblicazioni-matrimonio"]/tbody/tr')



        for x in vett_link:
            atto = x.text.split('\n')[2]
            vettore_sposi.append(self.pinzolo_scraping(atto))

        driver.quit()
        return vettore_sposi

    def pinzolo_scraping(self, atto):

        vett_str = atto.split(' ')
        lui = ""
        lei = ""

        i = 3
        while vett_str[i] != '-':
            lei += vett_str[i] + ' '
            i+=1
        i+=1
        while i < len(vett_str) and vett_str[i] != 'dal':
            lui += vett_str[i] + ' '
            i+=1

        lui = lui[:len(lui)-1]
        lei = lei[:len(lui)-1]

        sposi = Coppia.add_coppia(lui, lei, 'Pinzolo')

        return sposi

    def rovereto(self):
        driver = webdriver.PhantomJS()
        driver.get(self.url_rovereto)

        if len(driver.find_elements_by_xpath('//table[@id="tblgrid"]')) <= 0:
            #non sono sulla pagina giusta, devo riempire il form
            for option in driver.find_elements_by_xpath('//select[@id="id_ente"]/option'):
                if option.get_attribute('value').lower() == 'comunerovereto':
                    option.click()

            for option in driver.find_elements_by_xpath('//select[@id="id_tipo_atto"]/option'):
                if option.get_attribute('value').lower() == 'pubblicazione di matrimonio':
                    option.click()

            driver.find_element_by_xpath('//form[@class="well form-search"]//button[@class="btn btn-primary"]').click()

        atti = driver.find_elements_by_xpath('//table[@id="tblgrid"]/tbody/tr/td[4]')

        ret = self.rovereto_scraping(atti)

        driver.quit()

        return ret;

    def rovereto_scraping(self, atti):
        vettore_sposi = []

        for atto in atti:
            lui = ""
            lei = ""

            string_split = atto.get_attribute('title').split(" ")

            i = 3
            next = True
            while i < len(string_split) and next:
                if string_split[i].lower() == "di":
                    next = False
                    j = i + 1
                    while string_split[j].lower() != "e":
                        lui += string_split[j].capitalize()
                        lui += " "
                        j += 1
                    j += 1
                    while j < len(string_split) and string_split[j].lower() != "su":
                        lei += string_split[j].capitalize()
                        lei += " "
                        j += 1

                    lui = lui[:len(lui) - 1]
                    lei = lei[:len(lei) - 1]

                    # sposi = {'sposo':lui, 'sposa':lei}
                    sposi = Coppia.add_coppia(lui, lei, 'Rovereto')

                    vettore_sposi.append(sposi)
                i += 1
        return vettore_sposi

    def pergine(self):
        vettore_sposi = []

        driver = webdriver.PhantomJS()
        driver.get(self.url_pergine)

        atti = driver.find_elements_by_xpath('//tbody[@id="tabella_albo"]/tr/td[2]')

        ret = self.pergine_scraping(atti)

        driver.quit()

        return ret

    def pergine_scraping(self,atti):
        vettore_sposi = []

        for atto in atti:
            lui = ""
            lei = ""

            string_split = atto.text.split(" ")

            i=0
            next = True
            while i<len(string_split) and next:
                if string_split[i].lower() == "matrimonio:":
                    next = False
                    j = i+1
                    while string_split[j].lower() != "e":
                        lui += string_split[j].capitalize()
                        lui += " "
                        j+=1
                    j+=1
                    while string_split[j].lower()[0] != "(":
                        lei += string_split[j].capitalize()
                        lei += " "
                        j+=1

                    lui = lui[:len(lui)-1]
                    lei = lei[:len(lei)-1]

                    #sposi = {'sposo':lui, 'sposa':lei}
                    sposi = Coppia.add_coppia(lui,lei,'Pergine')

                    vettore_sposi.append(sposi)
                i+=1
        return vettore_sposi