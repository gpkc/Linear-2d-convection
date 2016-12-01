from Method import UpwindMethod


class BeamWarming(UpwindMethod):

    def __init__(self, ds, timestep, mesh):
        UpwindMethod.__init__(self, ds, mesh)
        self.timestep = timestep

    def __call__(self, u, p, velocity, adj):
        sigma = self.timestep/(2*self.ds)
        u_new = 0
        p_coords = self.mesh.points[p]
        for adj_p in adj[p]:
            adj_p_coords = self.mesh.points[adj_p]
            u_adj = u[adj_p]
            adj_adj_p = adj[adj_p]

            l_adj = self.left_2_element(adj_adj_p, adj_p_coords, u)
            r_adj = self.right_2_element(adj_adj_p, adj_p_coords, u)
            t_adj = self.top_2_element(adj_adj_p, adj_p_coords, u)
            b_adj = self.bot_2_element(adj_adj_p, adj_p_coords, u)
            u_new = u_new +\
                (self.left_upwind(velocity) *
                    self.left_element(adj_p_coords, p_coords) *
                    ((-3*u[p]/2) + (2*u_adj) - (l_adj/2) +  # noqa
                     (sigma*u[p]/2) - (sigma*u_adj) + (sigma*l_adj/2))) +\
                (self.right_upwind(velocity) *
                    self.right_element(adj_p_coords, p_coords) *
                    ((3*u[p]/2) - (2*u_adj) + (r_adj/2) +  # noqa
                     (sigma*u[p]/2) - (sigma*u_adj) + (sigma*r_adj/2))) +\
                (self.bot_upwind(velocity) *
                    self.bot_element(adj_p_coords, p_coords) *
                    ((-3*u[p]/2) + (2*u_adj) - (b_adj/2) +  # noqa
                     (sigma*u[p]/2) - (sigma*u_adj) + (sigma*b_adj/2))) +\
                (self.top_upwind(velocity) *
                    self.top_element(adj_p_coords, p_coords) *
                    ((3*u[p]/2) - (2*u_adj) + (t_adj/2) +  # noqa
                     (sigma*u[p]/2) - (sigma*u_adj) + (sigma*t_adj/2)))

        u_new = (sigma * u_new) + u[p]

        return u_new
