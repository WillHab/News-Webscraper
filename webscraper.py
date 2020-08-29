from flask import Flask, render_template, url_for, redirect
import requests 
from bs4 import BeautifulSoup
from time import sleep

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("homepage.html", title="Home")

@app.route('/NYT', methods=['GET', 'POST'])
def NYT():
    url = "https://www.nytimes.com/"
    site = requests.get("https://www.nytimes.com/")
    site_content = site.content
    soup = BeautifulSoup(site_content, 'html.parser')
    headlines = []
    h2_tags = soup.find_all("h2")
    for h2_tag in h2_tags:
        a_tag = h2_tag.find("span")
        try:
           headline = a_tag.text
           headlines.append(headline)
        except AttributeError:
            pass
    return render_template("homepage.html", headlines=headlines, title="NYT Headlines", url=url)

@app.route('/WashPost', methods=['GET', 'POST'])
def WP():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    url = "https://www.washingtonpost.com/"
    site = requests.get("https://www.washingtonpost.com/", headers=headers)
    site_content = site.content
    soup = BeautifulSoup(site_content, 'html.parser')
    headlines = []
    links = soup.find_all("a", {"data-pb-field": "headlines.basic"})
    for link in links:
        try:
           headline = link.text
           headlines.append(headline)
        except AttributeError:
            pass
        if len(headlines) > 4:
            break
        
    return render_template("homepage.html", headlines=headlines, title="WP Headlines", url=url)

@app.route('/guardian', methods=['GET', 'POST'])
def guardian():
    url = "https://www.theguardian.com/international"
    site = requests.get("https://www.theguardian.com/international")
    site_content = site.content
    soup = BeautifulSoup(site_content, 'html.parser')
    main = soup.find_all("div", class_="fc-item__container")
    headlines = []
    for links in main:
        link = links.find("a", {"data-link-name":"article"})
        headline = link.text
        headlines.append(headline)
        if len(headlines) > 4:
            break
    
    return render_template("homepage.html", headlines=headlines, title="Guardian Headlines", url=url)

@app.route('/WSJ', methods=['GET', 'POST'])
def WSJ():
    url = "https://www.wsj.com/"
    headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}
    site = requests.get("https://www.wsj.com/", headers=headers)
    site_content = site.content
    soup = BeautifulSoup(site_content, 'html.parser')
    h_tags = soup.find_all("h3")
    print(h_tags)
    headlines = []
    for links in h_tags:
        link = links.find("a")
        headline = link.text
        headlines.append(headline)
        if len(headlines) > 4:
            break
    return render_template("homepage.html", headlines=headlines, title="WSJ Headlines", url=url)

if __name__ == "__main__":
    app.run(debug=True)