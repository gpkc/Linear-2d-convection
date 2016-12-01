import numpy as np
import meshio


class Mesh2D:

    def __init__(self, filename):
        points, cells, point_data, cell_data, field_data = \
            meshio.read(filename)
        self.points = np.array([[x, y] for [x, y, _] in points])
        self.cells = cells
        self.fields = {}
        self.adj = {}
        self._set_1d_adjacency()

    def _set_1d_adjacency(self):
        self.adj['point'] = [set() for i, _ in enumerate(self.points)]
        for [p1, p2, p3, p4] in self.cells['quad']:
            self.adj['point'][p1].add(p2)
            self.adj['point'][p2].add(p1)
            self.adj['point'][p2].add(p3)
            self.adj['point'][p3].add(p2)
            self.adj['point'][p3].add(p4)
            self.adj['point'][p4].add(p3)
            self.adj['point'][p4].add(p1)
            self.adj['point'][p1].add(p4)

        self.adj['point'] = np.array([[i for i in pset]
                                      for pset in self.adj['point']])

    def _set_simple_scalar_field(self):
        def f(x, y):
            return x*y

        scalar = np.array([f(x, y) for [x, y] in self.points]).\
            astype('float32')
        self.fields['scalar'] = scalar

    def _set_axial_velocity_field(self, c_x=0.5, c_y=0.5):
        def f(x, y):
            return [y-c_x, -x+c_y, 0]

        vector = np.array([f(x, y) for [x, y] in self.points]).\
            astype('float32')
        self.fields['velocity'] = vector

    def export(self, filename):
        points = np.array([[x, y, 0] for [x, y] in self.points])
        meshio.write(filename, points, self.cells, point_data=self.fields)
