import pygame
from shapely.geometry import Polygon, Point



class Board:
    def __init__(self, screen_width, screen_length, initial_margin, window):
        self.screen_width = screen_width
        self.screen_length = screen_length
        self.initial_margin = initial_margin
        self.window = window

        #total board area at the start (unclaimed by marker)
        self.board_area = (screen_width-initial_margin)* (screen_length-initial_margin) 
        self.total_area_covered = 0         #total area marker has taken
        self.current_border = []            #list of list of tuples, indicate claimed area
        self.area_win_condition = 50        #percent of area to claim to win
    
    def update_border(self,points):
        """
        updates the border and area captured

        parameter:
        points (list of tuples): list of coordinates the marker traverses during push
        """
        self.total_area_covered += self.get_polygon_area(points)
        self.current_border.append(points)
    
    def get_polygon_area(self,points):
        "returns area of any polygon"
        num_points = len(points) #total number of points from given list
        points.append(points[0]) #add first point to end so shoelace theorem works
        area = 0
        for i in range(num_points):
            area += points[i][0]*points[i+1][1]
            area -= points[i][1]*points[i+1][0]
        return abs(area)/2

    def check_if_win(self):
        """
        Use to check win condition

        return:
        boolean whether or not win condition of area satisfied
        """
        return self.total_area_covered/self.board_area*100 >= self.area_win_condition
    
    def get_current_border(self):
        return self.current_border
    
    def draw(self, window):
        "draws board to window"
        for i in self.current_border:
            #specifically highlights claimed area in chosen colour
            pygame.draw.polygon(window, (255,0,0), i)
            #creates new border for marker to traverse
            pygame.draw.lines(window,'black', False, i,3)

