# SpotifyData
 
## Prerequisites
You must download your data package from Spotify, this can take 1-4 weeks for Spotify to deliver.   
This program supports both the account data download and the extended history download.   
https://www.spotify.com/us/account/privacy/
 
## Usage
```
usage: spotifyparse.py [-h] [-s] [-e] [-i] [-o OUTFILE] [-d] [-n PLOTNUM] path

Parses and charts Spotify data downloads

positional arguments:
  path                  Path to the folder containing json files

optional arguments:
  -h, --help            show this help message and exit
  -s, --song            Gather by song instead of artist
  -e, --extended        Use the lifetime streaming history files
  -i, --include-podcasts
                        Include podcast data, only works on extended data
  -o OUTFILE, --outfile OUTFILE
                        Saves csv in current directory with specified name
  -d, --dark-mode       Plot with a dark background
  -n PLOTNUM, --plot-num PLOTNUM
                        Number of items to plot
```

## SpotifyData Class
```
SpotifyData(path: str, searchType: str, extended=False, includePodcasts=False, darkMode=False)
```
The class requires two arguments with three optionals.   
Class must be instantiated before using the methods below.    
### Required Arguments
The path to the folder with the *StreamingHistoryX.json* files or the the *endsong_X.json* files.   
The search type which is either *'trackName'* or *'artistName'*.   
### Optional Arguments
Boolean if the data is from the extended streaming history download.  (The defualt is the account data download)   
Boolean to include podcasts. (Only works with the extended stream history)   
Boolean to make the chart dark mode.   

### create_playtime_dict()
```
@property
SpotifyData.create_playtime_dict()
```
Creates dictionary of playtime in minutes, keyed by artist or song name depending on the search type.   

### create_csv()
```
SpotifyData.create_csv(file: str)
```
Creates csv with playtime (in minutes) by artist or song name.   
Requires the file name/relative path to save CSV.

### plot_data()
```
SpotifyData.plot_data(plotNum: int)
```
Plots top plotNum artists or song names with matplotlib.   
Requires the number of items to plot.
