import requests
from html.parser import HTMLParser

class ArtistSongParser(HTMLParser):
    indiv = False
    insong = False
    songs = []

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self.indiv = True
        if self.indiv:
            if tag == "td":
                if attrs[0][1] == "marked" or attrs[0][1] == "":
                    self.insong = True
                else:
                    self.insong = False
            #print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.indiv = False
        #if self.indiv:
            #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if self.indiv and self.insong:
            print("Encountered some data  :", data)
            self.songs.append(data)


# code 

response = requests.get('http://songmeanings.com/artist/view/songs/46/') # pink floyd
#response = requests.get('http://songmeanings.com/artist/view/songs/200/') # radiohead

parser = ArtistSongParser()
parser.feed(str(response.content))
print(len(parser.songs))