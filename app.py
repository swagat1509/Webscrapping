import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

app = FastAPI()

class Scrapping(BaseModel):
    
    url: str
    


class TextExtraction:
    """
    Class to extract the news articles text from the body of the news article.

    """
    def __init__(self, url):
        self.url = url

    def getdata(self,url):
        r = requests.get(url)
        return r.text

    def extract_header(self):
        htmldata = self.getdata(self.url)
        soup = BeautifulSoup(htmldata, 'html.parser')
        header = soup.find("h1").get_text()
        return header


    def extract_body(self):
        htmldata = self.getdata(self.url)
        soup = BeautifulSoup(htmldata, 'html.parser')
        body_list = []
        for data in soup.find_all("p"):
            body_list.append(data.get_text())
        body = ".".join(body_list)
        body=body.replace("\n","")

        return body


"""
The following api is to extract the title and the body of any of the url given
""" 
@app.post('/getarticle')
def news_articles(getarticles: Scrapping):
    
    url = getarticles.url
    te = TextExtraction(url)
    text_header = te.extract_header()
    text_body = te.extract_body()

    # returns the title, descritpion and the body of the news
    return {'title':text_header,
           'body':text_body}





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)

