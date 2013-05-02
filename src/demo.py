'''
Created on Mar 3, 2013

@author: DemiCow
'''
'''

'''

import pygame, sprite, map_generator, do_input




class Scene(object):
    def __init__(self):        
        pygame.init()        
        
        #variables relating to window size. 
        self.resolution = (800, 640)
        self.field_length = self.resolution[0]
        self.field_height = self.resolution[1]
        self.fullscreen = 0                    
        self.screen = pygame.display.set_mode(self.resolution)
        self.screen_center = ((self.resolution[0]/2), (self.resolution[1]/2))
        
        #this is very important. This is how often a key will repeat when held down.        
        pygame.key.set_repeat(1, 1)   
        #setting the icon and caption you feel like a real pro
        img_icon = pygame.image.load("images/icon.png")
        pygame.display.set_icon(img_icon)
        pygame.display.set_caption("TOP-DOWN MAP DEMO. Press SPACE to toggle camera focus, ESCAPE to exit.")       
        self.timer = 20
        #if running = false, the game ends 
        self.running = True   
        # I put the objects in their own function to keep things neat. That's optional.
        self.init_objects()       
        
        
    def init_objects(self):
        #init the map. Generate gets called once, actually builds the map.
        self.mainmap = map_generator.Map(self.resolution)  
        self.mainmap.generate()
        #init the sprites, args = self, image file location, initial position
        self.pixeldoll = sprite.customSprite(self, "images/pixeldoll.png", (100,100))  
        
          
        
        #set camera focus- first sprite in sprite list right now
        self.camera_focus = self.pixeldoll   
        
        self.previousstate = ([(self.pixeldoll.x,self.pixeldoll.y),(self.mainmap.camera.x, self.mainmap.camera.y)])
    
    def start(self):
        #this keeps the game running
        self.clock = pygame.time.Clock()
        while self.running:
            self.mainLoop()
 
    def stop(self):
        #stops the game
        self.running = False 
    
    def toggle_focus(self):    
        
        if self.camera_focus is None:
            newfocus = self.pixeldoll   
            self.mainmap.camera.x, self.mainmap.camera.y = self.previousstate[1]            
            
            self.pixeldoll.x,self.pixeldoll.y = self.previousstate[0]                
          
            
            self.camera_focus = newfocus            
                          
        else: 
            
               
            
            #STORE STATE OF OLD FOCUS
            self.previousstate[0] = self.camera_focus.x, self.camera_focus.y
            self.previousstate[1] = self.mainmap.camera.x, self.mainmap.camera.y
            self.camera_focus = None
            
        self.timer = 30
        
    
            
        
                        
    def mainLoop(self):
        #this stuff gets called every turn
        #this variable controls the framerate. remove to see how fast it can go.
        self.clock.tick(50)
        #uncomment this to see your framerate
        #print self.clock.get_fps()
        
        #update map, update sprites
        
        self.mainmap.update(self,self.screen)     
          
        
        
        self.pixeldoll.update(self) 
        
        #flip the display             
        pygame.display.flip()
        #call input function
        do_input.do_input(self)
        #timer to space out the toggle
        self.timer = self.timer - 1
       
        
        

def main():

    game = Scene()

    game.start()
if __name__ == "__main__":

    main()
