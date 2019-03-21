import pyglet
from pyglet.window import key
from pyglet.window import mouse

from PhysicalObject import *
import Constants


class Application(pyglet.window.Window):
    def __init__(self, xs, ys, graph):
        super().__init__(width=xs, height=ys,visible=True)
        self._set_events_()
        self.graph = graph
        self.init()


    def init(self):

        # self.fancy_background = pyglet.sprite.Sprite(pyglet.image.load('images/back.jpg'), batch=self.batch)
        self.set_icon(pyglet.resource.image('source/100.png'))
        self.set_caption('Grapher!')
        # Connected components rotation direction: 1 - counter clockwize, -1 - clockwize, 0 - time stopped
        self.ROTATION_PREV_VAL = 1
        self.ROTATION = 1
        self.objects_num = len(self.graph.keys())
        self.batch = pyglet.graphics.Batch()
        self.Chosen_node = None
        self.CLEAR = False

        while(not self.nodes_creation()):
            pass

        self.create_colors()
        self.dist_from_cent_label = pyglet.text.Label('')
        self.graph_size_label = pyglet.text.Label('')
        self.mouse_pos_label = pyglet.text.Label('')
        self.chosen_node_label = pyglet.text.Label('')


    def create_colors(self):
        if(Constants.COLOR_PARTY):
            if(len(self.graph_colors.keys())>0):
                for i, name1 in enumerate(self.graph.keys()):
                    self.nodes_list[i].color = self.color_from_value(999)
                    for name2 in self.graph.keys():
                        if (name2 in self.graph[name1]):
                                self.graph_colors[(name1, name2)] = self.color_from_value(999)
        else:
            self.graph_colors = {}
            for i, name1 in enumerate(self.graph.keys()):
                self.nodes_list[i].color = self.color_from_value(0)
                for name2 in self.graph.keys():
                    if(name2 in self.graph[name1]):
                        if(Constants.COLORS or Constants.COLOR_PARTY):
                            self.graph_colors[(name1,name2)] = self.color_from_value(0)
                        else:
                            self.graph_colors[(name1, name2)] = self.color_from_value(0)
                    else:
                        self.graph_colors[(name1, name2)] = self.color_from_value(-1)

    def connect(self, pos1, pos2, color1 = (255,255,255), color2 = (255,255,255)):
        self.edges = self.batch.add(2, pyglet.gl.GL_LINES, None,
                                    ('v2i', (int(pos1[0]), int(pos1[1]),
                                             int(pos2[0]), int(pos2[1]))),
                                    ('c3B', (color1[0], color1[1], color1[2],
                                             color2[0], color2[1], color2[2])
                                     )
                                    )
        if (Constants.FRACTAL):
            pass
        else:
            self.edges.draw(pyglet.gl.GL_LINES)
            self.edges.delete()

    def nodes_creation(self):
        # TODO: ROUND RANDOM RADIUS
        self.nodes_list = []
        SCC = self.SCC_search()

        # Screen separation for clusters
        N = len(self.graph.keys())

        # Lines separation
        if(Constants.SEPARATION == 0):
            center = (self.width // 2, self.height // 2)
            screen_sep = [50]
            acc_val = 50
            for i in range(len(SCC)):
                #area = max((self.height - 100)* (len(SCC[i]) / N), 50))
                area = max((self.height - 100) * (len(SCC[i]) / N), 2)
                acc_val += int(area)
                screen_sep.append(acc_val)
                if(Constants.VISIBLE_SEP):
                    for i in range(len(screen_sep)):
                        self.edges = self.batch.add(2, pyglet.gl.GL_LINES, None,
                                                ('v2i', (0, screen_sep[i],
                                                         self.width, screen_sep[i])),
                                                ('c3B',
                                                 (255, 255, 255,
                                                  30, 194, 94)
                                                 )
                                                )
            #screen_sep.append(self.height - 50)
            print('SCREEN SEPARATION: {}'.format(screen_sep))

        # Round separation
        elif (Constants.SEPARATION == 1):
            round_sep = [0]
            round_val = 0
            center = (self.width//2, self.height//2)
            half_left = False
            for i in range(len(SCC)):
                if(half_left == False):
                    r_area = min((360) * len(SCC[i]) / N, 180)
                else:
                    if(N%2 == 1):
                        r_area = min((180) * len(SCC[i]) / ((N-1)/2), 180)
                    else:
                        r_area = min((180) * len(SCC[i]) / (N/2), 180)
                if(r_area == 180):
                    half_left = True
                    center = (self.width//2, self.height * len(SCC[i]) / N)
                round_val += int(r_area)
                if(i == len(SCC) -1):
                    round_val = 360
                round_sep.append(round_val)
                if (Constants.VISIBLE_SEP):
                    for i in range(len(round_sep)):
                        x_end = center[0] + self.height/1.5 * cos(pi/180 * round_sep[i])
                        y_end = center[1] - self.height/1.5 * sin(pi/180 * round_sep[i])
                        self.edges = self.batch.add(2, pyglet.gl.GL_LINES, None,
                                                    ('v2i', (int(center[0]), int(center[1]),
                                                             int(x_end), int(y_end))),
                                                    ('c3B',
                                                     (200, 200, 200,
                                                      94, 0, 0)
                                                     )
                                                    )
            #screen_sep.append(360)
                        print('SCREEN SEPARATION: {}'.format(round_sep))

        self.center = center
        separations_centers = []
        # Round structure
        if(Constants.SIRCLESTRUCTURE or True):
            if (len(SCC) == 1):
                separations_centers.append((self.width//2, self.height//2))
            elif (Constants.SEPARATION == 0):
                for i, el in enumerate(screen_sep):
                    if(i!=len(screen_sep)-1):
                        cen_x = self.width//2
                        cen_y = (screen_sep[i] + screen_sep[i+1])//2
                        separations_centers.append((cen_x, cen_y))
            elif (Constants.SEPARATION == 1):
                for i, el in enumerate(round_sep):
                    if(i!=len(round_sep)-1):
                        ang = (round_sep[i] + round_sep[i+1])//2
                        # radius = (self.width/2) * abs(cos(pi/180*ang))
                        radius = 0.8 * math.sqrt((self.width/2)**2 + (self.height/2)**2)/2
                        cen_x = self.width// 2 + radius * cos(pi/180 * ang)
                        cen_y = self.height// 2 - radius * sin(pi/180 * ang)
                        separations_centers.append((cen_x, cen_y))
        print("SEP CENTERS: {}".format(separations_centers))


        # Nodes creation
        Number_of_created_nodes = 0
        ones_cc = 0
        NEXT_ONE = -1
        SPLIT_FLAG = False
        for cc in SCC:
            if(len(cc) == 1):
                ones_cc += 1
        if(ones_cc >= 20):
            # if too many singular vertexes, we split them into a few lines
            SPLIT_FLAG = True

        for i, cc in enumerate(SCC,0):
            if(len(cc)==1):
                NEXT_ONE += 1
                if(ones_cc >= 20 and NEXT_ONE == ones_cc//2 ):
                    NEXT_ONE = 0
            cc_center = separations_centers[i]
            for j, node_name in enumerate(cc,0):

                if (Constants.SEPARATION == 1):
                    sector = int((round_sep[i + 1] - round_sep[i]) / len(cc))
                    if (j == 0):
                        st_angle = round_sep[i]
                    else:
                        st_angle = round_sep[i]+sector*j
                TimesPlaceNotFound = 0
                AllOk = False
                while (not AllOk):
                    if(TimesPlaceNotFound > 10):
                        print('FUCK, only {} nodes were created from {} '. format(Number_of_created_nodes, self.objects_num))
                        return True
                    AllOk = True
                    border = 20
                    mini_border = 1
                    sector_border = 2
                    if(Constants.SEPARATION == 0):
                        max_rad = 0
                        angle = 0
                        if(len(cc)==1):
                            if(SPLIT_FLAG):
                                left = int((self.width-border) * NEXT_ONE/ (ones_cc/2))
                                right =  int((self.width-border) * (NEXT_ONE+1)/(ones_cc/2))
                            else:
                                left = int((self.width - border) * NEXT_ONE / ones_cc)
                                right = int((self.width - border) * (NEXT_ONE + 1) / ones_cc)
                            node_x = self.width - rr(left, right)
                        else:
                            if(Constants.SIRCLESTRUCTURE):
                                angle = 360 / len(cc) * j
                                max_rad = 0.8 * (screen_sep[i+1] - screen_sep[i])/2
                                node_x = cc_center[0] + max_rad * cos(pi / 180 * angle)
                            else:
                                node_x =  int(rr(border , self.width - border))
                        if (Constants.SIRCLESTRUCTURE):
                            node_y = cc_center[1] - max_rad * sin(pi / 180 * angle)
                        else:
                            node_y = int(rr(screen_sep[i]+mini_border, screen_sep[i+1]-mini_border ))
                        if(node_x<0):
                            print('{} x_pos: {}'.format(node_name, node_x))
                    if(Constants.SEPARATION == 1):
                        # TODO: add sirclestructure !!!
                        if(Constants.SIRCLESTRUCTURE):
                            angle = 360 / len(cc) * j
                            max_rad = len(cc) * 10
                            node_x = cc_center[0] + max_rad * cos(pi / 180 * angle)
                            node_y = cc_center[1] - max_rad * sin(pi / 180 * angle)
                        else:
                            # angle = rr(round_sep[i] + mini_border,round_sep[i+1] - mini_border)
                            angle = rr(st_angle+sector_border, st_angle + sector-sector_border)
                            st_angle = angle
                            #radius = self.choose_round_position(center, angle)
                            radius = 1/2
                            # node_x = int(center[0] + rr(int(radius - 1)) * cos(pi/180 * angle))
                            # node_y = int(center[1] - rr(int(radius - 1)) * sin(pi / 180 * angle))

                            node_x = cc_center[0] + 250 * cos(pi/180 * angle)
                            node_y = cc_center[1] - 250 * sin(pi/180 * angle)

                    new_node_crd = (node_x, node_y)
                    for old_node in self.nodes_list:
                        if self.distance(new_node_crd, old_node.crd()) < Constants.TOLERANCE :
                            AllOk = False
                            TimesPlaceNotFound +=1
                            break

                if(not Constants.DOGS):
                    image = pyglet.resource.image('source/' + str(node_name) + '.png')
                else:
                    image = pyglet.resource.image('source/' + 'doge.png')
                image.anchor_x = image.width // 4
                image.anchor_y = image.height // 4
                size = 40
                image.width = size
                image.height = size

                new_node = PhysicalObject(img=image, x=node_x, y=node_y, batch=self.batch)
                Number_of_created_nodes += 1
                if(Constants.ROTATION):
                    new_node.rotation = rr(360)
                else:
                    new_node.rotation = 0
                new_node.velocity_x = Constants.SPEED * (-1) ** rr(2) * rr(5, 15)
                new_node.velocity_y = Constants.SPEED * (-1) ** rr(2) * rr(5, 15)
                new_node.rotate_speed = rr(5,30)
                new_node.set_name(node_name)
                print(cc_center)
                new_node.cc_size = len(cc)
                new_node.set_centers((self.width // 2, self.height // 2), cc_center)
                if (Constants.SEPARATION == 0):
                    print('noge {} is in ({} , {})'.format(new_node.name, new_node.x, new_node.y))
                if (Constants.SEPARATION == 1):
                    print('noge {} is in ({} , {})'.format(new_node.name, new_node.x, new_node.y))
                if(Constants.FRACTAL or Constants.TRASE or Constants.COLORS):
                    new_node.vertex_color = (rr(94,194),rr(94,194),rr(94,194))
                    #new_noge.color = new_noge.vertex_color
                else:
                    new_node.vertex_color = (255,255,255)
                self.nodes_list.append(new_node)
        self.center = center
        print('{} noges were created'.format(Number_of_created_nodes))
        for obj in self.nodes_list:
            pass
        return True

    def clear_batch(self):
        if(len(self.graph_colors.keys())):
            for key in self.graph_colors.keys():
                self.graph_colors.pop(key)

    def choose_round_position(self, center, angle):
        # node_x = center[0] + rr(int(radius - 1)) * cos(pi / 180 * angle)
        # node_y = center[1] + rr(int(radius - 1)) * sin(pi / 180 * angle)
        if (angle < 180 / pi * atan(self.width // 2 / (self.height - center[1]))):
            radius = self.width//2 * cos(pi / 180 * angle)
        elif (angle < 90):
            angle = 90 - angle
            radius = center[1] * cos(pi / 180 * angle)
            angle = 90 - angle
        elif (angle < 90 + 180 / pi * atan((self.width // 2)/center[1])):
            angle = angle - 90
            radius = center[1] * cos(pi / 180 * angle)
            angle = angle + 90
        elif (angle < 180):
            angle = 180 - angle
            radius = center[1] * cos(pi / 180 * angle)
            angle = 180 - angle
        elif (angle < 180 + 180 / pi * atan((self.height - center[1])/ (self.width // 2)) ):
            angle = angle - 180
            radius = self.width // 2 * cos(pi / 180 * angle)
            angle = angle + 180
        elif (angle < 270):
            angle = 270 - angle
            radius = (self.height - center[1]) * cos(pi / 180 * angle)
            angle = 270 - angle
        elif (angle < 270 + 180 / pi * atan(self.width // 2 / (self.height - center[1]))):
            angle = angle - 270
            radius = (self.height - center[1]) * cos(pi / 180 * angle)
            angle = angle + 270
        else:
            angle = 360 - angle
            radius = self.width // 2 * cos(pi / 180 * angle)
            angle = 360 - angle
        return radius

    def fractal_graph_creation(self):
        if(Constants.CONNECTIONS):
            for obj1 in self.nodes_list:
                for obj2 in self.nodes_list:
                    if(obj2.name in self.graph[obj1.name]):
                        col = self.graph_colors[(obj1.name, obj2.name)]
                        self.edges = self.batch.add(2, pyglet.gl.GL_LINES, None,
                                             ('v2i', (int(obj1.x), int(obj1.y),
                                                      int(obj2.x), int(obj2.y))),
                                             ('c3B', (col[0], col[1], col[2],
                                                      col[0], col[1], col[2])
                                              )
                                             )
                        # self.edges = self.batch.add(2, pyglet.gl.GL_LINES, None,
                        #                             ('v2i', (int(obj1.x), int(obj1.y),
                        #                                      int(obj2.x), int(obj2.y))),
                        #                             ('c3B',
                        #                              (obj1.vertex_color[0], obj1.vertex_color[1], obj1.vertex_color[2],
                        #                               obj2.vertex_color[0], obj2.vertex_color[1], obj2.vertex_color[2])
                        #                              )
                        #                             )
                        if(Constants.FRACTAL):
                            pass
                        else:
                            self.edges.draw(pyglet.gl.GL_LINES)
                            self.edges.delete()

    def color_from_value(self, value = 0):
        #print('VALUE = {}'.format(value))
        if (value == -1):
            return (0, 0, 0)
        elif (value == 0):
            return (255, 255, 255)
        elif(value == 1):
            return (255, 0, 0)
        elif (value == 2):
            return (0, 255, 0)
        elif (value == 3):
            return (0, 0, 255)
        else:
            return (rr(255),rr(255),rr(255))

    def trace_graph_creation(self):
        for obj1 in self.nodes_list:
            self.vertices = self.batch.add(2, pyglet.gl.GL_LINES, None,
                                 ('v2i', (int(obj1.x), int(obj1.y),
                                          int(obj1.prev_x), int(obj1.prev_y))),
                                 ('c3B', (obj1.vertex_color[0], obj1.vertex_color[1], obj1.vertex_color[2],
                                          obj1.vertex_color[0], obj1.vertex_color[1], obj1.vertex_color[2])
                                  )
                                 )
            if(Constants.TRASE):
                pass
            else:
                self.vertices.draw(pyglet.gl.GL_LINES)
                self.vertices.delete()

    def SCC_search(self):

        SCC = []
        visited = {}
        unobserved_nodes = []
        for node in self.graph.keys():
            visited[node] = False
            unobserved_nodes.append(node)
        for node in self.graph.keys():
            pass
        new_nodes = []
        i = -1
        while(len(unobserved_nodes)):
            node = unobserved_nodes[0]
            i +=1
            SCC.append([])
            stack = [node]
            unobserved_nodes.remove(node)
            while stack:
                vertex = stack.pop()
                if(vertex in unobserved_nodes):
                    unobserved_nodes.remove(vertex)
                if vertex not in SCC[i]:
                    SCC[i].append(vertex)
                    for ver in self.graph[vertex]:
                        if(not (ver in SCC[i])):
                            stack.append(ver)
                        if (vertex in unobserved_nodes):
                            unobserved_nodes.remove(ver)
        print('real SCC: {}'.format(SCC))
        # SCC = [[1, 5, 3, 9, 8, 4, 2, 7, 6], [11, 10, 12, 13], [16, 18, 17], [20, 19], [14, 15], [21, 22]]
        # print(SCC)

        def sortByElements(input):
            def sortByConnections(el):
                return len(self.graph[el])
            input.sort(key = sortByConnections, reverse = True)
            return len(input)
        SCC.sort(key = sortByElements, reverse = True)
        # print('SCC: {}'.format(SCC))

        return SCC

    def fill_creation(self):
        if (Constants.FILL):
            for obj1 in self.nodes_list:
                self.vertices = self.batch.add(2, pyglet.gl.GL_LINES, None,
                                     ('v2i', (int(obj1.x), int(obj1.y),
                                              int(obj1.zero_pos[0]), int(obj1.zero_pos[1]))),
                                     ('c3B', (obj1.vertex_color[0], obj1.vertex_color[1], obj1.vertex_color[2],
                                              obj1.vertex_color[0], obj1.vertex_color[1], obj1.vertex_color[2])
                                      )
                                     )

    def distance(self, point_1=(0, 0), point_2=(0, 0)):
        """Returns the distance between two points"""
        return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

    def collision_check(self, object_1, object_2):
        collision_distance = math.sqrt((object_1.image.width / 2 + object_2.image.width / 2) ** 2 +
                                       (object_1.image.height / 2 + object_2.image.height / 2) ** 2)
        pos_1 = (object_1.x, object_1.y)
        pos_2 = (object_2.x, object_2.y)
        actual_distance = self.distance(pos_1, pos_2)
        return (actual_distance <= collision_distance and actual_distance >= 0.0001)

    def center_image(self, image):
        """Sets an image's anchor point to its center"""
        image.x = image.width // 2
        image.x = image.height // 2

    def _set_events_(self):
        self.not_pressed = False
        self.on_draw = self.event(self.on_draw)
        self.on_key_press = self.event(self.on_key_press)
        # self.on_mouse_motion = self.event(self.on_mouse_motion)
        self.on_mouse_press = self.event(self.on_mouse_press)
        self.on_mouse_drag = self.event(self.on_mouse_drag)

    def on_draw(self):
        self.dist_from_cent_label.draw()
        self.graph_size_label.draw()
        self.mouse_pos_label.draw()
        self.chosen_node_label.draw()

    # def on_mouse_motion(self, x, y, dx, dy):
    #     pass

        #print(x,y)

    def print_distances(self):
        min_dist = 1000
        m1 = ''
        m2 = ''
        for node1 in self.nodes_list:
            for node2 in self.nodes_list:
                if(node1!=node2):
                    curr_dist = self.distance(node1.crd(), node2.crd())
                    if(curr_dist<min_dist):
                        m1 = node1.name
                        m2 = node2.name
                        min_dist = curr_dist
        print('Distance between {} and {} is {}'.format(m1,m2, min_dist))
        # print('Distanse from {} to {} is {}'.format(node1.name,
        #                                             node2.name,
        #                                             self.distance(node1.crd(), node2.crd())))

    def on_key_press(self, symbol, modifiers):
        if (self.not_pressed):
            self.not_pressed = not self.not_pressed
        else:
            Change_number = False
            self.not_pressed = not self.not_pressed
            if symbol == key.ENTER:
                self.batch = pyglet.graphics.Batch()
                while (not self.nodes_creation()):
                    pass
                print('Enter pressed')
            elif symbol == key.Z:
                self.print_distances()
            elif symbol == key.A:
                self.ROTATION = 1
                print('Back rotation')
            elif symbol == key.D:
                self.ROTATION = -1
                print('Forvard rotation')
            elif symbol == key.SPACE:
                if(self.ROTATION):
                    self.ROTATION_PREV_VAL = self.ROTATION
                    self.ROTATION = 0
                    print('Stop time')
                else:
                    self.ROTATION = self.ROTATION_PREV_VAL
                    print('Continue motion')
            elif symbol == key.Q:
                for node in self.nodes_list:
                    print('node {} is in ({},{})'.format(node.name, node.x, node.y))
            elif symbol == key.T:
                if(Constants.TRASE):
                    Constants.TRASE = False
                    print('TRASE DISACTIVATED')
                else:
                    Constants.TRASE = True
                    print('TRASE ACTIVATED')
            elif symbol == key.C:
                if(Constants.COLOR_PARTY):
                    Constants.COLOR_PARTY = False
                    self.create_colors()
                    print('PARTY DISACTIVATED')
                else:
                    Constants.COLOR_PARTY = True
                    self.create_colors()
                    print('PARTY ACTIVATED')
            elif symbol == key.BACKSPACE:
                self.CLEAR = True
            elif symbol == key.F:
                if(Constants.FRACTAL):
                    Constants.FRACTAL = False
                    print('FRACTALS DISACTIVATED')
                else:
                    Constants.FRACTAL = True
                    print('FRACTALS ACTIVATED')
            elif symbol == key.S:
                if(Constants.SIRCLESTRUCTURE):
                    Constants.SIRCLESTRUCTURE = False
                    print('SIRCLES DISACTIVATED')
                else:
                    Constants.SIRCLESTRUCTURE = True
                    print('SIRCLES ACTIVATED')
            elif symbol == key.L:
                if(Constants.SEPARATION):
                    Constants.SEPARATION = not Constants.SEPARATION
                    print('SEPARATION DISACTIVATED')
                else:
                    Constants.SEPARATION = not Constants.SEPARATION
                    print('SEPARATION ACTIVATED')
            elif symbol == key._0:
                Constants.MOTIONTYPE = 0
                print('New motion type is: {}'.format(Constants.MOTIONTYPE))
            elif symbol == key._1:
                Constants.MOTIONTYPE = 1
                print('New motion type is: {}'.format(Constants.MOTIONTYPE))
            elif symbol == key._2:
                Constants.MOTIONTYPE = 2
                print('New motion type is: {}'.format(Constants.MOTIONTYPE))
            elif symbol == key._3:
                Constants.MOTIONTYPE = 3
                print('New motion type is: {}'.format(Constants.MOTIONTYPE))
            elif symbol == key._4:
                Constants.MOTIONTYPE = 4
                print('New motion type is: {}'.format(Constants.MOTIONTYPE))
            elif symbol == key._5:
                Constants.MOTIONTYPE = 5
                print('New motion type is: {}'.format(Constants.MOTIONTYPE))
            elif symbol == key._6:
                Constants.MOTIONTYPE = 6
                print('New motion type is: {}'.format(Constants.MOTIONTYPE))
            # elif symbol == key._1:
            #     self.objects_num = 1
            #     Change_number = True
            # elif symbol == key._2:
            #     self.objects_num = 2
            #     Change_number = True
            # elif symbol == key._3:
            #     self.objects_num = 3
            #     Change_number = True
            # elif symbol == key._4:
            #     self.objects_num = 4
            #     Change_number = True
            # elif symbol == key._5:
            #     self.objects_num = 5
            #     Change_number = True
            # elif symbol == key._6:
            #     self.objects_num = 6
            #     Change_number = True
            # elif symbol == key._7:
            #     self.objects_num = 7
            #     Change_number = True
            # elif symbol == key._8:
            #     self.objects_num = 8
            #     Change_number = True
            # elif symbol == key._9:
            #     self.objects_num = 9
            #     Change_number = True
            # if(Change_number):
            #     self.batch = pyglet.graphics.Batch()
            #     self.nodes_creation()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
     if buttons & mouse.LEFT:
         if(not Constants.SIRCLESTRUCTURE):
             for node in self.nodes_list:
                 if (self.distance((x, y), (node.x, node.y)) <= 20):
                     node.color = (250, 0, 0)
                     self.Dragged_node = node
                     print(self.Dragged_node.width, self.Dragged_node.height)
                     break
                 else:
                     self.Dragged_node = None
                     node.color = (255, 255, 255)
             if (self.Dragged_node != None):
                self.Dragged_node.x = x
                self.Dragged_node.y = y
                self.Dragged_node.check_bounds()


    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.mouse_pos_label = pyglet.text.Label('Mouse position: ({} {})'.format(x, y),
                                                     font_name='Times New Roman',
                                                     font_size=22,
                                                     x=self.width // 2, y=50,
                                                     anchor_x='center', anchor_y='center')
            dist = int(self.distance(self.center, (x, y)))
            self.dist_from_cent_label = pyglet.text.Label('Distance from center: {}'.format(dist),
                                                          font_name='Times New Roman',
                                                          font_size=22,
                                                          x=self.width // 2, y=20,
                                                          anchor_x='center', anchor_y='center')
            for son1 in self.nodes_list:
                for son2 in self.nodes_list:
                    if (self.graph_colors[(son1.name, son2.name)] != (255, 255, 255)):
                        son1.color = (255, 255, 255)
                        son2.color = (255, 255, 255)
                        self.graph_colors[(son1.name, son2.name)] = (255, 255, 255)
                        self.graph_colors[(son2.name, son1.name)] = (255, 255, 255)

            for node in self.nodes_list:
                if (self.distance((x, y), (node.x, node.y)) <= 20):
                    node.color = (250, 0, 0)
                    self.Chosen_node = node
                    print(self.Chosen_node.width,self.Chosen_node.height)
                    break
                else:
                    self.Chosen_node = None
                    node.color = (255, 255, 255)
            if (self.Chosen_node != None):
                print(self.graph[self.Chosen_node.name])
                for son in self.nodes_list:
                    if (son.name in self.graph[self.Chosen_node.name]):
                        son.color = (0, 250, 0)
                        self.graph_colors[(self.Chosen_node.name, son.name)] = (250, 0, 0)
                        self.graph_colors[(son.name, self.Chosen_node.name)] = (250, 0, 0)
                self.chosen_node_label = pyglet.text.Label('Chosen node: {}'.format(self.Chosen_node.name),
                                                       font_name='Times New Roman',
                                                       font_size=22,
                                                       x=self.width // 2, y=80,
                                                       anchor_x='center', anchor_y='center')
            else:
                self.chosen_node_label = pyglet.text.Label('Chosen node not chosen',
                                                           font_name='Times New Roman',
                                                           font_size=22,
                                                           x=self.width // 2, y=80,
                                                           anchor_x='center', anchor_y='center')


    def collision_update(self):
        if(Constants.COLLISIONS):
            for obj1 in self.nodes_list:
                collisions = 0
                for obj2 in self.nodes_list:
                    if(self.collision_check(obj1,obj2)):
                        collisions += 1
                if(collisions):
                    if(not obj1.intersectes):
                        obj1.intersectes = True
                        obj1.change_direction(collisions)
                    else:
                        pass
                else:
                    if (obj1.intersectes):
                        obj1.change_direction(collisions)
                        obj1.intersectes = False
                    else:
                        pass

            for obj in self.nodes_list:
                if(obj.shining_timer > 1):
                    obj.show_collision()
                    obj.shining_timer -= 1
                elif(obj.shining_timer == 1):
                    obj.shining_timer -= 1
                    obj.delete_collision()
                else:
                    pass

    def update(self, dt):
        if(self.CLEAR):
            self.CLEAR = False
            #self.clear_batch()
        dt = self.ROTATION * dt
        self.graph_size_label = pyglet.text.Label('Current graph size: {}'.format(self.objects_num),
                                                  font_name='Times New Roman',
                                                  font_size=22,
                                                  x=self.width // 2, y=self.height - 30,
                                                  anchor_x='center', anchor_y='center')
        for obj in self.nodes_list:
            obj.directory_update(dt)
        self.collision_update()
        self.clear()
        self.fractal_graph_creation()
        self.trace_graph_creation()
        self.fill_creation()
        self.batch.draw()
        # for elem in self.nodes_list:
        #     print(elem.color)
