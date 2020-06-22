import trimesh
import os
from src.data.unit_of_work import UnitOfWork
from src.filter.z_circle_cropping_filter import ZCircleCroppingFilter
from src.filter.taubin_smoothing_filter import TaubinSmoothingFilter
from src.filter.afm_filling_hole_filter import AFMFillingHoleFilter
from src.pipe_and_sink.preprocessing_pipe import PreprocessingPipe
from src.pipe_and_sink.preprocessing_sink import PreprocessingSink
from src.features_selection_strategy.average_pick_up_vertices import AveragePickUpVertices
from src.features_selection_strategy.only_pick_nose import OnlyPickNose
from src.features_selection import FeaturesSelection

base_path = os.getcwd()[:-4] + "//UoY//"

obj_filename = base_path + '00023-13-mww38ngngy.obj'
mesh = trimesh.load(obj_filename)

mesh.visual = mesh.visual.to_color()

for index, facet in enumerate(mesh.visual.vertex_colors):
    mesh.visual.vertex_colors[index] = [0,255,0,0]

unit_of_work = UnitOfWork(mesh)
smoothing_pipe = PreprocessingPipe(TaubinSmoothingFilter(unit_of_work))
cropping_pipe = PreprocessingPipe(ZCircleCroppingFilter(unit_of_work, 125))
filling_hole_pipe = PreprocessingPipe(AFMFillingHoleFilter(unit_of_work))
sink = PreprocessingSink()
smoothing_pipe.set_next(cropping_pipe)
cropping_pipe.set_next(filling_hole_pipe)
filling_hole_pipe.set_next(sink)
unit_of_work = sink.get_unit_of_work()

# strategy
average_pick_up_vertices = AveragePickUpVertices(mesh)
fs = FeaturesSelection(average_pick_up_vertices)
fs.fit()

only_pick_nose = OnlyPickNose(mesh)
fs.change_strategy(only_pick_nose)
fs.fit()

# smoothing_mesh = mesh.copy()
# trimesh.smoothing.filter_taubin(smoothing_mesh)
#
# cropping_filter = ZCircleCroppingFilter()
# cropping_filter.filtering(smoothing_mesh, 125)
# cropping_mesh = cropping_filter.get_mesh()
# cropping_mesh.visual.vertex_colors[cropping_filter.get_nose_index()] = [255,0,0,0]
#
# mesh = cropping_mesh.copy()
# vertex_params_finder = VertexParamsFinder(mesh)
# vertex_repository = VertexRepository(vertex_params_finder)
# print(vertex_repository.get_by_index(0).get_index())
# boundary_vertex_repository = BoundaryVertexRepository(vertex_params_finder)
