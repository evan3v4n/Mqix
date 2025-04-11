import pygame
#pip install shapely might need to run this for on the terminal for shapely.geometry to work
from shapely.geometry import Polygon, Point, LineString
import math

class Board:
    def __init__(self, screen_width, screen_length, initial_margin, window, bg_color):
        self.screen_width = screen_width
        self.screen_length = screen_length
        self.im = initial_margin
        self.window = window
        self.bg_color = bg_color

        
        self.total_area_covered = 0         #total area marker has taken
        self.current_border = []            #list of list of tuples, indicate borders
        im = self.im
        #Polygon of the unclaimed space
        self.current_unclaimed_space = Polygon([(im-1,im-1),(self.screen_length-1-im,im-1),
                                              (self.screen_width-1-im,self.screen_width-1-im),(im-1,self.screen_width-1-im)])
        #Polygon of the initial unclaimed space (use to keep track of how much area is claimed)
        self.initial_board = Polygon([(im-1,im-1),(self.screen_length-1-im,im),
                                              (self.screen_width-1-im,self.screen_width-1-im),(im-1,self.screen_width-1-im)])
        self.area_win_condition = 50        #percent of area to claim to win

        
    
    def update_border(self,points):
        """
        updates the border and area captured

        parameter:
        points (list of tuples): list of coordinates the marker traverses during push
        """
        #update border
        self.current_border.append(points)
        #create enclosed shape
        enclosed_shape=self.enclose_shape(points)
        #print(list(enclosed_shape.exterior.coords))
        #however enclosed shape may or may not be the right one, of the complement or the enclosed shape whichever has a smaller area
        if (self.current_unclaimed_space.difference(enclosed_shape)).area >= enclosed_shape.area: 
            self.current_unclaimed_space = self.current_unclaimed_space.difference(enclosed_shape)
        else:
            self.current_unclaimed_space = self.current_unclaimed_space.intersection(enclosed_shape)
        
        #print(list(self.current_unclaimed_space.exterior.coords))

    
    

    def check_if_win(self):
        """
        Use to check win condition

        return:
        boolean whether or not win condition of area satisfied
        """
        return self.current_unclaimed_space.area/self.initial_board.area*100 <= self.area_win_condition
    
    def get_current_border(self):
        return self.current_border
    
    def enclose_shape(self,points):
        """
        Find the enclosed shape when given points after a push

        parameter:
        points (list of tuples): list of coordinates the marker traverses during push

        return:
        Enclosed Polygon, new area that the push claims
        """
        enclosed_shape_coords = points #keep tracks of the enclosed shape
        unclaimed_coords = list(self.current_unclaimed_space.exterior.coords)[:-1][::-1] #coords for the shape of the unclaimed area
        #print(unclaimed_coords)
        start_point = points[0] #start of the push
        end_point = points[len(points)-1] #end of the push
        #finds closest point to the end of push
        closest_point = min(unclaimed_coords, key=lambda point: self.distance(point, end_point))
        #print(self.is_clockwise(unclaimed_coords))
        if self.is_clockwise(unclaimed_coords):
            if closest_point[1]<end_point[1] and closest_point[0]==end_point[0]: #if closest point is above end point
                unclaimed_coords.reverse()
            elif closest_point[0]>end_point[0] and closest_point[1]==end_point[1]: #if right of end point
                unclaimed_coords.reverse()
        else:
            if closest_point[1]>end_point[1] and closest_point[0]==end_point[0]: #if below end point
                unclaimed_coords.reverse()
            elif closest_point[0]<end_point[0] and closest_point[1]==end_point[1]: #if left of end point
                unclaimed_coords.reverse()
        #remove unecessary coords before the closest point
        remaining_coords = unclaimed_coords[unclaimed_coords.index(closest_point):] + unclaimed_coords[:unclaimed_coords.index(closest_point)]
        #print("REMAINING COORDS")
        #print(remaining_coords)

        #print("ORIGINAL")
        #print(enclosed_shape_coords)
        #trace the boundary of the unclaimed area until reach back to starting point
       
        #print(self.in_between(start_point,end_point,remaining_coords[0]))
        if not self.in_between(start_point,end_point,remaining_coords[0]):
            for i in range(len(remaining_coords)-1):
                enclosed_shape_coords.append(remaining_coords[i])
                if self.in_between(start_point,remaining_coords[i],remaining_coords[i+1]):
                    #print("BREAK")
                    break

        return Polygon(enclosed_shape_coords)
    
    def in_between(self, p, a, b):
        # For vertical line: x values are the same for both a and b
        if a[0]==b[0] and a[0]==p[0]:
            return a[1]<p[1]<b[1] or a[1]>p[1]>b[1]

        # For horizontal line: y values are the same for both a and b
        if a[1]==b[1] and a[1]==p[1]:
            return a[0]<p[0]<b[0] or a[0]>p[0]>b[0]

        # If the line is neither horizontal nor vertical, return False
        return False

    def distance(self,p1,p2):
        "simple distance formula"
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    
    def is_clockwise(self,points):
        "determines if the shape is defined clockwise or not"
        num_points = len(points) #total number of points from given list
        points.append(points[0]) #add first point to end so shoelace theorem works
        area = 0
        for i in range(num_points):
            area += points[i][0]*points[i+1][1]
            area -= points[i][1]*points[i+1][0]
        return (area)/2 > 0
    
    def draw(self, window):
        "draws board to window"
        im = self.im
        pygame.draw.polygon(window,self.bg_color, list(self.current_unclaimed_space.exterior.coords))
        
        for i in self.current_border:
            #creates new border for marker to traverse
            pygame.draw.lines(window,'black', False, i,2)

