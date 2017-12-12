from . import bench


class FreeAgent(bench):
    def __init__(self):
        bench.Bench.__init__(self)

    def get_trending(self):
        """
        Get a list of the top X adds  and top X drops

        :return:
        """
        pass

    def find_targets(self):
        """
        Find potential waiver targets for the specified week.
        :return:
        """
