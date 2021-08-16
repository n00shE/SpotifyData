"""
Ryan Blanchard
rmblanch@uci.edu
Spotify data download parser
"""


import json
import argparse
import csv
import os
#import time

def create_playtime_dict(path: str, searchType: str):
    '''
    Creates dictionary of playtime in minutes, keyed by artist or song depending on 'searchType' ('trackName' or 'artistName').  
    Requires a search type ('trackName' or 'artistName') and the path to the folder containing the StreamingHistoryX.json files.  
    '''
    if searchType != 'trackName' and searchType != 'artistName':
        print("ERROR: Invalid search type.")
        quit()
    playtime = {}
    for jsonFile in os.scandir(path):
        if "StreamingHistory" in jsonFile.path:
            print('Opening ' + jsonFile.path + '...')
            with open(jsonFile.path, encoding="utf8") as file:
                songList = json.load(file)
                for song in songList:
                    #if '$' in song[searchType]: continue
                    try:
                        playtime[song[searchType]] += song['msPlayed'] / 60000 # divided to convert ms to minutes.
                    except KeyError:
                        playtime[song[searchType]] = song['msPlayed'] / 60000
    return dict(sorted(playtime.items(), key=lambda item: item[1], reverse=True))

def create_csv(playtime: dict, searchType: str, file: str):
    '''
    Creates csv with 'searchType' and playtime (in minutes) columns.
    Requires a playtime dictionary (gathered from create_playtime_dict()), a searchType (see above), and the file name/relative path to save CSV.
    '''
    file = "out.csv"
    with open(file, 'w', newline="\n", encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([searchType, 'playtime(m)'])
        for k, v in playtime.items():
            writer.writerow([k, v])
    print(f'Finished writing csv file to: {file}')

def plot_data(playtime: dict, searchType: str):
    '''
    Plots top 20 with matplotlib.
    Requires a playtime dictionary and a searchType (see above).
    '''
    import matplotlib.pyplot as plt
    l = dict(list(playtime.items())[:20])
    #print(l)
    plt.style.use('ggplot')
    x_pos = [i for i, _ in enumerate(l.keys())]

    plt.bar(x_pos, l.values(), color='blue')
    #plt.xlabel(searchType)
    plt.ylabel("Minutes")
    plt.title(f"Playtime by {searchType}")

    plt.xticks(x_pos, l.keys(),
    rotation=45, 
    horizontalalignment='right',
    fontweight='light',
    fontsize='small')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='spotifyparse.py',
                                    description='Parses spotify data downloads')
    parser.add_argument('path', action='store', type=str, help="Path to the folder containing StreamingHistory files")
    parser.add_argument('-s','--song', action='store_true', help="Gather by song instead of artist")
    parser.add_argument('-o','--outfile', action='store', default='out.csv', help="Saves csv in current directory with specified name (defaults to out.csv)")
    parser.add_argument('-p','--plot', action='store_true', help="Create a matplotlib bar chart of the top 20 by playtime")


    args = parser.parse_args()
    if args.song:
        searchType = 'trackName'
    else:
        searchType = 'artistName'
    playtime = create_playtime_dict(args.path, searchType)
    create_csv(playtime, searchType, args.outfile)
    if args.plot:
        plot_data(playtime, searchType)