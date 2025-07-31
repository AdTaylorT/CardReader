class region_of_interest():
    coords: list[tuple[int, int]]

    def __init__(self):
        self.coords = [(0,0)] * 2
        self.reset()

    def reset(self):
        self.coords[0] = (0,0)
        self.coords[1] = (0,0)

    def has_no_value(self):
        return self.coords[1] == (0,0)

    def set_coord(self, idx, val):
        if idx > 1:
            return

        self.coords[idx] = val
    
    def get_roi(self, frame):
        c1 = self.coords[0]
        c2 = self.coords[1]
        return frame[min(c1[1],c2[1]):max(c1[1],c2[1]), min(c1[0],c2[0]):max(c1[0],c2[0])]