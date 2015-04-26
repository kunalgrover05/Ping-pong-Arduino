
#PONG pygame
from Tkinter import*
import tkMessageBox
import random
import pygame, sys
from pygame.locals import *
from time import sleep
from gattlib import GATTRequester, GATTResponse
import time
 
req = GATTRequester("EA:02:7F:9E:5F:7C", False)
req1 = GATTRequester("EC:C7:D5:05:67:BF", False)


#globals
WIDTH = 1600
HEIGHT = 840      
BALL_RADIUS = 20
PAD_WIDTH = 50
PAD_HEIGHT = HEIGHT
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 100
r_score = 100
area = 0 #Left is 0 and right is 1. Useful since we are communicating with 2 devices at once, so request only the one which is in the area
finish_flag = 0
r_score_extra = 0
l_score_extra = 0

hit_1 = 0
hit_2 = 0
global min_speed,max_speed

def easy():
    global min_speed,max_speed
    min_speed=2
    max_speed=4
    start_game()

def medium():
    global min_speed,max_speed
    min_speed=5
    max_speed=7
    start_game()

def hard():
    global min_speed,max_speed
    min_speed=8
    max_speed=10
    start_game()

def start_game():
    pygame.init()
    fps = pygame.time.Clock()

    #colors
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLACK = (0,0,0)
    sounds = {
        "ping" : pygame.mixer.Sound("data/ping.wav"),
        "click" : pygame.mixer.Sound("data/click.wav"),
        "da-ding" : pygame.mixer.Sound("data/da-ding.wav"),
        "warn1" :pygame.mixer.Sound("data/warn1.mp3"),
        "warn2" :pygame.mixer.Sound("data/warn2.mp3")
    }
    sounds["ping"].set_volume(5)
    sounds["click"].set_volume(5)
    sounds["da-ding"].set_volume(5)
    sounds["warn1"].set_volume(5)
    sounds["warn2"].set_volume(5)

    #canvas declaration
    window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('PING PONG')
     
    # helper function that spawns a ball, returns a position vector and a velocity vector
    # if right is True, spawn to the right, else spawn to the left
    def ball_init(right):
        global ball_pos, ball_vel # these are vectors stored as lists
        ball_pos = [WIDTH/2,HEIGHT/2]
        horz = random.randrange(min_speed,max_speed)
        vert = random.randrange(min_speed,max_speed)
         
        if right == False:
            horz = - horz
             
        ball_vel = [horz,-vert]
     
    # define event handlers
    def init():
        global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score
        global hit_1 ,hit_2   # these are floats
        global score1, score2  # these are ints
        paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT/2]
        paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT/2]
        l_score = 100
        r_score = 100
        if random.randrange(0,2) == 0:
            ball_init(True)
        else:
            ball_init(False)
     
     
    #draw function of canvas
    def draw(canvas):
        global hit_1 ,hit_2
        global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
        global finish_flag
        global req, req1, response, response1
        global l_score_extra, r_score_extra

        canvas.fill((255,255,0))
        pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
        pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
        pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)
     
        #update ball
        ball_pos[0] += int(ball_vel[0])
        ball_pos[1] += int(ball_vel[1])
     
        #draw paddles and ball
        pygame.draw.circle(canvas, BLACK, ball_pos, 20, 0)

 
        if int(ball_pos[0]) < WIDTH/2 :
            if not req.is_connected():
                try:
                    req1.disconnect()
                except:
                    pass
                req.connect(True)
                response = GATTResponse()   
                l_score_extra=0

            req.read_by_handle_async(0x000e, response)
            if response.received():
                # print "1 works"
                print "Reading data from 1 : " + str(ord(response.received()[-1]))
                hit_1 = ord(response.received()[-1])
                if hit_1 == 1:
                    l_score_extra += (ball_pos[0]*400)/WIDTH/float(WIDTH)
                    pygame.draw.polygon(window, RED, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
        else:    
            if not req1.is_connected():
                try:
                    req.disconnect()
                except:
                    pass
                req1.connect(True)
                response1 = GATTResponse()
                r_score_extra=0      
            
            req1.read_by_handle_async(0x000e, response1)
            if response1.received():
                # print "2 works"
                print "Reading data from 2 :" + str(ord(response1.received()[-1]))
                hit_2 = ord(response1.received()[-1])
                if hit_2 == 1:
                    r_score_extra += ((WIDTH-ball_pos[0])*400)/WIDTH/float(WIDTH)
                    pygame.draw.polygon(window, RED, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)
        
        #ball collision check on top and bottom walls
        if int(ball_pos[1]) <= BALL_RADIUS:
            ball_vel[1] = - ball_vel[1]
            sounds["da-ding"].play()
        if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
            ball_vel[1] = -ball_vel[1]
            sounds["da-ding"].play()
            # sounds["ping"].play()
        #ball collison check on gutters or paddles
        if int(ball_pos[0])<=200 and hit_1==0:
            sounds["warn1"].play()
        if int(ball_pos[0])>=1400 and hit_2==0:
            sounds["warn2"].play()
            
        if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1) and hit_1==1:
            ball_vel[0] = -ball_vel[0]
            sounds["click"].play()
            l_score -= int(l_score_extra)
            l_score_extra = 0
            # sounds["ping"].play()
        elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
            if not finish_flag:
                l_score -= 10
                l_score -= int(l_score_extra)
                l_score_extra = 0
            sounds["ping"].play()
            time.sleep(2)
            ball_init(True)
             
        if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1) and hit_2==1:
            ball_vel[0] = -ball_vel[0]
            sounds["click"].play()
            r_score -= int(r_score_extra)
            r_score_extra = 0
            
        elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
            if not finish_flag:
                r_score -= 10
                r_score -= int(r_score_extra)
                r_score_extra = 0
            sounds["ping"].play()
            time.sleep(2)
            ball_init(False)
     
        #update scores
        myfont1 = pygame.font.SysFont(None,48)
        myfont2 = pygame.font.SysFont(None,48)
        if l_score>0 and r_score>0:
                myfont1.set_underline(1)
                label1 = myfont1.render("PLAYER1", 1, (0,0,0))
                myfont1.set_underline(0)
                label5 = myfont1.render(str(l_score), 1, (0,0,0))
                myfont2.set_underline(1)
                label2 = myfont2.render("PLAYER2", 1, (0,0,0))
                myfont2.set_underline(0)
                label6 = myfont2.render(str(r_score), 1, (0,0,0))
                canvas.blit(label1, (250,20))
                canvas.blit(label2, (1050, 20)) 
                canvas.blit(label5, (290,65))
                canvas.blit(label6, (1090,65)) 
        else:
            finish_flag = 1
            if l_score>r_score:
                label1=myfont1.render("WIN", 1, (0,255,0))
                label2=myfont2.render("LOST",1, (255,0,0))
                canvas.blit(label1, (250,20))
                canvas.blit(label2, (1050, 20)) 
            elif r_score>l_score:
                label1=myfont1.render("LOST",1, (255,0,0))
                label2=myfont2.render("WIN" ,1, (0,255,0))
                canvas.blit(label1, (250,20))
                canvas.blit(label2, (1050, 20))
            else:
                label3=myfont1.render("MATCH DRAW",1, (0,0,255))
                canvas.blit(label3, (850,20))
     
    
    init()
    pause = False
    while True: 
        draw(window)            
        if finish_flag==1:
            myfont1 = pygame.font.SysFont(None,80)    
            labelGame = myfont1.render("Game Over", 1, (0,0,0))
            myfont2 = pygame.font.SysFont(None,30)    
            labelGame2 = myfont2.render("Press any key", 1, (0,0,0))
            window.blit(labelGame, (WIDTH/2-150,500))
            window.blit(labelGame2, (WIDTH/2-50,700))
            pygame.display.update()
            pause = True
            while pause:
                for event in pygame.event.get():
                    if event.type==KEYUP:
                        pygame.quit()   
                        delete_connections()
                        sys.exit()

                    elif event.type == QUIT:
                        pygame.quit()   
                        delete_connections()
                        sys.exit()
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                delete_connections()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    pause = True
                    myfont1 = pygame.font.SysFont(None,80)
                    labelPause = myfont1.render("Pause", 1, (0,0,0))
                    window.blit(labelPause, (WIDTH/2-100,500))
                    pygame.display.update()
                    while pause:
                        for event in pygame.event.get():
                            if event.type==KEYUP:
                                if event.key==K_SPACE:
                                    pause = False
                            elif event.type == QUIT:
                                pygame.quit()
                                delete_connections()
                                sys.exit()
                 
        pygame.display.update()
        fps.tick(40)

def initialize():
    try:
        req.connect(True)
        req.disconnect()
        print "connected 1"

        req1.connect(True)
        req1.disconnect()
        print "connected 2"
        return True

    except:
        print "Error connecting"
        print "Shutting down"
        pygame.quit()
        delete_connections()
        sys.exit()
                 
        try:
            print "disconnect 1"
            req.disconnect()
        except Exception, e:
            pass
        try:
            print "disconnect 2"
            req1.disconnect()
        except Exception, e:
            pass

def delete_connections():
    global req, req1
    try:
        req.disconnect()
    except: 
        pass

    try:
        req1.disconnect()
    except: 
        pass
    
def instructions():
    tkMessageBox.showinfo( "INSTRUCTIONS", "Click the start button and choose the game level.                           Each player controls one paddle using the right switch on your board, you can only hit with the paddle when the ball is in your area.       Use spacebar to pause and resume the game.           GOAL: HIT THE BALL WHEN IT COMES TO YOUR AREA.            Game Rules:                                     1. Both players start with 100 points each.                                                             2. If the player fails to hit the ball, lose 10 points.                                        3. The more time you press the paddle for, the more points you lose. Try to be precise.                                        4. First one to lose all points, loses the game.")

def play():
    tkMessageBox.showinfo("Select a game mode.")

def main_part():
    top=Tk()
    C = Canvas(top, bg="white", height=840, width=1600)
    C.pack(side="top", fill="both", expand=True)
    canvas_id = C.create_text(650, 20, anchor="nw")
    C.itemconfig(canvas_id, text="PING PONG",font=("Helvetica",48,"bold"))

    C.grid()

    C.create_oval(700, 28, 710, 38, outline="#ff0000", fill="#ff0000", width=2)
    C.create_oval(720, 18, 730, 28, outline="#ff1919", fill="#ff1919", width=2)
    C.create_oval(740, 12, 750, 22, outline="#ff3232", fill="#ff3232", width=2)
    C.create_oval(760, 16, 770, 26, outline="#ff4c4c", fill="#ff4c4c", width=2)
    C.create_oval(780, 28, 790, 38, outline="#ff6666", fill="#ff6666", width=2)
    C.create_oval(800, 18, 810, 28, outline="#ff7f7f", fill="#ff7f7f", width=2)
    C.create_oval(820, 12, 830, 22, outline="#ff9999", fill="#ff9999", width=2)

    button4 = Button(None, text = "PLAY GAME",font=("Helvetica",24,"bold"), command = None, anchor = W)
    button4.configure(width = 20, activebackground = "red", bg="red",relief = FLAT)
    button4_window = C.create_window(650, 180, anchor=NW, window=button4)

    button1 = Button(None, text = "EASY",font=("Helvetica",24,"bold"), command = easy, anchor = W)
    button1.configure(width = 20, activebackground = "#ffc100", bg="#ff9999",relief = FLAT)
    button1_window = C.create_window(650, 240, anchor=NW, window=button1)

    button5 = Button(None, text = "MEDIUM",font=("Helvetica",24,"bold"), command = medium, anchor = W)
    button5.configure(width = 20, activebackground = "#ffc100", bg="#ff6666",relief = FLAT)
    button5_window = C.create_window(650, 300, anchor=NW, window=button5)

    button6 = Button(None, text = "HARD",font=("Helvetica",24,"bold"), command = hard, anchor = W)
    button6.configure(width = 20, activebackground = "#ffc100", bg="#ff3232",relief = FLAT)
    button6_window = C.create_window(650, 360, anchor=NW, window=button6)

    button2 = Button(None, text = "INSTRUCTIONS",font=("Helvetica",24,"bold"), command = instructions, anchor = W)
    button2.configure(width = 20, activebackground = "#ffc100", bg="red",relief = FLAT)
    button2_window = C.create_window(650, 440, anchor=NW, window=button2)

    button3 = Button(None, text = "EXIT",font=("Helvetica",24,"bold"), command = top.quit, anchor = W)
    button3.configure(width = 20, activebackground = "#ffc100", bg="red",relief = FLAT)
    button3_window = C.create_window(650, 520, anchor=NW, window=button3)
                    
    C.pack()
    top.mainloop()

val = initialize()
main_part()