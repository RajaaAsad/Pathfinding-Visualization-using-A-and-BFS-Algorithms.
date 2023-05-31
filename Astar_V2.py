# features:
#1. For the A* algorithm,  will print the f function for each iteration and each neighbor.

#2. If there is no path from the start spot to the end spot, the program will print "NO Path".
#3. After running the algorithm, the program will print the total cost of the path.
#4. To select an algorithm, press 'A' to run the A* algorithm or 'B' to run the BFS algorithm.



import pygame
from queue import PriorityQueue
pygame.init()
pygame.font.init()




WIDTH = 700
WIN=pygame.display.set_mode((WIDTH, WIDTH))
font=pygame.font.SysFont("monospace",15)
font2=pygame.font.SysFont("monospace",30)

pygame.display.set_caption("A* Path Finding ")

#colors Const
RED=(198,2,80)     #CLOSE
GREEN=(245,171,200)   #OPEN
BLUE=(252,0,0)    #END
 
WHITE=(255,255,255)  
BLACK=(0,0,0)  
GRAY=(128,128,128)
PURPLE=(43,218,78)   #PATH
ORANGE=(84,72,173)   #START
NOPATH=(0,255,0)




class Spot:
    def __init__(self,row,col,width,total_rows):
        self.row=row
        self.col=col
        self.x=row*width
        self.y=col*width
        self.width=width
        self.color=WHITE
        self.neighbors=[]
        self.total_rows=total_rows
    
    def get_pos(self):
        return self.row,self.col
    
    def is_closed(self):
        return self.color==RED
    def is_barrier(self):
        return self.color==BLACK
    def is_open(self):
        return self.color==GREEN
    def is_start(self):
        return self.color==ORANGE
    def is_end(self):
        return self.color==BLUE
    
    def reset(self):
        self.color=WHITE

    def make_close(self):
        self.color=RED
     
    def writex(self,s):
        
         label = font.render(s, 0, BLACK)
         WIN.blit(label, (self.x,self.y))

    def make_open(self):
        self.color=GREEN
    def make_barrier(self):
        self.color=BLACK
    def make_start(self):
        self.color=ORANGE
    def make_end(self):
        self.color=BLUE
    def make_path(self):
         self.color=PURPLE
        
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width)) 

    def update_neighbors(self,grid):
        self.nbors=[]
        #DOWN 
        if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
             self.nbors.append(grid[self.row+1][self.col])
        #UP 
        if self.row>0 and not grid[self.row-1][self.col].is_barrier():
             self.nbors.append(grid[self.row-1][self.col]) 
        #LEFT
        if self.col>0 and not grid[self.row][self.col-1].is_barrier():
             self.nbors.append(grid[self.row][self.col-1])
        #RIGHT
        if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
             self.nbors.append(grid[self.row][self.col+1])             


    
def make_grid(rows,width):
        grid=[]
        gap=width//rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot=Spot(i,j,gap,rows)
                grid[i].append(spot)
        return grid
    
def h(p1,p2):
        x1,y1=p1
        x2,y2=p2
        return abs(x1-x2)+abs(y1-y2)

def draw_grid(win,rows,width):
        gap=width//rows
        for i in range(rows):
            pygame.draw.line(win,GRAY,(0,i*gap),(width,i*gap))
            for j in range(rows):
                pygame.draw.line(win,GRAY,(j*gap,0),(j*gap,width))
                
def draw(win,grid,rows,width):
        win.fill(WHITE)
        for row in grid:
            for spot in row:
                spot.draw(win)
        draw_grid(win,rows,width)
        pygame.display.update()
        pygame.time.delay(200)

        
def get_clicked_pos(pos,rows,width):
    gap=width//rows
    y,x=pos
    col=x//gap
    row=y//gap
    return row,col

def path(came_from,cur,end,draw,g=None):
     end.make_end()
     cur=came_from[cur]
     c=0
     while cur in came_from:
      cur.make_path()
      cur=came_from[cur]
      c=c+1
      draw()

     if g!=None:
          totalCost=g
     else:
          totalCost=c+1
     text = font2.render('Cost From start to End', 1, NOPATH)
     cost= font2.render(str(totalCost), 1, NOPATH)
     WIN.blit(text,(50,50)) 
     WIN.blit(cost,(500,100))
     pygame.display.update()
     pygame.time.delay(9000)

def algorithmBFS(draw,grid,start,end):
     queue =[]
     visited=[]
     queue.append(start)
     visited.append(start)

     came_from={} 


     while queue:
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

          cur=queue.pop(0)   #Remove and return an item from the queue

          if cur==end:
               path(came_from,cur,end,draw) 
               return True
          
          for n in cur.nbors:
               if n not in visited and not n.is_barrier():
                    queue.append(n)
                    visited.append(n)
                    if not n.is_end():
                         n.make_open()
                    came_from[n]=cur
          draw()  

          if cur!=start:
               cur.make_close()
     return False        




def algorithmA_Star(draw,grid,start,end):
     count=0
     open_set=PriorityQueue()
     open_set.put((0,count,start))  #f(n),count,node
     open_set_hash={start}
     came_from={}                                                  #child:parent
     g_score={spot:float("inf")  for row in grid for spot in row}  #insted Loop
     g_score[start]=0
     f_score={spot:float("inf") for row in grid for spot in row} 
     f_score[start]=h(start.get_pos(),end.get_pos())
     
     while not open_set.empty():
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
          current=open_set.get()[2]                                        #remove and return from PQ  the node       
          open_set_hash.remove(current)                                    #remove from list
         
          if current==end:
              path(came_from,current,end,draw,g_score[end])  
              
              return True 

          for nbor in current.nbors:
               temp_g_score = g_score[current]+1
               temp_f_score=temp_g_score + h(nbor.get_pos(),end.get_pos())

               if temp_f_score < f_score[nbor]:       #the sopt take new small value then update the oldest one
                  #update
                  came_from[nbor]=current
                  g_score[nbor]=temp_g_score
                  f_score[nbor]=temp_f_score
                  
                  if nbor not in open_set_hash:
                       count+=1
                       open_set.put((f_score[nbor],count,nbor))
                       open_set_hash.add(nbor)
                       if not nbor.is_end():
                         nbor.make_open()
               if current != start:
                  current.make_close()
               draw()

          for n in open_set_hash:
           n.writex(str(f_score[n]))
           pygame.display.update()
           pygame.time.delay(500)
                         
     return False


def main(win,width):
    ROWS=20

    start=None
    end=None
    
    grid=make_grid(ROWS,width)
    run=True

    while run:
         draw(win,grid,ROWS,width)
         for event in pygame.event.get():
              if event.type==pygame.QUIT:                 #cancel the Game
                   run=False

              if pygame.mouse.get_pressed()[0]:          #press in LEFT mouse Butt
                   pos=pygame.mouse.get_pos()
                   row,col=get_clicked_pos(pos,ROWS,width)
                   spot=grid[row][col]

                   if not start and spot!=end:
                        start=spot
                        start.make_start()

                   elif not end and spot!=start:
                        end=spot
                        end.make_end()

                   elif spot!=start and spot!=end:
                        spot.make_barrier()

              elif pygame.mouse.get_pressed()[2]:              #press RIGHT mouse Butt
                   pos=pygame.mouse.get_pos()
                   row,col=get_clicked_pos(pos,ROWS,width)
                   spot=grid[row][col]
                   spot.reset()
                   if spot==start:
                        start=None
                   elif spot==end:     
                        end=None     
              if event.type==pygame.KEYDOWN:
                   if event.key==pygame.K_a and start and end:
                        for row in grid:
                             for spot in row:
                                  spot.update_neighbors(grid)

                        if algorithmA_Star(lambda:draw(win,grid,ROWS,width),grid,start,end)==False:
                            label = font2.render('NO PATH From Start to End', 1, NOPATH)
                            WIN.blit(label,(40,40)) 
                            pygame.display.update()
                            pygame.time.delay(10000)

                   elif event.key==pygame.K_b and start and end:
                        for row in grid:
                             for spot in row:
                                  spot.update_neighbors(grid)

                        if algorithmBFS(lambda:draw(win,grid,ROWS,width),grid,start,end)==False:
                             label = font2.render('NO PATH From Start to End', 1, NOPATH)
                             WIN.blit(label,(40,40)) 
                             pygame.display.update()
                             pygame.time.delay(10000)
                             

                   if event.key==pygame.K_c:
                        start=None
                        end=None
                        grid=make_grid(ROWS,width)
                        

    pygame.quit()



main(WIN,WIDTH)





