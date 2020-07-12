import trimesh

from src.filter.interface_processing_filter import IProcessingFilter
# from src.filter.interface_processing_filter import IProcessingFilter
class TaubinSmoothingFilter(IProcessingFilter):
    def __init__(self, unit_of_work):
        self.unit_of_work = unit_of_work
        self.mesh = None

    def filtering(self):
        self.mesh = trimesh.Trimesh([self.unit_of_work.get_vertices_pos(), self.unit_of_work.get_faces()])
        trimesh.smoothing.filter_taubin(self.mesh)
        self.unit_of_work.refresh(self.mesh)

    def get_mesh(self):
        return self.mesh

    def get_unit_of_work(self):
        return self.unit_of_work