from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import wikipedia
import re
import random
import os
# space = requests.get('https://apod.nasa.gov/apod/random_apod.html').text

# random = requests.get('https://www.getrandomthings.com/list-food.php').text
# print(random)
# reslist > div > div:nth-child(1)

# test = rsoup.prettify()
# f.write(test)


class Poem:
    defaultrequests = {'num': '6', 'add': 'address', 'unique':'true'}
    
    def __init__(self, randomUrl, typeOfRequest):
        self.randomUrl = randomUrl
        self.request = requests.post(randomUrl, data = self.defaultrequests)
        self.soup = BeautifulSoup(self.request.text, 'html5lib')
        self.typeOfRequest = typeOfRequest

    def getValidLink(self, link):
        try: 
            summary = wikipedia.summary(link)
            return link
        except wikipedia.exceptions.DisambiguationError as err:
            if err.options:
                title = err.options[0]
            else:
                title = "Chicken Noodle Soup"
        except wikipedia.exceptions.PageError:
            title = "Chicken Noodle Soup"
        
        return title

    def getTitle(self):
        if(self.typeOfRequest == 'food'):
            title = self.soup.select('div > div:nth-child(1)')[0].contents[3]
        elif(self.typeOfRequest == 'river'):
            title = self.soup.select('div > div:nth-child(1)')[0].contents[3].get_text()
        elif(self.typeOfRequest == 'noun'):
            title = self.soup.select('div > div:nth-child(1)')[0].get_text()
        elif(self.typeOfRequest == 'movie'):
            title = self.soup.select('div > div:nth-child(1)')[0].contents[2]
        else: 
            title = self.soup.select('div > div:nth-child(1)')[0].contents[2]


        self.summary = wikipedia.summary(self.getValidLink(title))
        self.title = title
        self.page = wikipedia.page(self.title)
        return self.title

    def getFirstSentence(self): 
        summary = wikipedia.summary(self.title) 
        regexmatches = re.findall("[A-Z]+[^(.!?)]*[.!?]", summary)

        if not regexmatches:
            return ""
        else:
            return random.choice(regexmatches)
                
    def getImage(self):
        image = self.page.images[0]
        return image

    def getSecondSentence(self):
        self.title2 = self.getValidLink(random.choice(self.page.links))

        summary = wikipedia.summary(self.title2)  
        self.page2 = wikipedia.page(self.title2)

        regexmatches = re.findall("[A-Z]+[^(.!?)]*[.!?]", summary)

        if not regexmatches:
            return ""
        else:
            return random.choice(regexmatches)
    
    def getThirdSentence(self):
        self.title3 = self.getValidLink(random.choice(self.page2.links))

        summary = wikipedia.summary(self.title3)  
        self.pag3 = wikipedia.page(self.title3)
        
        regexmatches = re.findall("[A-Z]+[^(.!?)]*[.!?]", summary)

        if not regexmatches:
            return ""
        else:
            return random.choice(regexmatches)

    def getPoem(self): 
        return self.getFirstSentence() + "\n" + self.getSecondSentence() + "\n" + self.getThirdSentence()
ship = wikipedia.page("MV Explorer (1969)")

app = Flask(__name__)
@app.route('/')
def index():
    p1 = Poem('https://www.getrandomthings.com/data/list-food.php', 'food')

    title = p1.getTitle()
    f1 = p1.getPoem()
    image = p1.getImage()

    return render_template('index.html',**locals())

@app.route('/second.html')
def second():
    p2 = Poem('https://www.getrandomthings.com/data/list-rivers.php', 'river')

    title2 = p2.getTitle()
    s1 = p2.getPoem()
    image2 = p2.getImage()

    return render_template('/second.html',**locals())

@app.route('/third.html')
def third():
    p3 = Poem('https://www.getrandomthings.com/data/random-nouns.php', 'noun')

    title3 = p3.getTitle()
    t1 = p3.getPoem()
    image3 = p3.getImage()
    
    return render_template('/third.html',**locals())

@app.route('/fourth.html')
def fourth():
    p4 = Poem('https://www.getrandomthings.com/data/top-moives.php', 'movie')

    title4 = p4.getTitle()
    fo1 = p4.getPoem()
    image4 = p4.getImage()

    return render_template('/fourth.html',**locals())

@app.route('/fifth.html')
def fifth():
    p5 = Poem('https://www.getrandomthings.com/data/list-tv-shows.php', 'tv')

    title5 = p5.getTitle()
    fi5 = p5.getPoem()
    imag5 = p5.getImage()

    return render_template('/fifth.html',**locals())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)