import numpy as np


class Solver2D:
    """
    Solves the problem du/dt + V.grad(u) = 0
    For three dependent variables (t, x, y)
    """

    def __init__(self, mesh, method, cfl=1.0):
        self.mesh = mesh
        self._set_default_initial_condition()
        self.ds = np.sqrt((mesh.points[mesh.adj['point'][0][1]][0] -
                          mesh.points[0][0])**2 +
                          (mesh.points[mesh.adj['point'][0][1]][1] -
                          mesh.points[0][1])**2)
        max_v = self._max_velocity()
        self.timestep = cfl * self.ds / (max_v[0] + max_v[1])
        print "Timestep size: " + str(self.timestep)
        self.method = method(self.ds, self.timestep, self.mesh)

    def _max_velocity(self):
        v = self.mesh.fields['velocity']
        max_vx = np.max([v[p][0] for p, _ in enumerate(v)])
        max_vy = np.max([v[p][1] for p, _ in enumerate(v)])
        return [max_vx, max_vy]

    def _pulse(self, x, y, size_x=0.1, size_y=0.1, c_x=0.5, c_y=0.5):
        if ((x <= (c_x + size_x) and x >= (c_x - size_x)) and
           (y <= (c_y + size_y) and y >= (c_y - size_y))):
            return 1
        return 0

    def _gauss_pulse(self, x, y, c_x=0.5, c_y=0.5):
        return 0

    def _saw_pulse(self, x, y, c_x=0.5, c_y=0.5):
        return 0

    def _set_default_initial_condition(self):
        self.mesh.fields['u'] = np.array([self._pulse(x, y, c_x=0.5, c_y=0.75) + # noqa
                                          self._gauss_pulse(x, y) +
                                          self._saw_pulse(x, y)
                                          for x, y in self.mesh.points]).\
                                          astype('float32')

    def _step(self):
        velocity = self.mesh.fields['velocity']
        u = self.mesh.fields['u']
        adj = self.mesh.adj['point']
        self.mesh.fields['u'] = np.array([self.method(u, p, velocity[p], adj)
                                          for p, _ in enumerate(u)])

    def run(self, foldername, timesteps):
        time = 0
        filename_suffix = foldername + "/" + "sol_"
        while(time < timesteps):
            if((time/float(timesteps))*100 % 10 == 0):
                print(time/float(timesteps))
            self.mesh.export(filename_suffix + str(time) + ".vtk")
            self._step()
            time = time + 1
