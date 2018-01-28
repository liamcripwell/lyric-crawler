import requests
import codecs
import lyricParsers

def mineArtists(page):
    response = requests.get(page)

    parser = lyricParsers.ArtistParser()
    print("Finding artists...")
    parser.feed(str(response.content))
    print("Number of artists found: " + str(len(parser.artists)))
    
    return parser.artists

def mineSongs(artistList):
    for artist in artistList:
        print("Mining songs for artist: " + artist[1])
        response = requests.get(artist[0])

        parser = lyricParsers.ArtistSongParser()
        parser.feed(str(response.content))

        mineLyrics(artist[1], parser.songs)

def mineLyrics(artistName, artistSongList):
    for song in artistSongList:
        print("Mining lyrics for song: " + song[1])
        response = requests.get(song[0])

        parser = lyricParsers.SongLyricParser()
        parser.feed(str(response.content))

        writeLyricsToFile(artistName, song[1], parser.lyrics)

def writeLyricsToFile(artistName, songName, lyrics):
    try:
        file = open("lyrics-data/" + artistName + "/" + songName, "w")
        print("Writing lyrics for " + songName + " to file")
    except "FileNotFoundError":
        print("Could not write lyrics for " + songName + " to file...")
        break

    file.write(lyrics)
    file.close()


artists = mineArtists('http://songmeanings.com/artist/directory/main/popular/') # top 50 artists

for artist in artists:
    # create artist directory
    directory = "lyrics-data/" + artist[1]
    if not os.path.exists(directory):
        os.makedirs(directory)

# mine and write lyrics to file
mineSongs(artists)
