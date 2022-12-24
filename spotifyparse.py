"""
Ryan Blanchard
Spotify data download parser
"""

import json
import argparse
import csv
import os
from datetime import datetime
from collections import OrderedDict, defaultdict
from itertools import islice

class SpotifyData:
    def __init__(self, path: str, searchType: str, extended=False, includePodcasts=False, darkMode=False):
        self.path = path
        self.searchType = searchType
        self.friendlySearchType = searchType
        self.extended = extended
        self.includePodcasts = includePodcasts
        self.darkMode = darkMode
        self.playtime = None
        self.newest = None
        self.oldest = None
        if searchType != 'trackName' and searchType != 'artistName':
            print("ERROR: Invalid search type.")
            quit(1)
        if extended:
            if searchType == 'trackName':
                self.searchType = 'master_metadata_track_name'
            elif searchType == 'artistName':
                self.searchType = 'master_metadata_album_artist_name'

    @property
    def playtime_dict(self):
        '''
        Creates dictionary of playtime in minutes, keyed by artist or song depending on 'searchType' ('trackName' or 'artistName').  
        Requires a search type ('trackName' or 'artistName') and the path to the folder containing the StreamingHistoryX.json files.  
        '''
        if self.playtime:
            return self.playtime
        self.playtime = defaultdict(int)
        if self.extended:
            self.parse_extended_data_files()
        else:
            self.parse_account_data_files()
        self.playtime = OrderedDict(sorted(self.playtime.items(), key=lambda item: item[1], reverse=True))
        return self.playtime

    def parse_extended_data_files(self):
        '''
        Parse the lifetime streaming data into a playtime dictionary
        '''
        files = 0
        for jsonFile in os.scandir(self.path):
            if 'endsong' in jsonFile.path and 'json' in jsonFile.path:
                print('Opening ' + jsonFile.path + '...')
                files += 1
                with open(jsonFile.path, encoding="utf8") as file:
                    songList = json.load(file)
                for song in songList:
                    self.find_date_range(song['ts'])
                    if song[self.searchType] == None:
                        if self.includePodcasts:
                            if self.friendlySearchType == 'artistName':
                                self.playtime[song['episode_show_name']] += song['ms_played'] / 60000 # divided to convert ms to minutes.
                            else:
                                self.playtime[song['episode_name']] += song['ms_played'] / 60000 # divided to convert ms to minutes.
                    else:
                        self.playtime[song[self.searchType]] += song['ms_played'] / 60000 # divided to convert ms to minutes.
        if files == 0:
            exit("ERROR: No endsong_x.json files found!")
        else:
            print(f"Processed {files} files.")

    def parse_account_data_files(self):
        '''
        Parse the account data download into a playtime dictionary
        '''
        files = 0
        for jsonFile in os.scandir(self.path):
            if "StreamingHistory" in jsonFile.path and 'json' in jsonFile.path:
                print('Opening ' + jsonFile.path + '...')
                files += 1
                with open(jsonFile.path, encoding="utf8") as file:
                    songList = json.load(file)
                for song in songList:
                    self.find_date_range(song['endTime'])
                    #if '$' in song[self.searchType]: continue
                    self.playtime[song[self.searchType]] += song['msPlayed'] / 60000 # divided to convert ms to minutes.
        if files == 0:
            exit("ERROR: No StreamingHistoryx.json files found!")
        else:
            print(f"Processed {files} files.")

    def find_date_range(self, time: str):
        '''
        Find the date range of the dataset
        '''
        if self.extended:
            date = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
        else:
            date = datetime.strptime(time, '%Y-%m-%d %H:%M')
        
        if not self.oldest or date < self.oldest:
            self.oldest = date
        if not self.newest or date > self.newest:
            self.newest = date

    def create_csv(self, file='out.csv'):
        '''
        Creates csv with 'searchType' and playtime (in minutes) columns.
        Requires a playtime dictionary (gathered from create_playtime_dict()), a searchType, and the file name/relative path to save CSV.
        '''
        with open(file, 'w', newline="\n", encoding="utf8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([self.friendlySearchType, 'playtime(m)'])
            for k, v in self.playtime_dict.items():
                writer.writerow([k, v])
        print(f'Finished writing csv file to: {file}')

    def plot_data(self, toPlot: int):
        '''
        Plots top 20 with matplotlib.
        Requires a playtime dictionary and a searchType.
        '''
        import matplotlib.pyplot as plt
        #l = dict(list(self.playtime_dict.items())[:toPlot])
        sliced = islice(self.playtime_dict.items(), toPlot)
        truncDict = OrderedDict(sliced)
        roundedTruncDict = dict(zip(truncDict, map(round, truncDict.values())))

        if self.darkMode:
            plt.style.use('dark_background')
        else:
            plt.style.use('ggplot')
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 6)
        #fig.set_dpi(100)

        x_pos = [i for i, _ in enumerate(truncDict.keys())]

        bars = ax.bar(x_pos, truncDict.values(), color='blue')
        #ax.set_xlabel(self.friendlySearchType)
        ax.set_ylabel("Minutes")
        ax.bar_label(bars, roundedTruncDict.values())
        #format = "%m/%d/%y"
        ax.set_title(f"Top {toPlot} playtime by {self.friendlySearchType} from {self.oldest} to {self.newest}")

        ax.set_xticks(x_pos, truncDict.keys(),
        rotation=45, 
        horizontalalignment='right',
        fontweight='light',
        fontsize='small')

        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='spotifyparse.py',
                                    description='Parses and charts Spotify data downloads')
    parser.add_argument('path', action='store', type=str, help="Path to the folder containing json files")
    parser.add_argument('-s','--song', action='store_true', help="Gather by song instead of artist")
    #parser.add_argument('-p','--plot', action='store_true', help="Create a matplotlib bar chart of the top 20 by playtime")
    parser.add_argument('-e','--extended', action='store_true', help="Use the extended streaming history files")
    parser.add_argument('-i','--include-podcasts', action='store_true', help="Include podcast data, only works on extended data", dest='includePodcasts')
    parser.add_argument('-o','--outfile', action='store', default=None, help="Saves csv in current directory with specified name")
    parser.add_argument('-d','--dark-mode', action='store_true', help="Plot with a dark background", dest='darkMode')
    parser.add_argument('-n','--plot-num', action='store', help="Number of items to plot", dest='plotNum', default=20, type=int)

    #subparsers = parser.add_subparsers(help='subplot')
    args = parser.parse_args()
    if args.includePodcasts and not args.extended:
        parser.error("Podcasts cannot be included or excluded unless using extended data")
    if args.song:
        searchType = 'trackName'
    else:
        searchType = 'artistName'
    sd = SpotifyData(args.path, searchType, args.extended, args.includePodcasts, args.darkMode)
    if args.outfile:
        sd.create_csv(args.outfile)
    sd.plot_data(args.plotNum)