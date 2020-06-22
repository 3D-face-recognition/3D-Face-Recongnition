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
from src.features_selection_strategy.only_pick_nose import OnlyPickNose


class FileProcess(object):
    def __init__(self):
        self.X = []
        self.y = []
        self.base_path = self.__get_base_paht()
        self.meshes = []
        self.obj_files = []
        self.files_register = []

    def __get_base_path(self):
        return os.getcwd()[:-4] + "//UoY//"

    def __filter_file_names(self):
        files = os.listdir(self.base_path)
        for file in files:
            if "obj" in file and ("-08-" in file or "-10-" in file):
                self.obj_files.append(file)

    def load_file(self):
        if len(self.files_register) != 0:
            self.obj_files = self.files_register

        for file in self.obj_files:
            print("loading", file)
            if len(self.X) > 30:
                break
            mesh = trimesh.load(self.base_path + file)

            # preprocessing, such as smoothing, cropping....
            cropping_mesh = self.__preprocessing(mesh)

            # generate X and y to use on model
            if cropping_mesh.area > 33000:
                if len(self.files_register) < 30:
                    self.files_register.append(file)  # register
                # add label
                if "-08-" in file:
                    self.y.append(0)  # angry
                elif "-10-" in file:
                    self.y.append(3)  # happy
                # features selection
                select_strategy = AveragePickUpVertices(cropping_mesh, 40)
                fs = FeaturesSelection(select_strategy)
                self.X.append(fs.fit())
                self.meshes.append(cropping_mesh)
        self.y = np.array(self.y)

    def __preprocessing(self, mesh):
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
