import pyglet
from random import randrange as rr
from random import random
import math
from math import sin, cos, tan,atan, acos, asin, pi
import Constants

class PhysicalObject(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = ''
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.shining_timer = 0
        self.intersectes = False
        self.vertex_color = (0,0,0)
        self.time = 0
        self.zero_pos = [self.x, self.y]
        self.prev_x = self.zero_pos[0]
        self.prev_y = self.zero_pos[1]
        self.app_center = (350,350)
        self.cc_size = 1

    def set_name(self, name):
        self.name = name


    def set_centers(self, app_center, cc_center):
        self.app_center = app_center
        self.cc_center = cc_center
        #self.radius = math.sqrt((self.x - self.app_center[0]) ** 2 + (self.y - self.app_center[1]) ** 2)
        if(Constants.MOTIONTYPE == 5):
            cc_coef = Constants.CC_RADIUS_COEF(self.cc_size)
            self.radius = cc_coef * math.sqrt((self.x - self.cc_center[0]) ** 2 + (self.y - self.cc_center[1]) ** 2)
            if(self.x - self.cc_center[0] > 0 ):
                if (self.y - self.cc_center[1] >= 0):
                    self.st_angle = atan((self.y - self.cc_center[1])/(self.x - self.cc_center[0]))
                else:
                    self.st_angle = 2*pi + atan((self.y - self.cc_center[1]) / (self.x - self.cc_center[0]))
            elif (self.x - self.cc_center[0] < 0):
                if (self.y - self.cc_center[1] >= 0):
                    self.st_angle = pi + atan((self.y - self.cc_center[1])/(self.x - self.cc_center[0]))
                else:
                    self.st_angle = pi + atan((self.y - self.cc_center[1]) / (self.x - self.cc_center[0]))
            else:
                if(self.y - self.cc_center[1] > 0):
                    self.st_angle = 90 / 180 * pi
                else:
                    self.st_angle = 270 / 180 * pi

        elif(Constants.MOTIONTYPE == 6):
            self.radius =  math.sqrt((self.x - self.app_center[0]) ** 2 + (self.y - self.app_center[1]) ** 2)
            if(self.x - self.app_center[0] > 0 ):
                if (self.y - self.app_center[1] >= 0):
                    self.st_angle = atan((self.y - self.app_center[1])/(self.x - self.app_center[0]))
                else:
                    self.st_angle = 2*pi + atan((self.y - self.app_center[1]) / (self.x - self.app_center[0]))
            elif (self.x - self.app_center[0] < 0):
                if (self.y - self.app_center[1] >= 0):
                    self.st_angle = pi + atan((self.y - self.app_center[1])/(self.x - self.app_center[0]))
                else:
                    self.st_angle = pi + atan((self.y - self.app_center[1]) / (self.x - self.app_center[0]))
            else:
                if(self.y - self.app_center[1] > 0):
                    self.st_angle = 90 / 180 * pi
                else:
                    self.st_angle = 270 / 180 * pi


    def directory_update(self, dt):
        if(Constants.MOTIONTYPE == 1):
            self.replace(dt)
        elif(Constants.MOTIONTYPE == 2):
            self.cardioida_replace(dt)
        elif (Constants.MOTIONTYPE == 3):
            self.limacon_replace(dt)
        elif (Constants.MOTIONTYPE == 4):
            self.perfec_heart_replace(dt)
        elif (Constants.MOTIONTYPE == 5):
            self.SCC_circle(dt)
        elif (Constants.MOTIONTYPE == 6):
            self.sircle_circle(dt)
        elif (Constants.MOTIONTYPE == 0):
            self.no_motion(dt)

    def crd(self):
        c = (self.x, self.y)
        return c

    def no_motion(self, dt):
        # 0
        self.time += dt
        #self.prev_x = self.x
        #self.prev_y = self.y
        #self.x = self.x
        #self.y = self.y
        if(Constants.ROTATION):
            self.rotation = self.rotation + self.rotate_speed * dt
        self.check_bounds()

    def replace(self,dt):
        # 1
        self.time += dt
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = self.x + self.velocity_x * dt
        self.y = self.y + self.velocity_y * dt
        self.rotation = self.rotation + self.rotate_speed * dt
        self.check_bounds()

    def cardioida_replace(self, dt):
        # 2
        self.time += dt
        self.prev_x = self.x
        self.prev_y = self.y
        a = 40
        self.x = self.zero_pos[0] + 2 * a * math.sin(self.time) - a * math.sin(2 * self.time)
        self.y = self.zero_pos[1] + 2 * a * math.cos(self.time) - a * math.cos(2 * self.time) - a
        self.rotation =  self.rotate_speed * dt
        self.check_bounds()

    def limacon_replace(self, dt):
        # 3
        self.time += dt
        self.prev_x = self.x
        self.prev_y = self.y
        a = 45
        b = 60
        self.x = self.zero_pos[0] + (b + a * math.cos(self.time)) * math.sin(self.time)
        self.y = self.zero_pos[1] - (b + a * math.cos(self.time)) * math.cos(self.time)
        self.rotation =  self.rotate_speed * dt
        self.check_bounds()

    def perfec_heart_replace(self, dt):
        # 4
        self.time += dt
        self.prev_x = self.x
        self.prev_y = self.y
        hearts_size = 10
        self.x = self.zero_pos[0] + hearts_size * 16 * (sin(self.time) ** 3)
        self.y = self.zero_pos[1] + hearts_size * (13 * cos(self.time) - 5 * cos(2* self.time) - 2 * cos(3*self.time) - cos(4*self.time))
        self.rotation = self.rotate_speed * dt
        self.check_bounds()

    def SCC_circle(self,dt):
        # 5
        self.time += dt
        self.prev_x = self.x
        self.prev_y = self.y
        if(self.cc_size == 1):
            pass
        else:
            self.x = self.cc_center[0] + self.radius * cos(self.time + self.st_angle)
            self.y = self.cc_center[1] + self.radius * sin(self.time + self.st_angle)
        self.rotation = self.rotate_speed * dt
        self.check_bounds()

    def sircle_circle(self, dt):
        # 6
        #print('RADIUS: {}'.format(self.radius))
        self.time += dt
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = self.app_center[0] + self.radius * cos(self.time + self.st_angle)
        self.y = self.app_center[1] + self.radius * sin(self.time + self.st_angle)
        self.rotation = self.rotate_speed * dt
        self.check_bounds()

    def check_bounds(self):
        min_x = 30
        min_y = 50
        max_x = Constants.SIZE_X - 30
        max_y = Constants.SIZE_Y - 30
        if(Constants.TRANSPARENCY):
            if self.x < min_x:
                self.x = max_x
            elif self.x > max_x:
                self.x = min_x
            if self.y < min_y:
                self.y = max_y
            elif self.y > max_y:
                self.y = min_y
        else:
            if self.x < min_x or self.x > max_x:
                self.velocity_x = - self.velocity_x
            if self.y < min_y or self.y > max_y:
                self.velocity_y = - self.velocity_y

    def change_direction(self, colisions):
        if(colisions == 0):
            return
            self.velocity_x = Constants.SPEED * ((-1) ** rr(2)) * rr(5, 15)
            self.velocity_y = Constants.SPEED * ((-1) ** rr(2)) * rr(5, 15)
        elif(colisions == 1):
            self.shining_timer = 10
            self.velocity_x = - self.velocity_x
            self.velocity_y = - self.velocity_y
        else:
            self.velocity_x = Constants.SPEED * ((-1) ** rr(2)) * rr(5, 15)
            self.velocity_y = Constants.SPEED * ((-1) ** rr(2)) * rr(5, 15)
            return
            self.velocity_x = 0
            self.velocity_y = 0

    def show_collision(self):
        if(Constants.COLLISIONS):
            image = pyglet.resource.image('images/cat.png')
            image.width = 50
            image.height = 80
            self.image = image
            self.color = (rr(255), rr(255), rr(255))
            #self.vertex_color = self.color

    def delete_collision(self):
        if (Constants.COLLISIONS):
            self.image = pyglet.resource.image('images/doge.png')
            self.image.width = 50
            self.image.height = 50
            self.color =  (255, 255, 255)
            # if(not FRACTAL):
            #     self.vertex_color = self.color

    def get_cntr(self):
        return (self.x, self.y)

    def explode(self):

        self.image = pyglet.resource.image('images/cat.png')
        self.image.width = 50
        self.image.height = 80