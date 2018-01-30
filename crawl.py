import requests
import codecs
import lyricParsers
import os

def mineArtists(page):
    print("Finding artists...")
    response = requests.get(page)
    parser = lyricParsers.ArtistParser()
    parser.feed(str(response.content))
    print("Number of artists found: " + str(len(parser.artists)))
    
    return parser.artists

def mineSongs(artistList):
    noSongs = 0
    for artist in artistList:
        # create artist directory
        createDirectory(artist[1])

        print("Mining songs for artist: " + artist[1])
        response = requests.get(artist[0])

        parser = lyricParsers.ArtistSongParser()
        parser.feed(str(response.content))

        mineLyrics(artist[1], parser.songs[noSongs:])
        noSongs = noSongs + len(parser.songs[noSongs:])

def mineLyrics(artistName, artistSongList):
    for song in artistSongList:
        print("Mining lyrics for song: " + song[1])
        response = requests.get(song[0])

        parser = lyricParsers.SongLyricParser()
        parser.feed(str(response.content))

        writeLyricsToFile(artistName, song[1], parser.lyrics)

def writeLyricsToFile(artistName, songName, lyrics):
    try:
        if len(songName) > 100:
            songName = "song-name-too-long"
        
        file = open("lyrics-data/" + artistName + "/" + songName, "w")
        print("Writing lyrics for " + songName + " to file")
        file.write(lyrics)
        file.close()
    except ("FileNotFoundError"):
        print("Could not write lyrics for " + songName + " to file...")

def createDirectory(artistName):
    directory = "lyrics-data/" + artistName
    if not os.path.exists(directory):
        os.makedirs(directory)


# collect list of artists and their page links
artists = mineArtists('http://songmeanings.com/artist/directory/main/popular/') # top 50 artists

# mine and write lyrics to file
mineSongs(artists)
