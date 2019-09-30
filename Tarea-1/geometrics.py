import numpy as np

class Geometrics():

    def quadrilateral (self, cnt):
        return cnt.size == 4

    def rectangle(self, cnt, accuracy):
        return (self.quadrilateral(cnt) and np.angle(cnt) <= np.pi/2 - accuracy*(np.pi/2))

    def square(self, cnt, accuracy):
        pass

    def circle(self, cnt, accuracy):
        pass

    def geometric_type(self, cnt, accuracy):
        if rectangle(cnt, accuracy):
            return "rectangle"
        elif square(cnt, accuracy):
            return "square"
        elif circle(cnt, accuracy):
            return "circle"
        else:
            return "other"

    


    def find_geometrics(self, contours):
        dict_geometrics = {'rectangle':[], 'square':[], 'circle':[], 'other':[]}
        dict_found_geometrics = {k:(v.append(cnt)  for cnt in contours) for k,v in dict_geometrics.items() if geometric_type(cnt,accuracy) == k}

       

 
        
        



