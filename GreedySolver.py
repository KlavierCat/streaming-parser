class GreedySolver:

    def __init__(self, endpoints, requests, caches):
        self.endpoints = endpoints
        self.requests = requests
        self.caches = caches

    def solve(self, req_eval_function):

        for req in sorted(self.requests, key=req_eval_function):
            end_point = req.endpoint()
            caches_arrays = end_point.sorted_caches

            # print("Processing req: {}".format(req))

            for c in caches_arrays:

                if req.to_video.number in self.caches[c.cache_number].videos:
                    # print("repeated vid already in cache")
                    break

                cap = self.caches[c.cache_number].capacity
                # print(cap, req.size(), req.to_video.number)
                if cap - req.size() >= 0:
                    self.caches[c.cache_number].add_video(req.to_video.number)
                    self.caches[c.cache_number].capacity = cap - req.size()
                    break

        return self.caches
