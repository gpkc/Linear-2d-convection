from Method import Method
from BeamWarming import BeamWarming
from LaxWendroff import LaxWendroff


class Mixed(Method):

    def __init__(self, ds, timestep, mesh, alpha=0.5):
        Method.__init__(self, ds, mesh)
        self.BW = BeamWarming(ds, timestep, mesh)
        self.LW = LaxWendroff(ds, timestep, mesh)
        self.alpha = alpha

    def __call__(self, u, p, velocity, adj):
        u_new = self.alpha * self.BW(u, p, velocity, adj) +\
            (1 - self.alpha) * self.LW(u, p, velocity, adj)

        return u_new


class MixedWrapper(object):
    def __init__(self, alpha):
        self.alpha = alpha

    def __call__(self, ds, timestep, mesh):
        return Mixed(ds, timestep, mesh, self.alpha)
