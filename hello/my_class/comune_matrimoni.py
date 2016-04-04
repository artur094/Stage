from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class Matrimoni:
    url_trento = "http://webapps.comune.trento.it/pretorioMatrimonio/ArkAccesso.do"
    url_pergine = "http://servizi.comune.pergine.tn.it/openweb/albo/albo_pretorio_matrimonio.php"
    url_arco = "http://www.servizi.comune.arco.tn.it:30080/publishing/PM/index.do"

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
                        lui += stringhe[j]
                        lui += " "
                        j+=1
                if stringhe[i] == "e":
                    j = i+1
                    while(stringhe[j] != "nata"):
                        lei += stringhe[j]
                        lei +=" "
                        j+=1
            lui = lui[:len(lui)-1]
            lei = lei[:len(lei)-1]

            sposi = {'sposo':lui, 'sposa':lei}
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

            lui = stringhe[0]
            lei = stringhe[1]

            lei = lei[1:]

            sposi = {'sposo': lui, 'sposa': lei}
            vettore_sposi.append(sposi)
        return vettore_sposi

    def pinzolo(self):
        pass

    def pergine(self):
        vettore_sposi = []

        driver = webdriver.PhantomJS()
        driver.get(self.url_pergine)

        atti = driver.find_elements_by_xpath('//tbody[@id="tabella_albo"]/tr/td[2]')

        return self.pergine_scraping(atti)

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
                        lui += string_split[j]
                        lui += " "
                        j+=1
                    j+=1
                    while string_split[j].lower()[0] != "(":
                        lei += string_split[j]
                        lei += " "
                        j+=1

                    lui = lui[:len(lui)-1]
                    lei = lei[:len(lei)-1]

                    sposi = {'sposo':lui, 'sposa':lei}
                    vettore_sposi.append(sposi)
                i+=1
        return vettore_sposi