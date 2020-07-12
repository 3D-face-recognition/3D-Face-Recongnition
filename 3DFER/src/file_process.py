from src.features_selection import FeaturesSelection
import os
import numpy as np
import trimesh
from src.filter.z_circle_cropping_filter import ZCircleCroppingFilter
from src.filter.taubin_smoothing_filter import TaubinSmoothingFilter
from src.filter.afm_filling_hole_filter import AFMFillingHoleFilter
from src.pipe_and_sink.preprocessing_pipe import PreprocessingPipe
from src.pipe_and_sink.preprocessing_sink import PreprocessingSink
from src.data.unit_of_work import UnitOfWork
from src.features_selection_strategy.average_pick_up_vertices import AveragePickUpVertices
from src.features_selection_strategy.histogram_oriented_gradient import HistogramOrientedGradient
from src.features_selection_strategy.local_binary_patterns import LocalBinaryPatterns
from src.filter.cropping_filter import  CroppingFilter

class FileProcess(object):
    def __init__(self):
        self.base_path = self.__get_base_path()
        self.meshes = []
        self.obj_files = []
        self.files_register = []

    def __get_base_path(self):
        return os.getcwd()[:-4] + "//UoY//"

    def __filter_file_names(self):
        files = os.listdir(self.base_path)
        for file in files:
            if "obj" in file and ("-08-" in file or "-10-" in file):
                print("select " + file)
                self.obj_files.append(file)

    def load_file(self):
        #find images in folder
        self.__filter_file_names()

        X = []
        y = []
        if len(self.files_register) != 0:
            self.obj_files = self.files_register

        for file in self.obj_files:
            print("Now loading ", len(X)+1)
            if len(X) > 10:
                break
            mesh = trimesh.load(self.base_path + file)
            # smoothing and cropping for filter incomplete mesh
            smoothing_mesh = trimesh.smoothing.filter_taubin(mesh)
            cropping_filter = CroppingFilter()
            cropping_filter.Filtering(smoothing_mesh, 125)
            cropping_mesh = cropping_filter.GetMesh()

            # move nose to 0,0,0
            nose_vertices = cropping_mesh.vertices[cropping_filter.GetNoseIndex()]
            new_vertices = [vertices - nose_vertices for vertices in cropping_mesh.vertices]
            cropping_mesh.vertices = new_vertices

            # change type of mesh and color
            cropping_mesh.visual = cropping_mesh.visual.to_color()
            for index, facet in enumerate(cropping_mesh.visual.vertex_colors):
                cropping_mesh.visual.vertex_colors[index] = [0, 255, 0, 0]

            # generate X and y to use on model
            if cropping_mesh.area > 33000:
                if len(self.files_register) < 30:
                    self.files_register.append(file)  # register
                # add label
                if "-08-" in file:
                    y.append(0)  # angry
                elif "-10-" in file:
                    y.append(3)  # happy

                select_strategy = LocalBinaryPatterns(cropping_mesh)
                fs = FeaturesSelection(select_strategy)
                X.append(fs.fit())
                self.meshes.append(cropping_mesh)
        y = np.array(y)
        return X, y


    def __get_unit_preprocessing_of_work(self, mesh):
        unit_of_work = UnitOfWork(mesh)
        smoothing_pipe = PreprocessingPipe(TaubinSmoothingFilter(unit_of_work))
        cropping_pipe = PreprocessingPipe(ZCircleCroppingFilter(unit_of_work, 125))
        filling_hole_pipe = PreprocessingPipe(AFMFillingHoleFilter(unit_of_work))
        sink = PreprocessingSink()
        smoothing_pipe.set_next(cropping_pipe)
        cropping_pipe.set_next(filling_hole_pipe)
        filling_hole_pipe.set_next(sink)
        unit_of_work = sink.get_unit_of_work()
        return unit_of_work
