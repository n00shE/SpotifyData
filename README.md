# SpotifyData
 
## Prerequisites
You must download your data package from Spotify, this can take 1-3 weeks.   
https://www.spotify.com/us/account/privacy/
 
## Usage
```
usage: spotifyparse.py [-h] [-s] [-o OUTFILE] [-p] path

Parses spotify data downloads

positional arguments:
  path                  Path to the folder containing StreamingHistory files

optional arguments:
  -h, --help            show this help message and exit
  -s, --song            Gather by song instead of artist
  -o OUTFILE, --outfile OUTFILE
                        Saves csv in current directory with specified name (defaults to out.csv)
  -p, --plot            Create a matplotlib bar chart of the top 20 by playtime
```

## Methods

### searchType
searchType is the way the dictionary of playtime is keyed. Anytime searchType is mentioned, 'trackName' or 'artistName' are the possible inputs.   
'trackName' gathers playtime by song and 'artistName' gathers playtime by artist.   

### create_playtime_dict()
```
create_playtime_dict(path: str, searchType: str)
```
Creates dictionary of playtime in minutes, keyed by artist or song depending on 'searchType' ('trackName' or 'artistName').  
Requires a searchType ('trackName' or 'artistName') and the path to the folder containing the *StreamingHistoryX.json* files.   

### create_csv()
```
create_csv(playtime: dict, searchType: str, file: str)
```
Creates csv with 'searchType' and playtime (in minutes) columns.   
Requires a playtime dictionary (gathered from create_playtime_dict()), a searchType (see above), and the file name/relative path to save CSV.

### plot_data()
```
plot_data(playtime: dict, searchType: str)
```
Plots top 20 with matplotlib.   
Requires a playtime dictionary and a searchType (see above).   
