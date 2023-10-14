import math
from math import pi, sin, cos, tan
from algebra import *
from figures import Triangle
class Obj3D(object):
    def __init__(self, filename,material,rot=(0,0,0),translate=(0,0,0), scale=(1,1,1)):
        # Asumiendo que el archivo es un formato .obj
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()

        # Se crean los contenedores de los datos del selfo.
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        # Por cada línea en el archivo
        for line in self.lines:
            # Si la línea no cuenta con un prefijo y un valor,
            # seguimos a la siguiente línea
            try:
                prefix, value = line.split(" ", 1)
                prefix = prefix.strip()
                value = value.strip()
            except:
                continue

            # Dependiendo del prefijo, parseamos y guardamos la información
            # en el contenedor correcto

            if prefix == "v":  # Vertices
                self.vertices.append(list(map(float, value.split(" "))))
            elif prefix == "vt":  # Texture Coordinates
                self.texcoords.append(list(map(float, value.split(" "))))
            elif prefix == "vn":  # Normals
                self.normals.append(list(map(float, value.split(" "))))
            elif prefix == "f":  # Faces
                self.faces.append([list(map(int, vert.split("/"))) for vert in value.split(" ")])
        
        self.material = material
        self.rot = rot
        self.translate = translate
        self.scale = scale
        self.__setMatrix()
        self.__makeVerts()
        self.__createTraingles()
        self.calculate_bounds()

    def vertexShader(self,vertex, **kwargs):
        # El Vertex Shader se lleva a cabo por cada vértice
        vt = [vertex[0],
            vertex[1],
            vertex[2],
            1]

        vt = multiplicar_matriz_vector(self.Mmat,vt)

        vt = [vt[0] / vt[3],
            vt[1] / vt[3],
            vt[2] / vt[3]]

        return vt
    
    def __setMatrix(self):
        # Matriz de traslación
        translation = [[1, 0, 0, self.translate[0]],
                                 [0, 1, 0, self.translate[1]],
                                 [0, 0, 1, self.translate[2]],
                                 [0, 0, 0, 1]]

        # Matrix de rotación
        rotMat = self.__rotationMatrix(self.rot)

        # Matriz de escala
        scaleMat = [[self.scale[0], 0, 0, 0],
                              [0, self.scale[1], 0, 0],
                              [0, 0, self.scale[2], 0],
                              [0, 0, 0, 1]]

        # Se multiplican las tres para obtener la matriz del objeto final
        self.Mmat = multiplicar_matrices(multiplicar_matrices(translation,rotMat),scaleMat)
   
    def __rotationMatrix(self, rotation = (0,0,0)):
        # Convertir a radianes
        pitch = rotation[0] * pi / 180
        yaw =   rotation[1] * pi / 180
        roll =  rotation[2] * pi / 180

        # Creamos la matriz de rotación para cada eje.
        pitchMat = [[1, 0, 0, 0],
                              [0, cos(pitch), -sin(pitch), 0],
                              [0, sin(pitch), cos(pitch), 0],
                              [0, 0, 0, 1]]

        yawMat = [[cos(yaw), 0, sin(yaw), 0],
                            [0, 1, 0, 0],
                            [-sin(yaw), 0, cos(yaw), 0],
                            [0, 0, 0, 1]]

        rollMat = [[cos(roll), -sin(roll), 0, 0],
                             [sin(roll), cos(roll), 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]]

        # Se multiplican las tres matrices para obtener la matriz de rotación final
        return multiplicar_matrices(multiplicar_matrices(pitchMat,yawMat),rollMat)
    
    def __makeVerts(self):
        self.transformedVerts = []
        self.textCoords = []
        # Para cada cara del selfo
        for face in self.faces:
            # Revisamos cuantos vértices tiene esta cara. Si tiene cuatro
            # vértices, hay que crear un segundo triángulo por cara
            vertCount = len(face)

            # Obtenemos los vértices de la cara actual.
            v0 = self.vertices[face[0][0] - 1]
            v1 = self.vertices[face[1][0] - 1]
            v2 = self.vertices[face[2][0] - 1]
            if vertCount == 4:
                v3 = self.vertices[face[3][0] - 1]

            # Si contamos con un Vertex Shader, se manda cada vértice
            # al mismo para transformarlos. Recordar pasar las matrices
            # necesarias para usarlas dentro del shader.
            if self.vertexShader:
                v0 = self.vertexShader(v0)
                v1 = self.vertexShader(v1)
                v2 = self.vertexShader(v2)

                if vertCount == 4:
                    v3 = self.vertexShader(v3)

            # Agregar cada vértice transformado al listado de vértices.
            self.transformedVerts.append(v0)
            self.transformedVerts.append(v1)
            self.transformedVerts.append(v2)
            if vertCount == 4:
                self.transformedVerts.append(v0)
                self.transformedVerts.append(v2)
                self.transformedVerts.append(v3)

            vt0 = self.texcoords[face[0][1]-1]
            vt1 = self.texcoords[face[1][1]-1]
            vt2 = self.texcoords[face[2][1]-1]
            if vertCount==4:
                vt3 = self.texcoords[face[3][1] - 1]

            self.textCoords.append(vt0)
            self.textCoords.append(vt1)
            self.textCoords.append(vt2)
            if vertCount==4:
                self.textCoords.append(vt0)
                self.textCoords.append(vt2)
                self.textCoords.append(vt3)

    def __createTraingles(self):
        self.TOBjects = []
        for i in range(0, len(self.transformedVerts), 3):
                # Un triángulo contará con las posiciones de sus vértices y
                # y sus UVs, seguidos uno tras otro.
                self.TOBjects.append(Triangle(material=self.material, 
                                              vertices=[self.transformedVerts[i],
                                                        self.transformedVerts[i + 1],
                                                        self.transformedVerts[i + 2]],txt=None))
    def calculate_bounds(self):
        min_X = self.transformedVerts[0][0]
        max_X = self.transformedVerts[0][0]
        min_Y = self.transformedVerts[0][1]
        max_Y = self.transformedVerts[0][1]
        min_Z = self.transformedVerts[0][2]
        max_Z = self.transformedVerts[0][2]
        for vert in self.transformedVerts[1:]:
            if vert[0] > max_X:
                max_X = vert[0] 
            if vert[0] < min_X:
                min_X = vert[0]
            if vert[1] > max_Y:
                max_Y = vert[1] 
            if vert[1] < min_Y:
                min_Y = vert[1]
            if vert[2] > max_Z:
                max_Z = vert[2] 
            if vert[2] < min_Z:
                min_Z = vert[2]
        self.minBox = [min_X,min_Y,min_Z]
        self.maxBox = [max_X,max_Y,max_Z]
    def isInsideBox(self, dir, origin):
        #x axis
        txMin = -float('inf')
        txMax = float('inf')
        if (dir[0] > 0) or (dir[0] < 0):
            txMin = (self.minBox[0] - origin[0])/dir[0]
            txMax = (self.maxBox[0] - origin[0])/dir[0]
            

        if (txMin > txMax):
            tmp = txMin
            txMin = txMax
            txMax = tmp
        #y axis
        tyMin = -float('inf')
        tyMax = float('inf')
        if (dir[1] > 0) or (dir[1] < 0):
            tyMin = (self.minBox[1] - origin[1])/dir[1]
            tyMax = (self.maxBox[1] - origin[1])/dir[1]
            

        if (tyMin > tyMax):
            tmp = tyMin
            tyMin = tyMax
            tyMax = tmp
        #z axis
        tzMin = -float('inf')
        tzMax = float('inf')
        if (dir[2] > 0) or (dir[2] < 0):
            tzMin = (self.minBox[2] - origin[2])/dir[2]
            tzMax = (self.maxBox[2] - origin[2])/dir[2]

        if (tzMin > tzMax):
            tmp = tzMin
            tzMin = tzMax
            tzMax = tmp
            
        tMin = min(txMin,tyMin)
        tMax = max(txMax,tyMax)

        if(txMin > tyMax) or (tyMin > txMax): return False
        if(tMin > tzMax) or (tzMin > tMax): return False

        return True 

