#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""


#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror

#如果没有导入font,mixer模块  输出警告信息
if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')


main_dir = os.path.split(os.path.abspath(__file__))[0]
# 将当前文件的绝对位置的目录位置返回
# 实际上，该函数的分割并不智能，它仅仅是以 "PATH" 中最后一个 '/' 作为分隔符，
# 分隔后，将索引为0的视为目录（路径），将索引为1的视为文件名
# 如果当前文件包含在sys.path里面，那么，__file__返回一个相对路径！
# 如果当前文件不包含在sys.path里面，那么__file__返回一个绝对路径！
data_dir = os.path.join(main_dir, 'data')
# 进入当前文件同一目录下的data目录位置
# os.path.join() 具有合并目录的作用
# os.path.abspath(path)¶ 放回一个路径的绝地地址
# functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    # 合并成该image文件的目录,但是前提是该音乐文件必须在data目录下
    try:
        image = pygame.image.load(fullname)
        # 返回一个image对象
    except pygame.error:
    # 出现pygame.error类错误
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
        # 退出系统,并抛出该错误
    image = image.convert()
    # 更改图像的像素格式  将不同格式的图片统一操作
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
            # 获取image对象(0,0)点的色素
        image.set_colorkey(colorkey, RLEACCEL)
        # 设置Surface的当前颜色键。当将该表面贴
        # 图到目标上时，任何与该颜色具有相同颜色的像素
        # 都将是透明的。颜色可以是RGB颜色或映射的颜色整数。
        # 如果设置失败,则默认为没有设置
        # RLEACCEL 在非加速显示器提供更好的性能
    return image, image.get_rect()
    # 返回一个surface对象  和位置元组

def load_sound(name):
    class NoneSound:
    # 创建一个空的虚拟播放器
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
    # 如果不存在pygame.mixer 或者改模块未初始化成功
    # get_init() 成功返回True
        return NoneSound()
        # 采用空的虚拟播放器方法
        # 目的:就是为了让程序,不会因为一点小差错,而不能继续执行
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
        # 该方法返回一个Sound对象
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
        # 抛出错误信息 并退出程序
    return sound


#classes for our game objects
class Fist(pygame.sprite.Sprite):
    #继承Sprite类  该代码的最后放了Sprite类的代码
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        self.punching = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)
            # 检测碰撞

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # call Sprite intializer
        self.image, self.rect = load_image('chimp.bmp', -1)
        # 上面的参数是Sprite派生类必须分配的属性
        screen = pygame.display.get_surface()
        # 放回一个Surface对象
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        # Sprite派生类必须重新写的一个方法
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
            # \ 是续行的意思
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            # move（x，y） - > Rect 按照给定的偏移量移动
            self.image = pygame.transform.flip(self.image, 1, 0)
            # 猩猩的头换个方向
        self.rect = newpos

    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
            # 旋转图像可能会破坏像素吧  所以每次旋转完后还原
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((468, 60))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

#Put Text On The Background, Centered
    if pygame.font:
    # 看是否存在font模块
        font = pygame.font.Font(None, 36)
        text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
        # render(文本，抗锯齿，颜色，背景 = 无)- > Surface
        textpos = text.get_rect(centerx=background.get_width()/2)
        # get_rect（text，style = STYLE_DEFAULT，rotation = 0，size = 0） - > rect
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    chimp = Chimp()
    fist = Fist()
    allsprites = pygame.sprite.RenderPlain((fist, chimp))


#Main Loop
    going = True
    while going:
        clock.tick(60)
        # 限制游戏的运行速度

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play() #punch
                    chimp.punched()
                else:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()


# class Sprite(object):
# 简单的基类，用于可见的游戏对象。
# pygame.sprite.Sprite(*group): 返回Sprit  用于可视游戏对象的基类.
# 派生类需要重写Sprite.update()方法并分配Sprite.image和Sprite.rect属性.
# __init__(self, *groups)可以接受任意数量的组实例。精灵将成为其中的一员.
# 在向组添加精灵之前,在子类化Sprite类时，一定要调用__init__()方法
#     def __init__(self, *groups):
#         self.__g = {} # The groups the sprite is in
          # 应该是初始化一个精灵的时候,也给该精灵分配了一个组 只是组的内容为空
#         if groups:
#             self.add(*groups)
#
#     def add(self, *groups):
#         """add the sprite to groups
#
#         Sprite.add(*groups): return None
#
#         任何数量的组实例都可以作为参数传递.
#         精灵会被加入到它还不是一个成员的团体中.
#
#         """
#         has = self.__g.__contains__
#         for group in groups:
#             if hasattr(group, '_spritegroup'):
#                 if not has(group):
#                     group.add_internal(self)
#                     self.add_internal(group)
#             else:
#                 self.add(*group)
#
#
#     def remove(self, *groups):
#         """remove the sprite from groups
#
#         Sprite.remove(*groups): return None
#
#         Any number of Group instances can be passed as arguments. The Sprite
#         will be removed from the Groups it is currently a member of.
#
#         """
#         has = self.__g.__contains__
#         # __contains__():当使用in，not in 对象的时候
#         # 调用(not in 是在in完成后再取反,实际上还是in操作)
#         for group in groups:
#             if hasattr(group, '_spritegroup'):
#             # 如果对象有该属性返回 True，否则返回 False。
#                 if has(group):
#                 # 如果含有group这个值
#                     group.remove_internal(self)
#                     # group这个组删除此对象
#                     self.remove_internal(group)
#                     # 此对象删除这个组
#             else:
#                 self.remove(*group)
#
#     def add_internal(self, group):
#         self.__g[group] = 0
#         # 添加一个键值对 {group:0}
#     def remove_internal(self, group):
#         del self.__g[group]
#
#     def update(self, *args):
#         """method to control sprite behavior
#
#         Sprite.update(*args):
#
#         The default implementation of this method does nothing; it's just a
#         convenient "hook" that you can override. This method is called by
#         Group.update() with whatever arguments you give it.
#
#         There is no need to use this method if not using the convenience
#         method by the same name in the Group class.
#         就是这个方法需要你自己重新写
#         """
#
#         pass
#
#     def kill(self):
#         """remove the Sprite from all Groups
#
#         Sprite.kill(): return None
#
#         The Sprite is removed from all the Groups that contain it. This won't
#         change anything about the state of the Sprite. It is possible to
#         continue to use the Sprite after this method has been called, including
#         adding it to Groups.
#
#         """
#         for c in self.__g:
#             c.remove_internal(self)
#         self.__g.clear()
#
#     def groups(self):
#         """list of Groups that contain this Sprite
#
#         Sprite.groups(): return group_list
#
#         Returns a list of all the Groups that contain this Sprite.
#
#         """
#         return list(self.__g)
#
#     def alive(self):
#         """does the sprite belong to any groups
#
#         Sprite.alive(): return bool
#
#         Returns True when the Sprite belongs to one or more Groups.
#         """
#         return truth(self.__g)
#
#     def __repr__(self):
#         return "<%s sprite(in %d groups)>" % (self.__class__.__name__, len(self.__g))
#         # 重构__repr__方法后，不管直接输出对象还是通过print打印的信息都按我们__repr__方法中定义的格式进行显示了
#
