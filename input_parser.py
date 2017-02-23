#!/bin/env python
# encoding utf-8

#  ----- CLASSES

import GreedySolver
from collections import OrderedDict

class Video:
    def __init__(self, number, size):
        self.number = int(number)
        self.size = int(size)

    def __str__(self):
        return "{} s: {}".format(self.number, self.size)

class Endpoint:
    def __init__(self, number, datacenter_latency):
        self.number = number
        self.datacenter_latency = datacenter_latency
        self.caches = []

    def __str__(self):
        return "{}".format(self.number)

    def sort_caches(self):
        self.sorted_caches = sorted(self.caches, key=lambda c: c.latency)


class CacheConnection:
    def __init__(self, cache_number, latency, capacity):
        self.cache_number = cache_number
        self.latency = latency
        self.capacity = int(capacity)
        self.videos = []

    def __repr__(self):
        return "id: {} - lat: {}".format(self.cache_number, self.latency)

    def add_video(self, vid):
        self.videos.append(vid)

    def get_videos(self):
        return self.videos

    def id(self):
        return self.cache_number

class Request:
    def __init__(self, amount, to_video, from_endpoint):
        self.amount = int(amount)
        self.to_video = to_video
        self.from_endpoint = from_endpoint

    def __str__(self):
        return "endpoint:{} - vid {} - times: {} - value: {}".format(self.from_endpoint, self.to_video, self.amount, self.amount * self.size())

    def endpoint(self):
        return self.from_endpoint

    def size(self):
        return self.to_video.size

# -------------

# Getting how many things there are of each
n_videos, n_endpoints, n_requests, n_caches, size_caches = raw_input().split(" ")

# Getting videos
video_sizes = raw_input().split(" ")
videos = []
for video_number, video_size in enumerate(video_sizes):
    videos.append(Video(video_number, video_size))

# Getting endpoints and connections to cache
endpoints = []
caches = OrderedDict()
for i in range(int(n_endpoints)):
    datacenter_latency, n_connected_caches = raw_input().split(" ")
    endpoint = Endpoint(i, datacenter_latency)
    for j in range(int(n_connected_caches)):
        cache_number, latency = raw_input().split(" ")
        endpoint.caches.append(CacheConnection(cache_number, latency, size_caches))
        caches[cache_number] = CacheConnection(cache_number, latency, size_caches)

    endpoints.append(endpoint)

for e in endpoints:
    e.sort_caches()

# Getting all requests
requests = []
for i in range(int(n_requests)):
    video_number, endpoint_number, latency = raw_input().split(" ")
    requests.append(Request(latency, videos[int(video_number)], endpoints[int(endpoint_number)]))

# print(videos, endpoints, requests)
for v in videos:
    print("Video: {}".format(v))

print("Cache size: {}".format(size_caches))

solver = GreedySolver.GreedySolver(endpoints, requests, caches)

# greed on the number of times a video is requested
# assigned_caches = solver.solve(lambda r: -r.amount)

# greedy on the "total value" of the request = vid_size x amount
assigned_caches = solver.solve(lambda r: -r.amount * r.size())

print("-- Solution -- ")
for k, ac in sorted(assigned_caches.items(), key=lambda t: int(t[0])):
    print("cache {: 3d} : videos {}".format(int(k), sorted(ac.get_videos())))
print("--")
