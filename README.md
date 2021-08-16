﻿# SpotifyData
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

