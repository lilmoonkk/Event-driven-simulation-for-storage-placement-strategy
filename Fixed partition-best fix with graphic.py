# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pygame

#setting up animation
pygame.init()

red=(255,0,0)
blue=(0,0,255)
white=(255,255,255)
black=(0,0,0)
purple=(197, 203, 235)
pink=(222, 69, 196)

def pressspacetocontinue():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                return
            
def displayalljobblock(blocklist, screen):
    pygame.draw.rect(win,purple,(20,550,650,100))
    pos_x=20
    pos_y=550
    for x in range(len(blocklist)):
        if x==8:
            pos_x=20
            pos_y=600
        screen.blit(blocklist[x].block,(pos_x,pos_y))
        pos_x+=80
    pygame.display.update()
    
class job:
    def __init__(self,jobno,arrivalt,processingt,jobsize):
        self.jobno=jobno
        self.arrivalt=arrivalt
        self.processingt=processingt
        self.jobsize=jobsize

class event:
    def __init__(self,time,jobno,memoryno,eventtype):
        self.time=time
        self.jobno=jobno
        self.memoryno=memoryno
        self.eventtype=eventtype #Arrive or Leave

class memory:
    def __init__(self,memoryno,size):
        self.memoryno=memoryno;
        self.size=size
        self.jobno=None
        self.status='Free' #Free or Busy
        self.position_x=None
        self.position_y=None
        
class waitingjob:
    def _init_(self,jobno, arrivalt, processingt,jobsize):
        self.jobno=jobno
        self.arrivalt=arrivalt
        self.processingt=processingt
        self.jobsize=jobsize
        
class jobblock:
    def __init__(self, jobno, jobsize, color):
        self.jobno=jobno
        self.block = pygame.Surface((50, 30))
        self.block.fill(color)
        self.position=self.block.get_rect().move(150, 50)
        self.font = pygame.font.SysFont(None,20)
        self.jobnotext= self.font.render("J"+str(jobno),True, white)
        self.block.blit(self.jobnotext, (25,17))
        self.text = self.font.render(jobsize, True, black)
        self.block.blit(self.text, (5,5))
    
    def move(self,pos_x,pos_y,screen):
        pygame.time.delay(500)
        keepmoving=True
        pygame.draw.rect(screen, purple, (150,50,50,30))
        while keepmoving:
            #pygame.draw.rect(screen, purple, (self.position,50,30)) 
            #pygame.display.update()
            self.position=self.position.move(0,5)
            if self.position.bottom>pos_y:
                keepmoving=False
        if self.position.right<pos_x:
                keepmoving=True
        while keepmoving:
            #pygame.draw.rect(screen, purple, (self.position,50,30)) 
            #pygame.display.update()
            self.position=self.position.move(5,0)
            if self.position.right>pos_x:
                keepmoving=False
      
#read joblist textfile and store data
infile=open('Joblist.txt','r')
joblisttxt=infile.readlines()
totaljobno=int(joblisttxt[0])
joblist=[]
eventlist=[]
jobblocklist=[]
for i in range(1,totaljobno+1):
    jobdata=joblisttxt[i].split()
    joblist.append(job(int(jobdata[0]),int(jobdata[1]),int(jobdata[2]),int(jobdata[3])))
    eventlist.append(event(int(jobdata[1]),int(jobdata[0]),None,'Arrive'))
    jobblocklist.append(jobblock(int(jobdata[0]),jobdata[3],red))

#read memorylist textfile and store data
infile=open('MemoryList.txt','r')

memorylisttxt=infile.readlines()
memoryno=int(input("Please enter total number of memory blocks(3/5/7/10):"))
memorysizelist=[]
memorylist=[]

for i in range(1,memoryno+1):
    memorylist.append(memory(i,int(memorylisttxt[i])))
    memorysizelist.append(int(memorylisttxt[i]))
maxmemory=max(memorysizelist)

# create the window to display the allocation  
win = pygame.display.set_mode((800, 650))
pygame.display.set_caption("Fixed partition-best fit") 
win.fill(purple)

#position of memory block
memory_x = 500
memory_y = 50
#size of memory block
memory_w = 150
memory_h = 40

#before sorting
#draw the memory block on the screen
for i in range(0,memoryno):
    pygame.draw.rect(win,white,(memory_x,memory_y,memory_w,memory_h))
    pygame.draw.line(win,blue,(memory_x,memory_y),(650, memory_y),1)
    font = pygame.font.SysFont(None,30)
    text = font.render(str(memorylist[i].size), True, blue)
    win.blit(text, (590,memory_y))
    memorylist[i].position_x=memory_x+75
    memorylist[i].position_y=memory_y+memory_h-8
    memory_y += 40

#draw waiting queue
pygame.draw.line(win,blue,(0,500),(650, 500),1)
font = pygame.font.SysFont(None,30)
text = font.render("Waiting Queue", True, blue)
win.blit(text, (5,505))

font = pygame.font.SysFont(None,40)
text = font.render("Press SPACE to continue", True, black)
win.blit(text, (5,5))
pygame.display.flip()
pressspacetocontinue()
#after sorting
memorylist.clear()
memorysizelist.sort()
for i in range(0,memoryno):
    memorylist.append(memory(i+1,int(memorysizelist[i])))
    
memory_y = 50
pygame.draw.rect(win,purple,(memory_x,memory_y,memory_w,450))
#draw the memory block on the screen
for i in range(0,memoryno):
    pygame.draw.rect(win,white,(memory_x,memory_y,memory_w,memory_h))
    pygame.draw.line(win,blue,(memory_x,memory_y),(650, memory_y),1)
    font = pygame.font.SysFont(None,30)
    text = font.render(str(memorylist[i].size), True, blue)
    win.blit(text, (590,memory_y))
    memorylist[i].position_x=memory_x+75
    memorylist[i].position_y=memory_y+memory_h-8
    memory_y += 40
    
pygame.draw.rect(win,purple,(5,5,450,40))
font = pygame.font.SysFont(None,40)
text = font.render("Press SPACE to continue", True, black)
win.blit(text, (5,5))
pygame.display.update()
pressspacetocontinue()

outfile=open('Fixed partition-best fit.txt','w')
totaljobdone=0
totalprocessingtimeofjob=0
totalsimulationtime=0
total_int_frag=0
waitingtime=[]
queuelength={}
waitingqueue=[]
waitingjobblocklist=[]

#fixed-partition first fix
while eventlist or joblist or waitingqueue:
    
    if eventlist:
        if not eventlist[0].time==0:
            if not ((eventlist[0].time-time)==0) or not ((eventlist[0].time-time)==1):
                round=eventlist[0].time-time
                for r in range(1,round):
                    temptime=time+r
                    queuelength[temptime]=len(waitingqueue)
        
        time=eventlist[0].time
        #display time
        pygame.draw.rect(win,purple,(5,5,450,40))
        font = pygame.font.SysFont(None,40)
        text = font.render(str(time)+"    Press SPACE to continue", True, black)
        win.blit(text, (5,5))
        
                    
        #if the event is 'Arrive'
        if eventlist[0].eventtype=='Arrive':
            # drawing a job block on screen when job arrived 
            #position of job block
            win.blit(jobblocklist[0].block,jobblocklist[0].position)
            pygame.display.update()
            pygame.time.delay(100)
            
            #if the jobsize exceeds the largest limit of memory block size, skip the job
            if joblist[0].jobsize>maxmemory:
                outfile.write("J"+str(joblist[0].jobno)+
                              ": There is no suitable memory block for this job at all"+"\n")
                pygame.draw.rect(win, purple, (150, 50,50,30)) 
                pygame.display.update()
                pygame.time.delay(100)
            else:
                found=False
                for k in range(0,memoryno):
                    if memorylist[k].size>=joblist[0].jobsize and memorylist[k].status=='Free':
                        memorylist[k].jobno=joblist[0].jobno
                        memorylist[k].status='Busy'
                        found=True
                        totaljobdone+=1
                        totalprocessingtimeofjob+=joblist[0].processingt
                        int_frag=memorylist[k].size-joblist[0].jobsize
                        total_int_frag+=int_frag
                        waitingtime.append(time-joblist[0].arrivalt)
                        leavingt=joblist[0].arrivalt+joblist[0].processingt
                        for j in range(1,len(eventlist)):
                            if leavingt>eventlist[j-1].time and leavingt<=eventlist[j].time:
                                eventlist.insert(j, event(leavingt, joblist[0].jobno, memorylist[k].memoryno,'Leave'))
                                break
                        if leavingt>eventlist[-1].time:
                            eventlist.append(event(leavingt, joblist[0].jobno, memorylist[k].memoryno,'Leave'))
                        jobblocklist[0].move(memorylist[k].position_x,memorylist[k].position_y,win)
                        win.blit(jobblocklist[0].block,jobblocklist[0].position)
                        pygame.display.update()
                        pygame.time.delay(100)
                        break
                #if the job cannot find a suitable memory block this round,
                #it will queue again
                if found==False:
                    waitingqueue.append(joblist[0])
                    pygame.time.delay(500)
                    pygame.draw.rect(win, purple, (150, 50,50,30)) 
                    pygame.display.update()
                    pygame.time.delay(500)
                    waitingjobblocklist.append(jobblock(joblist[0].jobno,str(joblist[0].jobsize),pink))
                    displayalljobblock(waitingjobblocklist, win)
                    pygame.time.delay(500)
            jobblocklist.remove(jobblocklist[0])
            joblist.remove(joblist[0])
            
        #if the event is 'Leave'
        elif eventlist[0].eventtype=='Leave':
            for k in range(0,memoryno):
                if memorylist[k].memoryno==eventlist[0].memoryno:
                    pygame.draw.rect(win,white,( memorylist[k].position_x-50,
                                                memorylist[k].position_y-30,memory_w-90,memory_h-5))
                    pygame.display.update()
                    pygame.time.delay(500)
                    memorylist[k].jobno=None
                    memorylist[k].status='Free'
                    break
        
        if waitingqueue:
            if not len(eventlist)==1:
                if eventlist[0].eventtype == 'Leave' and (not(eventlist[0].time==eventlist[1].time) or 
                                                          ((eventlist[0].time==eventlist[1].time)and 
                                                           eventlist[1].eventtype == 'Arrive')
                                                          ):
                    index=0
                    while index<len(waitingqueue):
                        found=False
                        win.blit(waitingjobblocklist[index].block,waitingjobblocklist[index].position)
                        pygame.display.update()
                        pygame.time.delay(500)
                        for b in range(0, memoryno):
                            if memorylist[b].size>=waitingqueue[index].jobsize and memorylist[b].status=='Free':
                                memorylist[b].jobno=waitingqueue[index].jobno
                                memorylist[b].status='Busy'
                                found=True
                                totaljobdone+=1
                                totalprocessingtimeofjob+=waitingqueue[index].processingt
                                int_frag=memorylist[b].size-waitingqueue[index].jobsize
                                total_int_frag+=int_frag
                                waitingtime.append(time-waitingqueue[index].arrivalt)
                                leavingt=time+waitingqueue[index].processingt
                                for j in range(1,len(eventlist)):
                                    if leavingt>eventlist[j-1].time and leavingt<=eventlist[j].time:
                                        eventlist.insert(j, event(leavingt, waitingqueue[index].jobno, memorylist[b].memoryno,'Leave'))
                                        break
                                if leavingt>eventlist[-1].time:
                                    eventlist.append(event(leavingt, waitingqueue[index].jobno, memorylist[b].memoryno,'Leave'))
                                waitingjobblocklist[index].move(memorylist[b].position_x,memorylist[b].position_y,win)
                                win.blit(waitingjobblocklist[index].block,waitingjobblocklist[index].position)
                                pygame.display.update()
                                pygame.time.delay(500)
                                waitingqueue.remove(waitingqueue[index])
                                waitingjobblocklist.remove(waitingjobblocklist[index])
                                displayalljobblock(waitingjobblocklist, win)
                                break
                        if found==True:
                            continue
                        pygame.draw.rect(win, purple, (150, 50,50,30)) 
                        pygame.display.update()
                        pygame.time.delay(200)
                        #if a job is removed, the index will remain
                        #Otherwise, it will increment 1
                        index=index+1
                    
        #Remove this event because it is sone processing
        eventlist.remove(eventlist[0])
                
    if not eventlist and waitingqueue:
        index=0
        while index<len(waitingqueue):
            found=False
            win.blit(waitingjobblocklist[index].block,waitingjobblocklist[index].position)
            pygame.display.update()
            pygame.time.delay(500)
            for b in range(0, memoryno):
                if memorylist[b].size>=waitingqueue[index].jobsize and memorylist[b].status=='Free':
                    memorylist[b].jobno=waitingqueue[index].jobno
                    memorylist[b].status='Busy'
                    found=True
                    totaljobdone+=1
                    totalprocessingtimeofjob+=waitingqueue[index].processingt
                    int_frag=memorylist[b].size-waitingqueue[index].jobsize
                    total_int_frag+=int_frag
                    waitingtime.append(time-waitingqueue[index].arrivalt)
                    leavingt=time+waitingqueue[index].processingt
                    if not eventlist:
                        eventlist.append(event(leavingt, waitingqueue[index].jobno, memorylist[b].memoryno,'Leave'))
                    else:
                        for j in range(1,len(eventlist)):
                            if leavingt>eventlist[j-1].time and leavingt<=eventlist[j].time:
                                eventlist.insert(j, event(leavingt, waitingqueue[index].jobno, memorylist[b].memoryno,'Leave'))
                                break
                        if leavingt>eventlist[-1].time:
                            eventlist.append(event(leavingt, waitingqueue[index].jobno, memorylist[b].memoryno,'Leave'))
                    waitingjobblocklist[index].move(memorylist[b].position_x,memorylist[b].position_y,win)
                    win.blit(waitingjobblocklist[index].block,waitingjobblocklist[index].position)
                    pygame.display.update()
                    pygame.time.delay(500)
                    waitingqueue.remove(waitingqueue[index])
                    waitingjobblocklist.remove(waitingjobblocklist[index])
                    displayalljobblock(waitingjobblocklist, win)
                    break
            if found==True:
                continue
            pygame.draw.rect(win, purple, (150, 50,50,30)) 
            pygame.display.update()
            pygame.time.delay(200)
            #if a job is removed, the index will remain
            #Otherwise, it will increment 1
            index=index+1
            
    queuelength[time]=len(waitingqueue)
    totalsimulationtime=time+1 
        
    pressspacetocontinue()
    

outfile.write("total processing time of job: "+str(totalprocessingtimeofjob)+"\n")
outfile.write("total simulation time: "+str(totalsimulationtime)+"\n")
throughput=totalprocessingtimeofjob/totalsimulationtime
queuelencat={}
for r in range(len(queuelength)):
    if queuelength[r] in queuelencat.keys():
        temp=queuelencat[queuelength[r]]
        queuelencat[queuelength[r]]=temp+1
    else:
        queuelencat[queuelength[r]]=1
queuelengthvar=list(queuelencat.keys())
averageql=0
for r in range(len(queuelencat)):
    averageql+=(queuelengthvar[r]*queuelencat[queuelengthvar[r]]/totalsimulationtime)
outfile.write("total job done: "+str(totaljobdone)+"\n")
outfile.write("throughput: "+ str(throughput)+"\n")
outfile.write("average internal fragmentation: "+str(total_int_frag/totaljobdone)+"\n")
outfile.write("maximum waiting time: "+ str(max(waitingtime))+"\n")
outfile.write("minimum waiting time: "+ str(min(waitingtime))+"\n")
outfile.write("average waiting time: "+ str(sum(waitingtime)/len(waitingtime))+"\n")
outfile.write("maximum queue length: "+ str(max(queuelengthvar))+"\n")
outfile.write("minimum queue length: "+ str(min(queuelengthvar))+"\n")
outfile.write("average queue length: "+str(averageql)+"\n")
outfile.close()
pygame.quit()