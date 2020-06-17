from abc import ABCMeta, abstractclassmethod
import numpy
import trimesh
class FeatureSelectionStrategy(metaclass = ABCMeta):
    @abstractclassmethod
    def select_features(self):
        pass



class AveragePickUpVertices(FeatureSelectionStrategy):  
    def __init__(self, mesh, quantity=40):
        self.mesh = mesh
        self.quantity = quantity
        self.vertices = None

    def select_features(self):
        selected_index = []
        iter_time = 0
        dtype = [('x', float), ('y', float), ('z', float)]
        vertices_seq = numpy.array([tuple(vertices) for vertices in self.mesh.vertices], dtype= dtype)
        vertices_seq = numpy.array([list(vertices) for vertices in numpy.sort(vertices_seq, order=['y', 'x', 'z'])])
        for index, point in enumerate(vertices_seq):
            if len(selected_index) >= self.quantity:
                break
            if self.__is_maintain_distance(point, vertices_seq[selected_index], 30): 
                selected_index.append(index)
            
        #draw the points on mesh
        #print("length of selected: ", len(selected_index))
        self.__visual_selected_points(self.mesh, vertices_seq[selected_index])
        return vertices_seq[selected_index]
    
    #private
    def __count_distance(self, p1, p2):
        return numpy.power(numpy.sum(numpy.square(numpy.array(p1) - numpy.array(p2))), 0.5)

    def __is_maintain_distance(self, point, selected_points, distance):
        for selected_point in selected_points:
            if self.__count_distance(point, selected_point) < distance:
                return False
        return True

        
    def __visual_selected_points(self, mesh, selected_points, selected_color=[255,0,0,0],
                          not_selected_color=[0,255,0,0]):
        for vertices in selected_points:
            index, j =  numpy.where(mesh.vertices== vertices) 
            mesh.visual.vertex_colors[index[0]] =  selected_color
    
class OnlyPickNose(FeatureSelectionStrategy):
    def __init__(self, mesh, nose_index=100):
        self.mesh = mesh
        self.nose_index = nose_index

    def select_features(self):
        return [self.mesh.vertices[self.nose_index]]

#     def _find_point_in_witch_triangle(self, mesh, point):
#         for triangle in mesh.triangles:
#             part_triangle_1 = count_triangle_area([point, triangle[0], triangle[1]])
#             part_triangle_2 = count_triangle_area([point, triangle[1], triangle[2]])
#             part_triangle_3 = count_triangle_area([point, triangle[0], triangle[2]])
#             if triangle.area == (part_triangle_1 + part_triangle_2 + part_triangle_3):
#                 return triangle
# #         return None
#     def count_triangle_area(self, vertices):
#         a = self.count_distance(vertices[0], vertices[1])
#         b = self.count_distance(vertices[0], vertices[2])
#         c = self.count_distance(vertices[1], vertices[2])
#         s = (a+b+c)/2
#         return pow(s*(s-a)*(s-b)*(s-c), 0.5)
    
#     def hog(self, mesh, mask_size=(2,2)):
#         x_min = mesh.vertices[np.argmin(mesh.vertices[:, 0])][0]
#         y_min = mesh.vertices[np.argmin(mesh.vertices[:, 1])][1]
#         x_max = mesh.vertices[np.argmax(mesh.vertices[:, 0])][0]
#         y_max = mesh.vertices[np.argmax(mesh.vertices[:, 1])][1]
#         print("x range:", x_min, x_max, "y range:", y_min, y_max)
#         sampling_frequency = 1.0
#         for y in range(y_min, y_max, mask_size[1]):
#             for x in range(x_min, x_max, mask_size[0]):

# class TestFeaturesSelector(unittest.TestCase):
#     @classmethod
#     def setUp(self):
#         self.selected_points = [[0, 7, 10], [2, 6, 10], [3, 4, 9]]
#         self.vertices = [[0, 0, 0], [2, 2, 4], [3, 3, 0], [4, 1, 4]]
#         self.FS = FeaturesSelector()
        
#     def test_count_distance(self):
#         self.assertAlmostEqual(self.FS.count_distance(self.vertices[0], self.vertices[1]), 4.8989, places=3)
#         self.assertAlmostEqual(self.FS.count_distance(self.vertices[0], self.vertices[2]), 4.2426, places=3)
    
#     def test_is_maintain_distance(self):
#         self.assertTrue(self.FS.is_maintain_distance(self.vertices[0], self.selected_points, 10))
#         self.assertFalse(self.FS.is_maintain_distance(self.vertices[1], self.selected_points, 10))
# unittest.main(argv=[''], verbosity=2, exit=False)