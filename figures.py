from algebra import *
from math import tan,pi,atan2,acos

class Intercept(object):
    def __init__(self,distance,point,normal,texcoords,obj):
        self.distance=distance
        self.point=point
        self.normal=normal
        self.texcoords = texcoords
        self.obj=obj
        
        

class Shape(object):
    def __init__(self,position,material):
        self.position = position
        self.material = material

    def ray_intersect(self,orig,dir):
        return None
    
class Sphere(Shape):
    def __init__(self,position,radius,material):
        self.radius = radius
        super().__init__(position,material)
        
    def ray_intersect(self,orig,dir):
        L = sub_vec(self.position,orig)
        lengthL = get_magnitude(L)
        tca = dot_vec(L,dir)
        d = (lengthL**2-tca**2)**0.5
        
        if d>self.radius:
            return None
        
        thc = (self.radius**2-d**2)**0.5
        t0 = tca-thc
        t1 = tca+thc
        
        if t0<0:
            t0=t1
        if t0<0:
            return None
        
        P = add_vec(orig,mul_veck(t0,dir))
        normal = sub_vec(P,self.position)
        normal = normalize_vec(normal)
        
        u = (atan2(normal[2],normal[0])/(2*pi))+0.5
        v = acos(normal[1])/pi

        return Intercept(distance=t0,
                         point=P,
                         normal=normal,
                         texcoords=(u,v),
                         obj=self)
    

class Triangle(Shape):
    def __init__(self,material,vertices,txt=None):
        self.A = vertices[0]
        self.B = vertices[1]
        self.C = vertices[2]
        self.txt = txt
        super().__init__((-1,-1,1),material)
 
    def ray_intersect(self,orig,dir):
        e1 = sub_vec(self.B, self.A)
        e2 = sub_vec(self.C, self.A)
        h = cros_vec(dir, e2)
        a = dot_vec(e1, h)
        # Bias
        if abs(a) < 0.00001:
            return None
        
        f = 1 / a
        s = sub_vec(orig, self.A)
        u = f * dot_vec(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = cros_vec(s, e1)
        v = f * dot_vec(dir, q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * dot_vec(e2, q)

        if t > 0.00001:
            intersect_point = add_vec(orig, mul_veck(t, dir))

            edge1 = sub_vec(self.B, self.A)
            edge2 = sub_vec(self.C, self.B)
            normal = cros_vec(edge1, edge2)
            normal = normalize_vec(normal)
            txtCoords = None
            if(self.txt):
                bc = barycentric_coords(self.A,self.B,self.C,intersect_point)
                if bc[0] >= 0 and bc[0] <= 1 and bc[1] >= 0 and bc[1] <= 1 and bc[2] >= 0 and bc[2] <= 1:
                    #vertex A texture coordinates
                    Tu =  bc[0] * self.txt[0][0] +  bc[1] * self.txt[1][0]  + bc[2] * self.txt[2][0] 
                    Tv =  bc[0] * self.txt[0][1] +  bc[1] * self.txt[1][1]  + bc[2] * self.txt[2][1]
                    txtCoords = (Tu,Tv)
            return Intercept(distance=t, point=intersect_point, normal=normal, texcoords=txtCoords, obj=self)

        return None
    
class Plane(Shape):
    def __init__(self,position,normal,material):
        self.normal = normalize_vec(normal)
        super().__init__(position,material)

    def ray_intersect(self,orig,dir):
        denom = dot_vec(dir,self.normal)
        
        if abs(denom)<=0.0001:
            return None
        
        num = dot_vec(sub_vec(self.position,orig),self.normal)
        t = num/denom
        
        if t<0:
            return None
        
        #P=O+D*t0
        P = add_vec(orig,mul_veck(t,dir))     
        return Intercept(distance=t,
                    point=P,
                    normal=self.normal,
                    texcoords=(P[0]%1,P[1]%1)  ,
                    obj=self)

class Disc(Shape):
    def __init__(self,position,normal,radius,material):
        self.normal = normalize_vec(normal)
        self.r = radius
        super().__init__(position,material)

    def ray_intersect(self,orig,dir):
        denom = dot_vec(dir,self.normal)
        
        if abs(denom)<=0.0001:
            return None
        
        num = dot_vec(sub_vec(self.position,orig),self.normal)
        t = num/denom
        
        P = add_vec(orig,mul_veck(t,dir))
        v = sub_vec(P,self.position)
        d2 = dot_vec(v,v)
        if d2 <= self.r**2:
            return Intercept(distance=t,
            point=P,
            normal=self.normal,
            texcoords=(P[0]%1,P[1]%1)  ,
            obj=self)
        return None
    
class Cube(Shape):
    #Axis Aligned Bounding Box
    
    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)
        
        self.planes = []
        self.size = size
        
        
        #Sides
        leftPlane = Plane(add_vec(self.position,[-size[0]/2,0,0]),(-1,0,0),material)
        rightPlane = Plane(add_vec(self.position,[size[0]/2,0,0]),(1,0,0),material)
        
        bottomPlane = Plane(add_vec(self.position,[0,-size[1]/2,0]),(0,-1,0),material)
        topPlane = Plane(add_vec(self.position,[0,size[1]/2,0]),(0,1,0),material)
    
        backPlane = Plane(add_vec(self.position,[0,0,-size[2]/2]),(0,0,-1),material)
        frontPlane = Plane(add_vec(self.position,[0,0,size[2]/2]),(0,0,1),material)
        
        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)
        
        #Bounds
        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]
        
        bias = 0.001
        
        for i in range(3):
            self.boundsMin[i] = self.position[i]-(bias+size[i]/2)
            self.boundsMax[i] = self.position[i]+(bias+size[i]/2)
            
    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')
        
        u = 0
        v = 0
        
        for plane in self.planes:
            planeIntersect = plane.ray_intersect(orig,dir)
            
            if planeIntersect is not None:
                planePoint = planeIntersect.point
                if self.boundsMin[0]<planePoint[0]<self.boundsMax[0]:
                    if self.boundsMin[1]<planePoint[1]<self.boundsMax[1]:
                        if self.boundsMin[2]<planePoint[2]<self.boundsMax[2]:
                            if planeIntersect.distance<t:
                                t = planeIntersect.distance
                                intersect = planeIntersect
                                
                                #Generar las uvs
                                if abs(plane.normal[0])>0:
                                    #Estoy en X, usamos Y y Z para crear las uvs
                                    u = (planePoint[1]-self.boundsMin[1])/(self.size[1]+0.002)
                                    v = (planePoint[2]-self.boundsMin[2])/(self.size[2]+0.002)
                                elif abs(plane.normal[1])>0:
                                    #Estoy en Y, usamos X y Z para crear las uvs
                                    u = (planePoint[0]-self.boundsMin[0])/(self.size[0]+0.002)
                                    v = (planePoint[2]-self.boundsMin[2])/(self.size[2]+0.002)
                                elif abs(plane.normal[2])>0:
                                    #Estoy en Z, usamos X y Y para crear las uvs
                                    u = (planePoint[0]-self.boundsMin[0])/(self.size[0]+0.002)
                                    v = (planePoint[1]-self.boundsMin[1])/(self.size[1]+0.002)

                                    
                                
        if intersect is None:
            return None
        
        return Intercept(distance=t,
                         point=intersect.point,
                         normal=intersect.normal,
                         texcoords=(u,v),
                         obj=self)


