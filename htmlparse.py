import requests
from html.parser import HTMLParser

class SongLyricParser(HTMLParser):
    indiv = False
    lyrics = ""

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if attrs and attrs[0][1] == "holder lyric-box":
                self.indiv = True
            else:
                self.indiv = False

    def handle_data(self, data):
        if self.indiv:
            self.lyrics = self.lyrics + data


class ArtistSongParser(HTMLParser):
    indiv = False
    insong = False
    currentlink = ""
    currenttitle = ""
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
            if tag == "a" and self.insong:
                self.currentlink = attrs[2][1]
            #print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.indiv = False
        #if self.indiv:
            #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if self.indiv and self.insong:
            self.currenttitle = data
            self.songs.append((self.currentlink, self.currenttitle))


# code 

response = requests.get('http://songmeanings.com/artist/view/songs/46/') # pink floyd
song = requests.get('http://songmeanings.com/songs/view/2880/')
#response = requests.get('http://songmeanings.com/artist/view/songs/200/') # radiohead

parser = ArtistSongParser()
parser.feed(str(response.content))
print(len(parser.songs))

parser = SongLyricParser()
parser.feed(str(song.content))
print(parser.lyrics)