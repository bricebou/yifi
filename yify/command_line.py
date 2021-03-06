from __future__ import print_function
import webbrowser
import textwrap
import requests
import sys
import urllib

try:
    import yify
    yify.browser()
except (ImportError, AttributeError):
    from yify import yify

# display movie id and title
def displayMovies( movies):
    for movie in movies:
        print( "{} {}".format(movie[0],movie[1]) )

# list Qualities
def displayQualities(y,Id):

    #default selected quality
    quality = -1

    print ("please select the quality :")
    qualities = y.getQualities(Id)

    for i in range(len(qualities)): print(i+1, " -> ", str(qualities[i]) )

    quality = int(input())

    # on bad input
    while quality < 0 and quality >= len(qualities):
        print( "bad input , please select an available quality" )
        quality = int(input())

    return quality

# detailed display of the movie
def displayDetails(movie):

    print("title   : " + str(movie["title"]))
    print("year    : " + str(movie["year"]))
    print("rating  : " + str(movie["rating"]))
    print("runtime : " + str(movie["runtime"])+" min")
    print("lang    : " + str(movie["language"]))
    print("genres  : " + ",".join( [str(genre) for genre in movie["genres"]]) )
    print("mpa     : " + movie["mpa_rating"])
    print("quality : " + movie["quality"])
    print("descr   : " + "\n\t  ".join(textwrap.wrap(" "+movie["description_intro"])))
    print("imdb_id : " + movie["imdb_code"])
    print()

# help text
def help():

    help_str = """
    usage

    \t\t-id     <number>      get the details of movie
    \t\t-s      <r or s>      sort by rating
    \t\t-l      <number>      list length (max of 50)
    \t\t-p      <number>      page number
    \t\t-f      <string>      find query term
    \t\t-m      <number>      minimum rating (max 10)

    \t\t--download            downloads the torrent file
    \t\t--magnet              downloads the movie using the magnet

    """

    print( help_str )

def execute():

    arg = sys.argv

    if '--help' in arg:
        help()
        exit()

    y = yify.browser()

    if "-id" in arg:

        # Id holds the selected id by user
        Id = ""

        # if there is a proper input
        # assign Id
        if len(arg) >= arg.index("-id")+1:
            Id = arg[arg.index("-id")+1]
        else:
            help()
            exit()

        # trailer , magnet and download flags
        # requires movie Id to be set

        # directly open default web browser
        if "--trailer" in arg:
            url = y.getTrailerUrl(Id)
            webbrowser.open(url)
            exit()

        # pass the magnet link to web browser
        # it simply redirects the address to 
        # default torrent client
        if "--magnet" in arg:

            quality = ''
            if "-q" in arg:
                
                if len(arg) >= arg.index("-q")+1:
                    quality = arg[arg.index("-q")+1]

                if quality not in y.getQualities(Id):
                    quality = displayQualities(y,Id)

            else:
                quality = displayQualities(y,Id)

            url = y.getMagnetUrl(Id,quality)
            # webbrowser.open(url)
            with open (Id+'.magnet', 'a') as f: f.write (url)
            exit()

        # similar to magnet links , pass download 
        # url to web browser to handle
        if "--download" in arg:

            quality = ""
            if "-q" in arg:
                if len(sys.arg) >= arg.index("-q")+1:
                    quality = sys.argv[sys.argv.index("-q")+1]

                if quality not in y.getQualities():
                    quality=displayQualities(y,Id);

            else:
                quality = displayQualities(y,Id)

            url = y.getTorrentUrl(Id,quality)
            # webbrowser.open(url)
            urllib.urlretrieve(url, filename=Id+".torrent")
            exit()

        # incase none of the above flags are set
        # fetch the details of the movie 
        displayDetails(y.detail(Id))

    else:

        # search movies
        if "-f" in arg:

            q=""
            if len(arg) >= arg.index("-f")+1:
                q = arg[arg.index("-f")+1]

            # range query
            if "-" not in q:
                lis = y.find(q)

                # on no movies found
                if(len(lis)==0):
                    print("sorry, no results found :(")
                else:
                    displayMovies(y.find(q))

        else:
            # 20 movies on a page
            limit = 20
            page = 1
            min_rating = 0

            # on limit set
            if "-l" in arg:

                if len(arg) >= arg.index("-l")+1:
                    limit = arg[arg.index("-l")+1]

                # on bad limit value
                try:
                    val = int(limit)
                except ValueError:
                    print ("value error with parsing the limit ")
                    print ('-'*40)

            # on page set
            if "-p" in arg:

                if len(arg) >= arg.index("-p")+1:
                    page = arg[arg.index("-p")+1]

                # on bad page value
                try:
                    val = int(page)
                except ValueError:
                    print ("value error with parsing the page")
                    print ('-'*40)

            # on minimum rating set
            if "-m" in arg:
                if len(arg) >= arg.index("-m")+1:
                    min_rating = arg[arg.index("-m")+1]

                # on bad minimum rating
                try:
                    val = int(min_rating)
                except ValueError:
                    print("Value error with parsing minimum rating")

            # on sort is set
            if "-s" in arg:

                if len(arg) >= arg.index("-s")+1:
                    sort = arg[arg.index("-s")+1]

                if sort == "r" or sort == "s" or sort == "rating" or sort == "seeds":
                    if sort == "r" or sort == "rating":
                        displayMovies(y.byRating(limit,page,min_rating))
                    else:
                        displayMovies(y.bySeeds(limit,page,min_rating))
                exit()

            # display the movies with ids
            displayMovies(y.bySeeds(limit,page,min_rating))

def main():
    try:
        execute()
    except requests.exceptions.ConnectionError as e:
        print("connection refuced by yify")
