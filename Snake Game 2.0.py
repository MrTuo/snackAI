# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:55:43 2015

@author: 妥明翔
"""


from Tkinter import*
import random 
class snack_game:
        #属性：
        direct = "left"
        dead = False
        eatten = True
        speed=200

        food_x=random.randrange(10,580,10)
        food_y=random.randrange(10,170,10)
        snack_x=random.randrange(10,550,10)
        snack_y=random.randrange(180,340,10)
        score=0
        X=[0,0,0]
        
        for i in range(3):
            X[i]=[snack_x+10*i,snack_y]
    
        '''View 模块'''
        def draw_wall(self):
            self.bg.create_rectangle(0,0,10,360,fill="red")
            self.bg.create_rectangle(590,0,600,360,fill="red")
            self.bg.create_rectangle(0,0,600,10,fill="red")
            self.bg.create_rectangle(0,350,600,360,fill="red")
            
        def draw_food(self):
            self.bg.delete("food")
            self.food_x=random.randrange(10,580,10)
            self.food_y=random.randrange(10,340,10)
            self.food=self.bg.create_rectangle(self.food_x,self.food_y,self.food_x+10,self.food_y+10,fill="orange"\
                                        ,tags="food")
         
        def draw_snack(self):
            self.bg.delete("snack")
            for i in self.X:
                    self.snack=self.bg.create_rectangle(i[0],i[1],i[0]+10,i[1]+10,fill="black"\
                                        ,tags="snack")
        def score_label(self):
            self.label.destroy()
            if self.eatten==True:
                self.score+=10
                print self.score
            self.label=Label(self.frame2,text="Score: "+str(self.score)) 
            self.label.pack()
        
        def draw_gameover(self):
            self.bg.delete("snack")
            self.bg.delete("food")
            self.over=self.bg.create_text((280,150),text="           Game Over!\n         Your score is "\
                                    +str(self.score)+"\n\n"\
                                     ,font='Helvetica -30 bold')
#                                    +"Press \"Enter \"to continue.\n"\
#                                    +"      Press \"Esc\" to exit."
#                                         
                                  
        '''Module 模块'''
        def is_eatten(self):
            self.eatten=False
            if self.X[0]==[self.food_x,self.food_y]:
                self.eatten=True
                
        def is_dead(self):
            self.dead=False         
            if (self.X[0][0] not in range(10,581)) or (self.X[0][1] not in range(10,351)):
                self.dead=True 
            else:
                for i in range(1,len(self.X)):
                    if self.X[i]==self.X[0]:
                        self.dead=True
                        break
                        
        def change_X(self):
            
            if self.direct =='left':
                self.X.insert(0,[self.X[0][0]-10,self.X[0][1]])
            elif self.direct=='up':
                self.X.insert(0,[self.X[0][0],self.X[0][1]-10])
            elif self.direct=='right':
                self.X.insert(0,[self.X[0][0]+10,self.X[0][1]])
            elif self.direct=='down':
                self.X.insert(0,[self.X[0][0],self.X[0][1]+10])           
            if self.eatten==False:    
                self.X.pop()
            
                    
        '''Control 模块'''
        def control(self,event):
            
            if event.keycode==37:
                self.direct='left'               
            elif event.keycode==38:
                self.direct='up'               
            elif event.keycode==39:
                self.direct='right'              
            elif event.keycode==40:
                self.direct='down'
            elif event.keycode==87:
                self.speed-=25
            elif event.keycode==83:
                self.speed+=25
                

           
        def main(self):
            
            self.window = Tk()
            self.window.geometry()
            self.window.maxsize(600,400)
            self.window.minsize(600,400)
            self.window.title("Snake game")
            
            self.frame1=Frame(self.window,relief=GROOVE)
            self.frame2=Frame(self.window,relief=RAISED,height=40,width=600)
            self.bg=Canvas(self.frame1,width=600,height=360,bg="white")
            for i in range(2):
                    self.bg.create_rectangle(self.X[i][0],self.X[i][1],self.X[i][0]+10,self.X[i][1]+10,fill="black"\
                                        ,tags='snack')
            self.label=Label(self.frame2,text="Score: "+str(self.score)) 
                      
            self.frame1.pack()
            self.frame2.pack(fill=BOTH)
            self.label.pack(side=LEFT)
            self.bg.pack(fill=BOTH)
            self.bg.bind('<Key>',self.control)
            self.bg.focus_set()
            self.draw_wall()             
            while self.dead == False:
                if self.eatten==True:    
                    self.draw_food()
                self.draw_snack()
                self.is_eatten()
                self.score_label()
                self.is_dead()
                self.change_X()

                self.bg.after(self.speed)
                self.bg.update()
            else:
                self.draw_gameover()
                
            self.window.mainloop()
            
snack_game=snack_game()
snack_game.main()

