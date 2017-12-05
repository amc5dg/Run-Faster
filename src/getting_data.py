import json
from pymongo import MongoClient
import os
import requests
from collections import defaultdict
import time
import pickle

class RunFreeData(object):

    def __init__(self):
        self.access_token = os.environ['ACCESS_TOKEN']
        self.header = {'Authorization' : 'Bearer %s' % self.access_token}
        self.url_base = 'https://www.strava.com/api/v3/'
        self.activity_type = 'running'
        self.segments = None
        self.page_max = 200
        self.bounds = None
        self.page = None
        self.efforts = None
        self.last_page = None
        self.a_list = []
        self.t_list = []
        self.d_list = []

    def get_segments_by_gps(self,gps_string):
        '''
        Draw a 'box' to get all segments in an area.

        Inputs:
        ------
        self
        gps_string: a string outlining the gps boundary of the area. (See below for additional notes)

        Note: Strava API syntax given by: ‘sw.lat,sw.lng,ne.lat,ne.lng’

        Outputs:
        -------
        A list of segment_id's in the specified area
        '''

        self.bounds = gps_string

        self.segments_info = requests.get(self.url_base + 'segments/explore', headers=self.header, params={'bounds': self.bounds,'activity_type':self.activity_type}).json()

        self.num_segments = len(self.segments_info['segments'])

        self.segments = [self.segments_info['segments'][x]['id'] for x in range(self.num_segments)]

    def get_segment_efforts(self,segments):
        self.segments = segments
        self.segments_info = requests.get(self.url_base + 'segments/{}'.format(segments[0]),headers=self.header).json()

    def get_data(self):
        self.lp_dic = defaultdict(int)
        for j in range(len(self.segments)):
            self.efforts = []
            try:
                for i in range(0,10000):
                    print(j,i)
                    time.sleep(1.5)
                    page = requests.get(self.url_base + 'segments/{}/all_efforts'.format(self.segments[j]), headers=self.header, params={'per_page': self.page_max, 'page': i}).json()

                    if page != []:
                        self.efforts.append(page)
                    else:
                        self.lp_dic[self.segments[j]]=i
                        self.get_athletes_who_attempted_segment()
                        break
            except:
                self.lp_dic[self.segments[j]] = i
                self.get_athletes_who_attempted_segment()
                continue
        self.last_page = self.lp_dic
        
        # saving the model data
        
        with open('a2.pkl','wb') as f:
            pickle.dump(self.a_list,f)
        with open('t2.pkl','wb') as f:
            pickle.dump(self.t_list,f)
        with open('d2.pkl','wb') as f:
            pickle.dump(self.d_list,f)

    def get_athletes_who_attempted_segment(self):
        '''
        This function takes the json file of the efforts on a given segment and returns 3 dictionaries (with the athlete's id as a key): athletes that returns how many times each athlete attempted the segment, times that returns the elapsed time for each of their attempts, and dates which givves the date of each attempt.

        Inputs:
        -------
        efforts: a list of dictionaries of recorded segment efforts

        Outputs:
        --------
        athletes: Dictionary of (athlete_id: # of times segment completed) pairs

        times: Dictionary of (athlete_id: how long each of their segment efforts took) pairs

        dates: Dictionary of (athlete_id: the date of each of their efforts) pairs

        '''
        num_pages = len(self.efforts)
        athletes = defaultdict(int)
        times = defaultdict(list)
        dates = defaultdict(list)
        for i in range(num_pages-1):
            for j in range(self.page_max):

                print(i,j)
                try:
                    athlete_id = self.efforts[i][j]['athlete']['id']
                    if athlete_id in athletes:
                        athletes[athlete_id] += 1
                        times[athlete_id].append(self.efforts[i][j]['elapsed_time'])
                        dates[athlete_id].append(self.efforts[i][j]['start_date'])
                    else:
                        athletes[athlete_id] = 1
                        times[athlete_id] = [self.efforts[i][j]['elapsed_time']]
                        dates[athlete_id] = [self.efforts[i][j]['start_date']]
                except:
                    break

        self.athletes = athletes
        self.times = times
        self.dates = dates

        self.a_list.append(self.athletes)
        self.t_list.append(self.times)
        self.d_list.append(self.dates)

if __name__ == '__main__':
    
    # Searching for good data
    crissy = '37.803641,-122.473825,37.807155,-122.447496'
    ggp = '37.763199,-122.511097,37.775297,-122.453977'
    embarc = '37.790310,-122.422348,37.812338,-122.401405'
    marine_headlands = '37.840308,-122.552467,37.870910, -122.528107'
    city_loop = '37.762089,-122.510246,37.810932,-122.407930'
    presidio = '37.785290,-122.480057,37.804760,-122.453964'
    double_dipsea = '37.804760,,-122.453964,37.913735,-122.570350'
    ggb = '37.800840,-122.477996,37.831051,-122.477996'
    ninja_loop = '37.828716, -122.524130,37.868504,-122.514860'
    northside_loop = '37.916160,-122.610261,37.936035,-122.567689'

    # track 400m
    t_400_ggp = 630725

    # xc course 800m
    f_800_xc = 8525023

    running = RunFreeData()
    bounds = northside_loop
    running.get_segment_efforts([8525023,630725])
    # running.get_data()
