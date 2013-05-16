import pygame
import random



class MapTile(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        #makes a map tile. This is just a sprite with an image and a rect.
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


"""
To Make your map!  Look at the 'map1.png' file. This is a pixel representation of the larger map. The light green tiles are grass and
correspond with the first row of tiles in 'tileset.png'. the dark grey tiles are rocks and represent the second row. Trees are dark
green and represent the third row. Whatever pixels you make grey or dark green will put a rock or tree on that section of the map.
You can easily expand this system and have an easy way to make a map. 
 
 """       

class Map:


    def __init__(self, resolution):
        #init all our variables
        self.scrolling_up = False
        self.scrolling_down = False
        self.scrolling_right = False
        self.scrolling_left = False
        self.tiles = []
        self.camera = pygame.Rect((0, 0), resolution)        
        self.at_top = False
        self.at_right_side = False     
        self.at_left_side = False
        self.at_bottom = False
        self.scrolling_mode_horizontal = False   
        self.scrolling_mode_vertical = False
        #controls the speed the sprite walks around.
        self.scroll_speed = 2
        
        #loads the pixelmap.        
        self.pixelmap = pygame.image.load("images/map1.png").convert()
        self.map_width = self.pixelmap.get_width()
        self.map_height = self.pixelmap.get_height()
        self.mapsize = (self.pixelmap.get_width(),self.pixelmap.get_height())
        #if your tiles are bigger than this, change it here.
        self.tile_size  = (32,32)
        self.tile_size_x = self.tile_size[0]
        self.tile_size_y = self.tile_size[1]
        
        self.leftedge =  0
        self.rightedge = (self.map_width*self.tile_size_x ) - self.camera.w
        self.topedge = 0
        self.bottomedge = (self.map_height*self.tile_size_y) - self.camera.h

    def load_images(self):
        #loads our tile spritesheet
        self.tileset = pygame.image.load("images/tileset.png").convert_alpha()

               
        
    def check_bounds(self):
        #keeps the camera from sliding off the edge of the map, detects when it's 
        #at the edge of the map
        if self.camera.x <= 0:
            self.camera.x = 0
            self.at_left_side = True
        else: self.at_left_side = False
        
        
        if self.camera.x + self.camera.w >= self.map_width*self.tile_size_x :
            self.camera.x = (self.map_width*self.tile_size_x ) - self.camera.w
            self.at_right_side = True
        else: self.at_right_side = False
        
        if self.camera.y <= 0:
            self.camera.y = 0
            self.at_top = True            
        else: self.at_top = False
            
        if self.camera.y + self.camera.h >= self.map_height*self.tile_size_y :
            self.camera.y = (self.map_height*self.tile_size_y) - self.camera.h
            self.at_bottom = True            
        else: self.at_bottom = False
        
    
    def generate(self):
        #this is called once, at the beginning.
        
        
        self.tiles = []
        self.load_images()       
        mountaingrey = [128,128,128]
        treegreen = [0, 128, 64]
        self.bumplist = []
       
        for y in range(0, self.map_height):
            for x in range(0, self.map_width):  
                self.tile_size_x = self.tile_size[0]
                self.tile_size_y = self.tile_size[1]
                tile_image = pygame.surface.Surface(self.tile_size)
                color = list(self.pixelmap.get_at((x,y)) [:-1])
                #####WALL TILES
                if color == mountaingrey:   
                    bumprect = pygame.Rect(x*self.tile_size_x,y*self.tile_size_y, self.tile_size_x, self.tile_size_y)                 
                    self.bumplist.append(bumprect)                    
                    i = random.randint(1, 3)
                    if i == 1:
                        tile_image.blit(self.tileset, (0, 0), (self.tile_size_x, self.tile_size_y, self.tile_size_x, self.tile_size_y))
                    elif i == 2:
                        tile_image.blit(self.tileset, (0, 0), ((self.tile_size_x)*2, self.tile_size_y, self.tile_size_x, self.tile_size_y))
                    else:
                        tile_image.blit(self.tileset, (0, 0), (0, self.tile_size_y, self.tile_size_x, self.tile_size_y))    
                #### TREE TILES        
                elif color == treegreen:   
                                   
                    i = random.randint(1, 3)
                    if i == 1:
                        tile_image.blit(self.tileset, (0, 0), (self.tile_size_x, self.tile_size_y*2, self.tile_size_x, self.tile_size_y))
                    elif i == 2:
                        tile_image.blit(self.tileset, (0, 0), ((self.tile_size_x)*2, self.tile_size_y*2, self.tile_size_x, self.tile_size_y))
                    else:
                        tile_image.blit(self.tileset, (0, 0), (0, self.tile_size_y*2, self.tile_size_x, self.tile_size_y))
                ### GRASS TILES                
                else:
                    i = random.randint(1, 50)
                    if i == 1:
                        tile_image.blit(self.tileset, (0, 0), (self.tile_size_x, 0, self.tile_size_x, self.tile_size_y))
                    elif i == 2:
                        tile_image.blit(self.tileset, (0, 0), ((self.tile_size_x)*2, 0, self.tile_size_x, self.tile_size_y))
                    else:
                        tile_image.blit(self.tileset, (0, 0), (0, 0, self.tile_size_x, self.tile_size_y))
                        
                self.tiles.append(MapTile(tile_image, x*self.tile_size_x, y*self.tile_size_y))
      
    
    def focusing(self,scene):        
        key_pressed = pygame.key.get_pressed()         
                
        # SCROLLING TO THE LEFT
        if self.camera.x <= scene.field_length/2:    
            if scene.camera_focus.rect.x >= scene.field_length/2 - self.scroll_speed:                
                if self.at_left_side == True and  key_pressed[pygame.K_LEFT]:                               
                    self.scrolling_mode_horizontal = False                    
                else: 
                    self.scrolling_mode_horizontal = True
                   
                    
                           
        #SCROLLING TO THE RIGHT               
        if self.camera.x >= scene.field_length/2:  
            if scene.camera_focus.rect.x <= scene.field_length/2 + self.scroll_speed:
                              
                if self.at_right_side == True and  key_pressed[pygame.K_RIGHT]:                                   
                    self.scrolling_mode_horizontal = False                   
                else: 
                    self.scrolling_mode_horizontal = True
                                 
                        
                    
            
        #SCROLLING TO THE UP
        # I am so sorry about these random '4's. this is some kind of bug.
        if self.camera.y <= scene.field_height/2:            
               
            if scene.camera_focus.rect.y >= scene.field_height/2-self.scroll_speed*2:  
                
                if self.at_top == True and  key_pressed[pygame.K_UP]:       
                                                 
                    self.scrolling_mode_vertical = False                    
                else: 
                    self.scrolling_mode_vertical = True
                    
                    
                    
                
        #SCROLLING TO THE DOWN
        
        if self.camera.y >= scene.field_height/2: 
            
            if scene.camera_focus.rect.y <= scene.field_height/2 + self.scroll_speed*2:    
                                           
                if self.at_bottom == True and key_pressed[pygame.K_DOWN]:                                    
                    self.scrolling_mode_vertical = False            
                            
                else: 
                    self.scrolling_mode_vertical = True
                    
        
        else: pass
        
    
    def scroll_bumptiles(self):
        #this takes in the list of tiles you can't walk through, and 
        #returns a new list of those tile rect translated with the camera.        
        #collision_tiles_list = []
        
        for b in self.bumplist:
            if self.scrolling_up == True:
                b.y += self.speed
            elif self.scrolling_down == True:
                b.y -= self.speed
            elif self.scrolling_right == True:
                b.x -= self.speed
            elif self.scrolling_left == True:
                b.x += self.speed
    
    def update(self, scene, surface):  
        
        
        
         
        if scene.camera_focus is not None:
            self.focusing(scene)
          
                      
        self.check_bounds()
        self.collisionblocks = self.scroll_bumptiles()
        
        for tile in self.tiles:
            if self.camera.colliderect(tile):
                surface.blit(tile.image, (tile.rect.x - self.camera.x , tile.rect.y - self.camera.y), (0, 0, self.tile_size_x, self.tile_size_y))
