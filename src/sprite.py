'''
Created on Apr 7, 2012

@author: Demicow
'''
import  pygame

#Tie circle collion to self. leftside etc

class customSprite(pygame.sprite.DirtySprite):

    def __init__(self, scene, image, location):    
        #init the sprite!    
        pygame.sprite.DirtySprite.__init__(self)   
        
        #info about the screen            
        self.screen = scene.screen 
        self.map = scene.mainmap             
        self.screen_center = scene.screen_center 
        self.field_length = scene.field_length 
        self.field_height = scene.field_height      
        
        #load image
        self.imagemaster = pygame.image.load(image).convert_alpha()
        self.imagesize = (20,20)
        self.load_images()
        self.image = self.imagestill
        self.currentimage = self.imagefront
        
        self.rect = self.image.get_rect()
        self.radius = 10
        self.movement = 4
        #use same movement speed as map           
        self.speed = scene.mainmap.scroll_speed
                
        #variables for animation
        self.pause = 0
        self.delay = 11
        self.frame = 0
        
        #initial position
        self.x, self.y = location    
        
        #holds info about location for camera toggling purposes
        self.previouscenter = ((self.x, self.y), (scene.mainmap.camera.x, scene.mainmap.camera.y))
        
        
        #init variables to be used later
        self.animation_on = False
        self.collidedblock = None
        self.movingleft = False         
        self.rightside = self.leftside = self.topside = self.bottomside = False
        self.rect.x = self.x 
        self.rect.y = self.y
        
    def load_images(self):
        # load the image if the sprite is still
        self.imagestill = pygame.Surface(self.imagesize, pygame.SRCALPHA)        
        self.imagestill.blit(self.imagemaster, (0, 0), ((0,0), self.imagesize))
        
        #make a list of frames for the sprite viewed from the front
        self.imagefront= []        
        offsetfront = []
        for i in range(3):
            offsetfront.append((self.imagesize[0]*i,0*self.imagesize[1]))    
        for i in range(0,3):
            tmpimg = pygame.Surface(self.imagesize, pygame.SRCALPHA)            
            tmpimg.blit(self.imagemaster, (0, 0), (offsetfront[i], self.imagesize))          
            self.imagefront.append(tmpimg)
        
        #make a list of frames for the sprite viewed from the back  
        self.imageback= []        
        offsetback = []
        for i in range(3):
            offsetback.append((self.imagesize[0]*i,1*self.imagesize[1]))
        for i in range(0,3):
            tmpimg = pygame.Surface(self.imagesize, pygame.SRCALPHA)            
            tmpimg.blit(self.imagemaster, (0, 0), (offsetback[i], self.imagesize))           
            self.imageback.append(tmpimg)
            
        #make a list of frames for the sprite viewed from the side    
        self.imageside= []        
        offsetside = []
        for i in range(3):
            offsetside.append((self.imagesize[0]*i,2*self.imagesize[1]))
        for i in range(0,3):
            tmpimg = pygame.Surface(self.imagesize, pygame.SRCALPHA)            
            tmpimg.blit(self.imagemaster, (0, 0), (offsetside[i], self.imagesize))           
            self.imageside.append(tmpimg)
        
        

    
    def animation(self):
        #flip through the frames of animation
        if self.animation_on == True:
            delay = 10       
            
            self.pause += 1
            if self.pause >= delay:
                self.pause = 0
                self.frame += 1
                if self.frame >= len(self.currentimage):
                    self.frame = 0               
            
            self.image = self.currentimage[self.frame]
        else: self.image = self.currentimage[1]
          
   
    
                       
     
    def scroll_with_map_horizontal(self, scene):        
        if scene.mainmap.scrolling_right == True: 
            self.movingleft = False
            self.currentimage = self.imageside
           
        elif scene.mainmap.scrolling_left == True:
            self.currentimage = self.imageside  
            self.movingleft = True     
        
            
    def scroll_with_map_vertical(self,scene):  
        if scene.mainmap.scrolling_up == True:            
            self.currentimage = self.imageback
            
        elif scene.mainmap.scrolling_down == True:            
            self.currentimage = self.imagefront    
    
                        
        
    def update(self,scene):         
        self.animation()
               
        # Determines which blocks the sprite is colliding with. Had to tweak it a bit
        #to get it to recognize multiple blocks
        collidelist = self.rect.collidelistall(scene.mainmap.collisionblocks)
        blocklist =[scene.mainmap.collisionblocks[b] for b in collidelist]      
        if len(blocklist) > 0:
            for block in blocklist:
                self.check_block(block)
        else: self.rightside = self.leftside = self.topside = self.bottomside = False
        
       
            
        if scene.camera_focus is self:            
            self.check_bounds() 
            if self.movingleft == True:   
                self.flip()    
            else: pass
            
            self.rect.x = self.x 
            self.rect.y = self.y 
            
            if scene.mainmap.scrolling_mode_horizontal == True:
                self.scroll_with_map_horizontal(scene)
                self.x = scene.field_length/2
            else: pass
            
            if  scene.mainmap.scrolling_mode_vertical == True:
                self.scroll_with_map_vertical(scene)
                self.y = scene.field_height/2 
            else:  pass                     
            
               
        else:    
            #if camera is not focused on object
            #DO NOT CHANGE. Changing this will not help you.    
            
            if scene.mainmap.scrolling_up == True and scene.mainmap.at_top == False:                
                self.y += self.speed            
            elif scene.mainmap.scrolling_down == True and scene.mainmap.at_bottom == False:                
                self.y -= self.speed
            elif scene.mainmap.scrolling_right == True and scene.mainmap.at_right_side == False:
                self.x -= self.speed   
            elif scene.mainmap.scrolling_left == True and scene.mainmap.at_left_side== False:
                self.x  += self.speed  
            else: pass
            
            self.rect.x = self.x 
            self.rect.y = self.y 
            
         
        self.screen.blit(self.image, (self.rect.centerx, self.rect.centery), special_flags= 0)
              
    
            
    def check_bounds(self):     
        
        #keeps ya from walkin' off the edge        
        mapleft = 0
        mapright = self.map.rightedge
        maptop = 0
        mapbottom = self.map.bottomedge
       
        if self.rect.left < mapleft:            
            self.leftside = True
            
            
        if self.rect.top < maptop:
            self.topside = True
            
            
        if self.rect.right > mapright:
            self.rightside = True
            
            
        if self.rect.bottom > mapbottom:
            self.bottomside = True
            
        
    def flip(self):
        """ flips sprite horizontally"""        
        self.image = pygame.transform.flip(self.image, True, False)    
                  

                
   
    def check_block(self, block): 
        """
        This ended up getting a little complex. This code determines which side of a block the sprite is striking. The info is used by the
        do_input module.
        """
                
        offset = self.imagesize[0] -2
       
        #LEFT side of sprite
        if self.rect.left <= block.right and self.rect.right > block.centerx:              
            if self.rect.midleft[1] - block.midright[1]  < offset and self.rect.midleft[1] - block.midright[1] > -offset:                
                self.leftside = True            
           
        
        #RIGHT side of sprite
        if self.rect.right >= block.left and self.rect.left < block.centerx:  
            if self.rect.midright[1] - block.midleft[1]  < offset and self.rect.midright[1] - block.midleft[1] > -offset:   
                self.rightside = True            
            
        
        #TOP of sprite
        if self.rect.top <= block.bottom and self.rect.bottom> block.centery:                          
            if self.rect.midtop[0] - block.midbottom[0]< offset and  self.rect.midtop[0]- block.midbottom[0]> -offset:                       
                self.topside = True
                   
        #BOTTOM of sprite
        if self.rect.bottom >= block.top and self.rect.top< block.centery:             
            if self.rect.midbottom[0] - block.midtop[0] < offset and  self.rect.midbottom[0] - block.midtop[0] > -offset:   
                self.bottomside = True
            
    
    
