import numpy as np


class HanoiSolver:
    def __init__(self, n_disks):
        self.n_disks = n_disks
        self.towers = [[], [], []]
        self.start_order = []

    def solve(self):
        return []