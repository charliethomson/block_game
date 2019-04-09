
from pyglet.window import Window as pyg_Win
from pyglet.app import run as run_app
from pyglet.window.key import KeyStateHandler, W, A, S, D, LSHIFT, LCTRL, SPACE
from pyglet.clock import schedule
from pyglet.gl import *
from pyglet.image import load as load_img
from pyglet.graphics import Batch, TextureGroup
from math import sin, cos, pi

class Model:

    def get_texture(self, file):
        texture = load_img(file).texture
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return TextureGroup(texture)

    def __init__(self):
        self.batch = Batch()

        self.top = self.get_texture('./resources/grass_top.png')
        self.side = self.get_texture('./resources/grass_side.png')
        self.bottom = self.get_texture('./resources/dirt.png')

        x, y, z = 0, 0, -1
        X, Y, Z = x+1, y+1, z+1

        texture_coords = ('t2f', (0,0,1,0,1,1,0,1))

        self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z,  X, y, z,  X, Y, z,  x, Y, z)), texture_coords)

    def draw(self):
        self.batch.draw()


class Player:
    def __init__(self):
        # x, y, z
        self.pos = [0, 0, 0]
        self.rot = [0, 0]

    def update(self, delta, keys):
        s = delta * 10
        rot_y = self.rot[1] / 180*pi
        dx, dz = s * sin(rot_y), s * cos(rot_y)
        if keys[W]: self.pos[0] += dx
        if keys[A]: self.pos[2] -= dz
        if keys[S]: self.pos[0] -= dx
        if keys[D]: self.pos[2] += dz
        if keys[LSHIFT]: self.pos[1] += s
        if keys[LCTRL]:  self.pos[1] -= s




class Window(pyg_Win):

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self: self.lock, setLock)

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set3d(self):
        self.Projection()
        # fov, aspect ratio, min / max render dist
        gluPerspective(70, self.width / self.height, 0.05, 1000 )
        self.Model()

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.set_minimum_size(150, 100)
        self.model = Model()
        self.keys = KeyStateHandler()
        self.push_handlers(self.keys)

        self.player = Player()

    def update(self, delta):
        self.player.update(delta,self.keys)
        
        if self.keys[SPACE]:
            self.mouse_lock = not self.mouse_lock


    def on_draw(self):
        self.clear()
        self.set3d() 
        self.model.draw()
        glRotatef(-30, -70, 0,0)
        glTranslatef(0, 0, -2)
        print(self.player.pos)






if __name__ == "__main__":
    window = Window(1000, 1000)
    keys = KeyStateHandler()
    window.push_handlers(keys)

    ##
    glClearColor(0.5, 0.7, 1, 1)

    ##

    schedule(window.update)
    run_app()

