import numpy as np
import math

class CroppingFilter():
    def __init__(self):
        self.mesh = None
        self.noseIndex = 0
        self.depthSortVertices = None

    def InitMeshAttributes(self, mesh):
        self.mesh = mesh.copy()
        self.depthSortVertices = sorted(self.mesh.vertices, key=lambda vertice: vertice[2], reverse=True)

    def GetMesh(self):
        return self.mesh

    def GetNoseIndex(self):
        return self.noseIndex

    def Filtering(self, mesh, r):
        self.InitMeshAttributes(mesh)
        preSphereVerticeNum = 0
        for vertice in self.depthSortVertices:
            mesh = self.GetShpereMesh(self.mesh, vertice, r)
            curSphereVerticeNum = len(mesh.vertices)
            if curSphereVerticeNum - preSphereVerticeNum > 150:
                self.noseIndex = self.FindNoseIndex(mesh.vertices, vertice)
                self.mesh = mesh
                break
            preSphereVerticeNum = curSphereVerticeNum

    def GetShpereMesh(self, originMesh, centerVertice, r):  # private
        mesh = originMesh.copy()
        sphereIndexes = self.GetSphereIndexes(mesh, centerVertice, r)
        mesh = self.RemoveFaces(mesh, sphereIndexes)
        mesh = self.RemoveVertices(mesh)
        return mesh

    def GetSphereIndexes(self, mesh, centerVertice, r):  # private
        sphereIndexes = np.array([])
        for index, vertice in enumerate(mesh.vertices):
            if self.EuclideanDistance(centerVertice, vertice, 3) < r:
                sphereIndexes = np.append(sphereIndexes, index)
        return sphereIndexes

    def EuclideanDistance(self, lvertice, rvertice, dimensional):  # private
        euclideanDistance = 0
        for d in range(dimensional):
            euclideanDistance += pow(lvertice[d] - rvertice[d], 2)
        euclideanDistance = math.sqrt(euclideanDistance)
        return euclideanDistance

    """
        Rename the name of function and parameter
    """

    def RemoveFaces(self, mesh, sphereIndexes):  # private
        faces = np.empty((0, 3), int)
        for face in mesh.faces:
            if self.IsFaceCompositionOfShpereVertices(face, sphereIndexes):
                faces = np.append(faces, np.array([face]), axis=0)
        mesh.faces = faces
        return mesh

    def IsFaceCompositionOfShpereVertices(self, face, sphereIndexes):  # private
        for vertice in face:
            if not (vertice in sphereIndexes):
                return False
        return True

    def RemoveVertices(self, mesh):  # private
        mesh.remove_unreferenced_vertices()
        return mesh

    def FindNoseIndex(self, vertices, vertice):  # private
        for index in range(len(vertices)):
            if (np.array(vertices[index]) == np.array(vertice)).all():
                return index
        return -1