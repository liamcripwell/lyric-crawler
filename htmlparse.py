import requests
import codecs
import lyricParsers

def mineSongs(artistName, artistSongList):
    for song in artistSongList:
        print("Mining lyrics for song: " + song[1])
        try:
            file = open("lyrics-data/" + artistName + "/" + song[1], "w") 
        except "FileNotFoundError":
            break
        
        response = requests.get(song[0])

        songParser = SongLyricParser()
        songParser.feed(str(response.content))

        file.write(songParser.lyrics)
        file.close()


response = requests.get('http://songmeanings.com/artist/directory/main/popular/') # top 50 artists

# parser = ArtistSongParser()
# print("Finding songs for artist...")
# parser.feed(str(response.content))
# print("Number of songs found: " + str(len(parser.songs)))

parser = lyricParsers.ArtistParser()
print("Finding artists...")
parser.feed(str(response.content))
print("Number of artists found: " + str(len(parser.artists)))
print([x[1] for x in parser.artists])

# import nltk

# with open('lyrics-data/pink-floyd/A Great Day for Freedom.txt', 'r') as myfile:
#     data=myfile.read()

# words = nltk.word_tokenize(data)
# print(words)