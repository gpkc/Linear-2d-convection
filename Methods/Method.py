import numpy as np


class Method:

    def __init__(self, ds, mesh):
        self.ds = ds
        self.mesh = mesh

    def left_element(self, adj_p_coords, p_coords):
        is_left = adj_p_coords[0] < p_coords[0]
        same_y_coord = np.abs(adj_p_coords[0] - p_coords[0]) / self.ds
        return is_left * same_y_coord

    def right_element(self, adj_p_coords, p_coords):
        is_right = adj_p_coords[0] > p_coords[0]
        same_y_coord = np.abs(adj_p_coords[0] - p_coords[0]) / self.ds
        return is_right * same_y_coord

    def top_element(self, adj_p_coords, p_coords):
        is_top = adj_p_coords[1] > p_coords[1]
        same_x_coord = np.abs(adj_p_coords[1] - p_coords[1]) / self.ds
        return is_top * same_x_coord

    def bot_element(self, adj_p_coords, p_coords):
        is_bot = adj_p_coords[1] < p_coords[1]
        same_x_coord = np.abs(adj_p_coords[1] - p_coords[1]) / self.ds
        return is_bot * same_x_coord

    def left_2_element(self, adj, p_coords, u):
        u_left_2 = 0
        for adj_p in adj:
            adj_p_coords = self.mesh.points[adj_p]
            u_adj = u[adj_p]
            u_left_2 = u_left_2 +\
                self.left_element(adj_p_coords, p_coords) * u_adj

        return u_left_2

    def right_2_element(self, adj, p_coords, u):
        u_2 = 0
        for adj_p in adj:
            adj_p_coords = self.mesh.points[adj_p]
            u_adj = u[adj_p]
            u_2 = u_2 +\
                self.right_element(adj_p_coords, p_coords) * u_adj

        return u_2

    def top_2_element(self, adj, p_coords, u):
        u_2 = 0
        for adj_p in adj:
            adj_p_coords = self.mesh.points[adj_p]
            u_adj = u[adj_p]
            u_2 = u_2 +\
                self.top_element(adj_p_coords, p_coords) * u_adj

        return u_2

    def bot_2_element(self, adj, p_coords, u):
        u_2 = 0
        for adj_p in adj:
            adj_p_coords = self.mesh.points[adj_p]
            u_adj = u[adj_p]
            u_2 = u_2 +\
                self.bot_element(adj_p_coords, p_coords) * u_adj

        return u_2


class CenteredMethod(Method):

    def __init__(self, ds, mesh):
        Method.__init__(self, ds, mesh)


class UpwindMethod(Method):

    def __init__(self, ds, mesh):
        Method.__init__(self, ds, mesh)

    def left_upwind(self, velocity):
        return (np.abs(velocity[0]) + velocity[0])/2

    def right_upwind(self, velocity):
        return (velocity[0] - np.abs(velocity[0]))/2

    def bot_upwind(self, velocity):
        return (np.abs(velocity[1]) + velocity[1])/2

    def top_upwind(self, velocity):
        return (velocity[1] - np.abs(velocity[1]))/2
