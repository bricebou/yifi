## yify on commandline

Command line tool for browsing and downloading the yts torrents 

#### Installation
    
    pip install yify

##### options 

    -id <number>      get the details of movie
    -s  <r or s>      sort by rating 
    -l  <number>      list length (max of 50)
    -p  <number>      page number
    -f  <string>      find query term
    -m  <number>      minimum rating (max 10)

    --download        downloads the torrent file
    --magnet          downloads the movie using the magnet
    --trailer         watch the trailer on youtube
 
##### examples
first simply get the list top seeded and latest movie torrent by
        
        yify

the output has 2 columns **movie_id** and **movie_title**

if you want the further page results go for 
    
        yify -p 2 
        yify -p 5

once you have the id you can view the details of the movie by simply
    
        yify -id movie_id
    
to search the movie in yify database 
    
        yify -f <move_name>
   
and when you want to download the movie go with
    
        yify -id <movie_id> --download

this would download the **.torrent** file 

to download the movie using the magnet do
    
        yify -id <movie_id> --magnet
