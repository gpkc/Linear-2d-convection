from Method import UpwindMethod


class UpWind(UpwindMethod):

    def __init__(self, ds, timestep, mesh):
        UpwindMethod.__init__(self, ds, mesh)
        self.timestep = timestep

    def __call__(self, u, p, velocity, adj):
        sigma = -self.timestep/(self.ds)
        u_new = 0
        p_coords = self.mesh.points[p]
        for adj_p in adj[p]:
            adj_p_coords = self.mesh.points[adj_p]
            u_adj = u[adj_p]
            u_new = u_new +\
                (self.left_upwind(velocity) *
                    self.left_element(adj_p_coords, p_coords, u_adj) *
                    (u[p] - u[adj_p])) +\
                (self.right_upwind(velocity) *
                    self.right_element(adj_p_coords, p_coords, u_adj) *
                    (u[adj_p] - u[p])) +\
                (self.bot_upwind(velocity) *
                    self.bot_element(adj_p_coords, p_coords, u_adj) *
                    (u[p] - u[adj_p])) +\
                (self.top_upwind(velocity) *
                    self.top_element(adj_p_coords, p_coords, u_adj) *
                    (u[adj_p] - u[p]))

        u_new = (sigma * u_new) + u[p]

        return u_new
