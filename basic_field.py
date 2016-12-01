import os
import time

from Mesh import Mesh2D
from Solver import Solver2D

from Methods.LaxWendroff import LaxWendroff  # noqa
from Methods.BeamWarming import BeamWarming  # noqa
from Methods.Mixed import MixedWrapper  # noqa


mesh_folder = "meshes/"
solutions_folder = "solutions/"
info_file = "0_info.dat"

mesh_sizes = [50, 60, 70, 80, 90]

cfl_values = [0.1, 0.5, 0.9, 1.0, 1.1, 1.5, 1.9, 2.0]

methods = [
    {
        'solver': LaxWendroff,
        'name': "Lax_Wendroff"
    },
    {
        'solver': BeamWarming,
        'name': "Beam_Warming"
    },
    {
        'solver': MixedWrapper(0.1),
        'name': "Mixed_a0_1"
    },
    {
        'solver': MixedWrapper(0.25),
        'name': "Mixed_a0_25"
    },
    {
        'solver': MixedWrapper(0.5),
        'name': "Mixed_a0_5"
    },
    {
        'solver': MixedWrapper(0.75),
        'name': "Mixed_a0_75"
    },
    {
        'solver': MixedWrapper(0.9),
        'name': "Mixed_a0_9"
    },
]

for mesh_size in mesh_sizes:
    mesh_size = str(mesh_size) + "x" + str(mesh_size)
    mesh_filename = mesh_size + ".msh"
    myMesh = Mesh2D(mesh_folder + mesh_filename)
    myMesh._set_simple_scalar_field()
    myMesh._set_axial_velocity_field(0.5, 0.5)

    for cfl in cfl_values:

        for method in methods:
            final_directory = solutions_folder +\
                method['name'] + "/" +\
                "cfl_" + str(cfl) + "/" +\
                mesh_size

            if not os.path.exists(final_directory):
                os.makedirs(final_directory)

            print "\n===== Running " + method['name'] +\
                  " with cfl " + str(cfl) +\
                  " and mesh " + mesh_size + " =====\n"
            solver = Solver2D(myMesh, method['solver'], cfl)

            start = time.time()

            solver.run(final_directory, 100)

            done = time.time()
            elapsed = done - start

            with open(final_directory + "/" + info_file, 'w') as f:
                f.write("Timestep: " + str(solver.timestep))
                f.write("\nTime: " + str(elapsed))
