import bench


class Players(bench.Bench):
    def __init__(self, league):
        bench.Bench.__init__(self)
        self.league = league
