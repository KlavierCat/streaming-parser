# ----- CLASSES
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
        self.datacenter_latency = int(datacenter_latency)
        self.caches = []

    def __str__(self):
        return "{}".format(self.number)

    def sort_caches(self):
        self.sorted_caches = sorted(self.caches, key=lambda c: c.latency)

class CacheConnection:
    def __init__(self, cache_number, latency, capacity):
        self.cache_number = cache_number
        self.latency = int(latency)
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
        return "endpoint:{} - vid {} - times: {}".format(self.from_endpoint, self.to_video, self.amount)

    def endpoint(self):
        return self.from_endpoint

    def size(self):
        return self.to_video.size

# -------------

class InputParser():
    def parse(self):
        # Getting how many things there are of each
        self.n_videos, self.n_endpoints, self.n_requests, self.n_caches, self.size_caches = raw_input().split(" ")

        # Getting videos
        self.video_sizes = raw_input().split(" ")
        self.videos = []
        for video_number, video_size in enumerate(self.video_sizes):
            self.videos.append(Video(video_number, video_size))

        # Getting endpoints and connections to cache
        self.endpoints = []
        self.caches = OrderedDict()
        for i in range(int(self.n_endpoints)):
            datacenter_latency, n_connected_caches = raw_input().split(" ")
            endpoint = Endpoint(i, datacenter_latency)
            for j in range(int(n_connected_caches)):
                cache_number, latency = raw_input().split(" ")
                endpoint.caches.append(CacheConnection(cache_number, latency, self.size_caches))
                self.caches[cache_number] = CacheConnection(cache_number, latency, self.size_caches)

            self.endpoints.append(endpoint)

        for e in self.endpoints:
            e.sort_caches()

        # Getting all requests
        self.requests = []
        for i in range(int(self.n_requests)):
            video_number, endpoint_number, latency = raw_input().split(" ")
            self.requests.append(Request(latency, self.videos[int(video_number)], self.endpoints[int(endpoint_number)]))

        solver = GreedySolver.GreedySolver(self.endpoints, self.requests, self.caches)

        # greed on the number of times a video is requested
        assigned_caches = solver.solve(lambda r: -r.amount)

        total_savings = 0
        total_requests = 0

        for r in self.requests:
            latency_used = min([ac.latency for ac in assigned_caches.values() if r.to_video.number in ac.videos] + [r.from_endpoint.datacenter_latency ])
            gain = r.from_endpoint.datacenter_latency - latency_used
            # print("req {} - DC Lat {} - Used Lat {} - gain {} * {}".format(r, r.from_endpoint.datacenter_latency, latency_used, gain, r.amount))

            total_savings += gain * r.amount
            total_requests += r.amount

        print("SCORE: {}".format(total_savings * 1000 / total_requests))

        #print(self.videos, self.endpoints, self.requests)

def main():
    parser = InputParser()
    parser.parse()

if __name__ == '__main__':
    main()
