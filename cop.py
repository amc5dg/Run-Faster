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


    def get_data(self):
        self.lp_dic = defaultdict(int)
        for j in range(10):
            self.efforts = []
            try:
                for i in range(1,1500):
                    print(j,i)
                    time.sleep(1.5)
                    page = requests.get(self.url_base + 'segments/{}/all_efforts'.format(self.segments[j]), headers=self.header, params={'per_page': self.page_max, 'page': i}).json()

                    if page != []:
                        self.efforts.append(page)
                    else:
                        self.lp_dic[self.segments[j]]=i
                        self.get_athletes_who_attempted_segment()
                        break
            except ValueError:
                self.lp_dic[self.segments[j]] = i
                self.get_athletes_who_attempted_segment()
                continue
        self.last_page = self.lp_dic

        # for key,value in self.lp_dic.items():
        #     self.get_segment_efforts(value,key)
        #     self.get_athletes_who_attempted_segment()


        # self.save_to_mongodb()

        with open('a.pkl','wb') as f:
            pickle.dump(self.a_list,f)
        with open('t.pkl','wb') as f:
            pickle.dump(self.t_list,f)
        with open('d.pkl','wb') as f:
            pickle.dump(self.d_list,f)

    # def get_segment_efforts(self,last_page,segment):
    #     efforts = []
    #     for i in range(1,last_page):
    #         time.sleep(1.5)
    #         print(i)
    #         page = requests.get(self.url_base + 'segments/{}/all_efforts'.format(segment), headers=self.header, params={'per_page': self.page_max, 'page': i}).json()
    #         efforts.append(page)
    #     self.efforts = efforts

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
            for j in range(self.page_max-1):
                print(i,j)
                athlete_id = self.efforts[i][j]['athlete']['id']
                if athlete_id in athletes:
                    athletes[athlete_id] += 1
                    times[athlete_id].append(self.efforts[i][j]['elapsed_time'])
                    dates[athlete_id].append(self.efforts[i][j]['start_date'])
                else:
                    athletes[athlete_id] = 1
                    times[athlete_id] = [self.efforts[i][j]['elapsed_time']]
                    dates[athlete_id] = [self.efforts[i][j]['start_date']]

        self.athletes = athletes
        self.times = times
        self.dates = dates

        self.a_list.append(self.athletes)
        self.t_list.append(self.times)
        self.d_list.append(self.dates)

    # def save_to_mongodb(self):
    #     client = MongoClient()
    #     db_a = client.denver_segments_a
    #     collections_a = db_a.collections
    #
    #     db_t = client.denver_segments_t
    #     collections_t = db_t.collections
    #
    #     db_d = client.denver_segments_d
    #     collections_d = db_d.collections
    #
    #     self.a_dic = {str(k):v for k,v in enumerate(self.a_list)}
    #     self.t_dic = {str(k):v for k,v in enumerate(self.t_list)}
    #     self.d_dic = {str(k):v for k,v in enumerate(self.d_list)}

        # collections_a.insert_one(self.a_dic)
        # collections_a.insert_one(self.a_dic)
        # collections_a.insert_one(self.a_dic)

if __name__ == '__main__':
    running = RunFreeData()
    bounds = '39.958280, -105.319698,39.996563, -105.278585'
    running.get_segments_by_gps(bounds)
    running.get_data()
    print(running.last_page)
