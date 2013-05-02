'''
Created on Apr 5, 2013

@author: DemiCow
'''

import pygame
"""
I broke this out into its own page to keep things simple, even though it's just one function. This gets called by the main loop once a turn. I'm getting the keyboard 
input with 'event' because we can space it out, instead of getting it once a frame. use 'key.set_repeat' in main function to control this. I know
this looks like a bit of a mess, but it's dealing with three cases. 1- no camera focus, 2- there's a camera focus but the camera is scrolling, and 3- the
camera is still and the sprite is moving around on its own. Within this it also controls whether the sprite's animation is going and whether it's
facing left (flipped).

"""


def do_input(scene):
    for event in pygame.event.get():   
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if scene.timer < 0:                        
                        scene.toggle_focus()  
                    else: pass
            if event.type == pygame.KEYDOWN:
                #sprite is animated if a key's being held down
                if scene.camera_focus is not None:
                    scene.camera_focus.animation_on = True
                #escape exits the game.    
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                #toggle camera focus    
                
                # if key pressed is the left arrow    
                if event.key == pygame.K_LEFT: 
                    #keeps non-focused sprites from scrolling the wrong way if 2 buttons are pressed at the same time.
                    scene.mainmap.scrolling_right =scene.mainmap.scrolling_up = scene.mainmap.scrolling_down = False
                    #if the camera is scrolling horizontal or there is no camera focus
                    if scene.mainmap.scrolling_mode_horizontal == True or scene.camera_focus == None:                        
                        #if there's no camera focus, scroll camera freely
                        if scene.camera_focus is None:
                            scene.mainmap.camera.x -= scene.mainmap.scroll_speed
                            scene.mainmap.scrolling_left = True 
                        #if there is, scroll camera, but don't walk through blocks    
                        elif scene.camera_focus is not None:
                            scene.mainmap.scrolling_left = True
                            scene.camera_focus.movingleft = True 
                            scene.camera_focus.currentimage = scene.camera_focus.imageside
                            #does nothing if you're walking into a wall
                            if scene.camera_focus.leftside == False:
                                scene.mainmap.camera.x -= scene.mainmap.scroll_speed
                    #sprite is walking around, camera not scrolling    
                    else:
                        scene.camera_focus.currentimage = scene.camera_focus.imageside
                        scene.camera_focus.movingleft = True 
                        if scene.camera_focus.leftside == False:
                            scene.camera_focus.x = scene.camera_focus.x - scene.camera_focus.speed
                        
                        
                elif event.key == pygame.K_RIGHT:
                    scene.mainmap.scrolling_left=scene.mainmap.scrolling_up = scene.mainmap.scrolling_down = False
                    if scene.mainmap.scrolling_mode_horizontal == True or scene.camera_focus == None:
                        
                        if scene.camera_focus is None:
                            scene.mainmap.scrolling_right = True
                            scene.mainmap.camera.x += scene.mainmap.scroll_speed
                                               
                        elif scene.camera_focus is not None:
                            scene.mainmap.scrolling_right = True
                            scene.camera_focus.movingleft = False
                             
                            scene.camera_focus.currentimage = scene.camera_focus.imageside
                            if scene.camera_focus.rightside == False:
                                scene.mainmap.camera.x += scene.mainmap.scroll_speed
                    else:
                        scene.camera_focus.currentimage = scene.camera_focus.imageside
                        scene.camera_focus.movingleft = False
                        if scene.camera_focus.rightside == False:
                            scene.camera_focus.x = scene.camera_focus.x + scene.camera_focus.speed
                        
                        
                elif event.key == pygame.K_UP:
                    scene.mainmap.scrolling_right =scene.mainmap.scrolling_left=scene.mainmap.scrolling_down = False
                    if scene.mainmap.scrolling_mode_vertical == True or scene.camera_focus == None:
                        
                        if scene.camera_focus is None:
                            scene.mainmap.scrolling_up = True
                            scene.mainmap.camera.y -= scene.mainmap.scroll_speed
                            scene.mainmap.scrolling_up = True 
                        elif scene.camera_focus is not None:
                            scene.mainmap.scrolling_up = True                            
                            scene.camera_focus.currentimage = scene.camera_focus.imageback
                            if scene.camera_focus.topside == False:
                                scene.mainmap.camera.y -= scene.mainmap.scroll_speed
                            else: pass
                    else:
                        scene.camera_focus.currentimage = scene.camera_focus.imageback
                        if scene.camera_focus.topside == False:          
                            scene.camera_focus.y = scene.camera_focus.y-scene.camera_focus.speed 
                        else: pass    
                        
                        
                elif event.key == pygame.K_DOWN:  
                    scene.mainmap.scrolling_right =scene.mainmap.scrolling_left=scene.mainmap.scrolling_up = False
                    if scene.mainmap.scrolling_mode_vertical == True or scene.camera_focus == None:
                        
                        if scene.camera_focus is None:
                            scene.mainmap.scrolling_down = True
                            scene.mainmap.camera.y += scene.mainmap.scroll_speed
                            scene.mainmap.scrolling_down = True 
                        elif scene.camera_focus is not None:   
                            scene.mainmap.scrolling_down = True                         
                            scene.camera_focus.currentimage = scene.camera_focus.imagefront
                            if scene.camera_focus.bottomside == False:
                                scene.mainmap.camera.y += scene.mainmap.scroll_speed
                            else: pass
                    else:
                        scene.camera_focus.currentimage = scene.camera_focus.imagefront
                        if scene.camera_focus.bottomside == False:
                            scene.camera_focus.y = scene.camera_focus.y + scene.camera_focus.speed 
                        else: pass
                    
                
            else:
                scene.mainmap.scrolling_right =scene.mainmap.scrolling_left=scene.mainmap.scrolling_up = scene.mainmap.scrolling_down = False 
                
                scene.pixeldoll.animation_on = False
                    
    
