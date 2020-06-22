import trimesh
from src.hole_finder import HoleFinder

from src.filter.interface_processing_filter import IProcessingFilter
class AFMFillingHoleFilter(IProcessingFilter):
    def __init__(self, unit_of_work):
        self.unit_of_work = unit_of_work
        self.holes = HoleFinder(self.unit_of_work).get_holes()

    # unsure
    def filtering(self):
        for front in self.holes:
            front = ...

    def get_mesh(self):
        return trimesh.Trimesh([self.unit_of_work.get_vertices_pos(), self.unit_of_work.get_faces()])

    def get_unit_of_work(self):
        return self.unit_of_work
