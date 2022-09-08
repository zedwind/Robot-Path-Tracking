import matplotlib.pyplot as plt 
import numpy as np
import math

class PathFeaturePoints():
    def __init__(self, map_path):
        with open("map.txt") as f:
            contents = f.read()
        contents = contents.split(' ')
        points = []
        for i in range(int(len(contents)/3)):
            temp_x = 100*float(contents[3*i])
            temp_y = 100*float(contents[3*i+1])
            temp_point = [temp_x,temp_y]
            points.append(temp_point)

        self.map = np.array(points)
        self.show_points(self.map)
    
    def filterMapSegmentId(self, mapSegmenId, theta = 1/4*np.pi):
        """
        筛选特征点,滤除转角小于theta的特征点
        """
        newSegmentId = []
        newSegmentId.append(mapSegmenId[0])
        for i in range(len(mapSegmenId)-2):
            tempAngle = self.calVectorAngle(self.map[mapSegmenId[i]],self.map[mapSegmenId[i+1]],self.map[mapSegmenId[i+2]])
            if(tempAngle >= theta):
                newSegmentId.append(mapSegmenId[i+1])
        
        newSegmentId.append(mapSegmenId[-1])

        for i in range(0,self.map.shape[0]):
                plt.scatter(self.map[i][0],self.map[i][1],marker='o',color='black')
                if(i < len(newSegmentId)):
                    plt.text(self.map[newSegmentId[i]][0],self.map[newSegmentId[i]][1],newSegmentId[i],size=12)
        plt.plot(np.array(self.map)[:,0],np.array(self.map)[:,1],color='black')#连线
        plt.show()

        return newSegmentId

    def findMapId(self, startId, endId, theta):
        """
        找到startId-endId的路径点内离由startId和endId组成的直线最远的点
        需要设定最小的距离阈值theta,theta越小找到的点就越全,越大找到的点越精确,默认为8
        """
        maxTempDist=0.0
        maxTempId = -1
        for i in range(startId,endId):
            tempLineDist = self.getLineDist(self.map[i],self.map[startId],self.map[endId])
            if(tempLineDist > maxTempDist):
                maxTempDist = tempLineDist
                maxTempId = i
        
        if(maxTempDist > theta):
            return maxTempId
        else:
            return -1
    
    def getSegmentId(self, require_filter=False):
        """
        通过连接路径点两端点成直线,不断迭代求两端点内路径点到直线最远点作为特征角点
        """
        mapSegmenId = []
        mapSegmenId.append(0)
        mapSegmenId.append(self.map.shape[0]-1)
        tempMapSegmentIdIndex = 0
        for i in range(mapSegmenId[tempMapSegmentIdIndex],mapSegmenId[tempMapSegmentIdIndex+1]):
            if(mapSegmenId[tempMapSegmentIdIndex] == (self.map.shape[0]-1) ):
                break
            tempMapSegmentId = self.findMapId(mapSegmenId[tempMapSegmentIdIndex],mapSegmenId[tempMapSegmentIdIndex+1],8.0)
            if(tempMapSegmentId>=0):
                mapSegmenId.append(tempMapSegmentId)
                mapSegmenId.sort()
            else:
                tempMapSegmentIdIndex = tempMapSegmentIdIndex +1

        #显示
        for i in range(0,self.map.shape[0]):
                plt.scatter(self.map[i][0],self.map[i][1],marker='o',color='black')
                if(i < len(mapSegmenId)):
                    plt.text(self.map[mapSegmenId[i]][0],self.map[mapSegmenId[i]][1],mapSegmenId[i],size=12)
        plt.plot(np.array(self.map)[:,0],np.array(self.map)[:,1],color='black')
        plt.show()

        if require_filter:
            self.filterMapSegmentId(mapSegmenId)

        return mapSegmenId

    def show_points(self, points):
        for i in range(0,points.shape[0]):
            plt.scatter(points[i][0],points[i][1],marker='o',color='black')
            plt.text(points[i][0],points[i][1],i,size=12)
        plt.plot(np.array(points)[:,0],np.array(points)[:,1],color='black')#散点连线
        plt.show()

    def getLineDist(self, p3, p1, p2):
        """
        p3(x3,y3)到由p1(x1,y1)和p2(x2,y2)构成的直线的距离
        L = abs( (y1-y2)x3+(x2-x1)y3+x1y2-y1x2 )/sqrt( (y1-y2)^2 + (x1-x2)^2 )
        """
        return abs((p1[1]-p2[1])*p3[0] + (p2[0]-p1[0])*p3[1] + p1[0]*p2[1] - p1[1]*p2[0]) / np.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)

    def calVectorAngle(self, p1, p2, p3):
        """
        计算3点组成两向量之间的夹角,返回夹角弧度
        """
        vector1 = [p2[0]-p1[0],p2[1]-p1[1]]
        vector2 = [p3[0]-p2[0],p3[1]-p2[1]]
        cosAngle = (vector1[0]*vector2[0] + vector1[1]*vector2[1]) / (np.sqrt(vector1[0]**2 + vector1[1]**2)*np.sqrt(vector2[0]**2 + vector2[1]**2))
        angle = math.acos(cosAngle)
        return angle
    


if __name__ == "__main__":
    PathFeaturePoints = PathFeaturePoints(map_path="map.txt")
    mapID = PathFeaturePoints.getSegmentId(require_filter=True)