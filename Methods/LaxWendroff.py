from Method import CenteredMethod


class LaxWendroff(CenteredMethod):

    def __init__(self, ds, timestep, mesh):
        CenteredMethod.__init__(self, ds, mesh)
        self.timestep = timestep

    def __call__(self, u, p, velocity, adj):
        sigma_x = self.timestep*velocity[0]/(2*self.ds)
        sigma_y = self.timestep*velocity[1]/(2*self.ds)
        sigma_x2 = sigma_x**2
        sigma_y2 = sigma_y**2
        sx2_m_sx = (sigma_x2 - sigma_x) / 2
        sx2_p_sx = (sigma_x2 + sigma_x) / 2
        sy2_m_sy = (sigma_y2 - sigma_y) / 2
        sy2_p_sy = (sigma_y2 + sigma_y) / 2
        u_new = 0
        p_coords = self.mesh.points[p]
        for adj_p in adj[p]:
            adj_p_coords = self.mesh.points[adj_p]
            u_adj = u[adj_p]
            u_new = u_new +\
                self.right_element(adj_p_coords, p_coords) * u_adj * sx2_m_sx +\
                self.left_element(adj_p_coords, p_coords) * u_adj * sx2_p_sx +\
                self.top_element(adj_p_coords, p_coords) * u_adj * sy2_m_sy +\
                self.bot_element(adj_p_coords, p_coords) * u_adj * sy2_p_sy

        u_new = u_new + u[p]*(1 - sigma_x2 - sigma_y2)

        return u_new
