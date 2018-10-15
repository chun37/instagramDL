# -*- coding: utf-8 -*-
import bs4
import requests
import json
host = "https://www.instagram.com/"
post = host + "p/"


def getImageURLsfromId(UserId):
    r = requests.get(host + UserId)
    soup = bs4.BeautifulSoup(r.content, "lxml")
    data = json.loads(soup.find_all("script")[3].text[21:-1])
    posts = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
    imageURLlist = list(map(lambda x: post + x["node"]["shortcode"], posts))
    map(getImageURL, imageURLlist)


def getImageURL(PostUrl):
    r = requests.get(PostUrl)
    soup = bs4.BeautifulSoup(r.content, "lxml")
    data = json.loads(soup.find_all("script")[3].text[21:-1])
    try:
        for image in data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]:
            print(image["node"]["display_resources"][-1]["src"])
    except:
        print(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_resources"][-1]["src"])

IDorURL = input("PostURL>>>")
if IDorURL.startswith("https://"):
    getImageURL(IDorURL)
else:
    getImageURLsfromId(IDorURL)
