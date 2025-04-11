import pygame
#pip install shapely might need to run this for on the terminal for shapely.geometry to work
from shapely.geometry import Polygon, Point, LineString
import math
from itertools import chain


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
        #print("SHAPE ENCLOSED")
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
        #print("START OF PROCESS")
        enclosed_shape_coords = points #keep tracks of the enclosed shape
        unclaimed_coords = list(self.current_unclaimed_space.exterior.coords)[:-1] #coords for the shape of the unclaimed area
        #print(unclaimed_coords)
        start_point = points[0] #start of the push
        end_point = points[len(points)-1] #end of the push
        #finds closest point to the end of push
        closest_point = min(unclaimed_coords, key=lambda point: self.distance(point, end_point))
        #print(self.is_clockwise(unclaimed_coords))

        #print("CHECK ORIENTATION OF ENDPOINT")
        #print(self.check_general_direction(end_point))
        direction = self.check_general_direction(end_point) #of the exterior of the unclaimed area, what general direction is it facing
        
        unclaimed_coords_temp = list(self.current_unclaimed_space.exterior.coords)[:-1]
        unclaimed_coords = list(chain(unclaimed_coords_temp, [unclaimed_coords_temp[0]]))

        #forces clockwise orientation of unclaimed's vertices for easier comparison
        unclaimed_coords = self.make_clockwise(unclaimed_coords)
        #determine whether going cw (clockwise) or ccw through is each scenario
        #north facing line, closest point to LEFT of end point
        if direction == "N" and closest_point[0]<end_point[0] and closest_point[1]==end_point[1]: 
            unclaimed_coords = unclaimed_coords[1:][::-1] #reverse list (make ccw)
        #south facing line, closest point to RIGHT of end point
        elif direction == "S" and closest_point[0]>end_point[0] and closest_point[1]==end_point[1]:
            unclaimed_coords = unclaimed_coords[1:][::-1]
        #east facing line, closest point ABOVE  end point
        elif direction == "E" and closest_point[1]<end_point[1] and closest_point[0]==end_point[0]:
            unclaimed_coords = unclaimed_coords[1:][::-1]
        #west facing line, closest point BELOW end point
        elif direction == "W" and closest_point[1]>end_point[1] and closest_point[0]==end_point[0]:
            unclaimed_coords = unclaimed_coords[1:][::-1]

        #remove unecessary coords before the closest point
        #print("IS CLOCKWISE")
        #print(self.is_clockwise(unclaimed_coords))
        #print(unclaimed_coords)
        #print("TEST 1")
        #print(unclaimed_coords[unclaimed_coords.index(closest_point):-1])
        #print("TEST 2")
        #print(unclaimed_coords[:unclaimed_coords.index(closest_point)+1])
        remaining_coords = unclaimed_coords[unclaimed_coords.index(closest_point):-1] + unclaimed_coords[:unclaimed_coords.index(closest_point)+1]
        #print("REMAINING COORDS")
        #print(remaining_coords)
        #print(unclaimed_coords)

        #print("ORIGINAL")
        #print(enclosed_shape_coords)
        #trace the boundary of the unclaimed area until reach back to starting point
       
        #print(self.in_between(start_point,end_point,remaining_coords[0]))
        if not self.in_between(start_point,end_point,remaining_coords[0]):
            for i in range(len(remaining_coords)-1):
                enclosed_shape_coords.append(remaining_coords[i])
                if self.in_between(start_point,remaining_coords[i],remaining_coords[i+1]):
                    print("BREAK")
                    break
        
        return Polygon(enclosed_shape_coords)

    def check_general_direction(self,end_point):
        "given point (the end point) find what general direction it is facing"
        p1, p2 = self.find_edge_with_point(self.current_unclaimed_space, end_point)
        
        #print("CHECK EDGE")
        #print(p1)
        #print(p2)
        #print("DONE CHECK EDGE SEGMENT")
        dx, dy = p2[0]-p1[0], p2[1]-p1[1]
        ex , ey = end_point[0], end_point[1]
        surface = pygame.display.get_surface()
        if dx == 0:  # Vertical line (can be either facing E or W)
            if surface.get_at((int(ex+5),int(ey))) == self.bg_color or surface.get_at((int(ex+5),int(ey))) == (238,87,35):
                return "E"
            else:
                return "W"
        
        if dy == 0:  # Horizontal line (can be either facinge N or S)
            if surface.get_at((int(ex),int(ey-5))) == self.bg_color or surface.get_at((int(ex),int(ey-5))) == (238,87,35):
                return "N"
            else:
                return "S"

    def find_edge_with_point(self, polygon, point):
        "find the line segment that the point lies on"
        coords = list(polygon.exterior.coords)
        for i in range(len(coords)-1):
            edge = LineString([coords[i], coords[i+1]])
            if edge.contains(Point(point)):
                return coords[i], coords[i+1]
    
        return None, None
    
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
    
    def make_clockwise(self,points):
        "makes the orientation that the polygon points are drawn in to be clockwise"
        if not self.is_clockwise(points):
            return points[1:][::-1]
        return points
            
    
    def draw(self, window):
        "draws board to window"
        im = self.im
        pygame.draw.polygon(window,(252, 215, 203), list(self.current_unclaimed_space.exterior.coords))
        
        for i in self.current_border:
            #creates new border for marker to traverse
            pygame.draw.lines(window,'black', False, i,2)

