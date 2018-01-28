from html.parser import HTMLParser

# Parse lyrics from a song page
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
            self.lyrics = self.lyrics + data.encode().decode('unicode_escape')

# Parse list of artists from an artist list page
class ArtistParser(HTMLParser):
    indiv = False
    inartist = False
    currentlink = ""
    currentartist = ""
    artists = []

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self.indiv = True
        if self.indiv:
            if tag == "td":
                if attrs[0][1] == "95%":
                    self.inartist = True
                else:
                    self.inartist = False
            if tag == "a" and self.inartist:
                self.currentlink = attrs[0][1]
                self.currentartist = attrs[1][1].replace('&', 'and').replace(" ", "-").lower()
                self.artists.append(('http:' + self.currentlink, self.currentartist.replace("/", " ")))

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.indiv = False

# Parse list of songs from an artist page
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

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.indiv = False

    def handle_data(self, data):
        if self.indiv and self.insong:
            self.currenttitle = str(data)
            self.songs.append(('http:' + self.currentlink, self.currenttitle.replace("/", " ")))