# -*- coding: utf-8 -*-
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
    #print(len(blocklist))
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
    def __init__(self,time,jobno,start,end,eventtype):
        self.time=time
        self.jobno=jobno
        self.start=start
        self.end=end
        self.eventtype=eventtype #Arrive or Leave

class memory:
    def __init__(self,start,end,size,status,position_y):
        self.start=start
        self.end=end
        self.size=size
        self.jobno=None
        self.status=status #Free or Busy
        self.position_y=position_y
        
class jobblock:
    def __init__(self, jobno, jobsize, color):
        self.jobno=jobno
        self.jobsize=jobsize
        self.block = pygame.Surface((50, 30))
        self.block.fill(color)
        self.position=self.block.get_rect().move(150, 50)
        #self.rect = self.block.get_rect()
        self.font = pygame.font.SysFont(None,20)
        self.jobnotext= self.font.render("J"+str(jobno),True, white)
        self.block.blit(self.jobnotext, (25,17))
        self.text = self.font.render(jobsize, True, black)
        self.block.blit(self.text, (5,5))
    
    def move(self,pos_y,jobsize,screen,color):
        pygame.time.delay(500)
        pygame.draw.rect(screen, purple, (150,50,50,30))
        pygame.draw.rect(screen, color, (500,pos_y,150,(jobsize/maxmemory)*400),1 )
        self.text = self.font.render("J"+str(self.jobno), True, black)
        screen.blit(self.text, (550,pos_y))
        pygame.display.update()
        pygame.time.delay(500)
        
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
    jobblocklist.append(jobblock(int(jobdata[0]),jobdata[3],red))
    eventlist.append(event(int(jobdata[1]),int(jobdata[0]),None,None,'Arrive'))

#initiate memory
memorylist=[]
maxmemory=int(input("Please enter memory size(20000/30000/40000/50000):"))
memorylist.append(memory(0,maxmemory,maxmemory,'Free',50))

# create the window to display the allocation  
win = pygame.display.set_mode((800, 650))
pygame.display.set_caption("Dynamic partition-first fit") 
win.fill(purple)
pygame.draw.rect(win,white,(500,50,150,400))
font = pygame.font.SysFont(None,30)
text = font.render(str(maxmemory), True, blue)
win.blit(text, (550,460))
#draw waiting queue
pygame.draw.line(win,blue,(0,500),(650, 500),1)
font = pygame.font.SysFont(None,30)
text = font.render("Waiting Queue", True, blue)
win.blit(text, (5,505))

pygame.display.flip()


outfile=open('Dynamic partition-first fit.txt','w')
totaljobdone=0
totalprocessingtimeofjob=0
totalsimulationtime=0
total_ext_frag=0
waitingtime=[]
queuelength={}
#initiate waiting queue
waitingqueue=[]
waitingjobblocklist=[]

#dynamic partition-best fix
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
        pygame.draw.rect(win,purple,(5,5,450,50))
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
            if joblist[0].jobsize>maxmemory:
                outfile.write("J"+str(joblist[0].jobno)+": There is no suitable memory blaock for this job at all\n")
                pygame.draw.rect(win, purple, (150, 50,50,30)) 
                pygame.display.update()
                pygame.time.delay(100)
            else:
                
                #initiate found to false
                found=False
                #Gather free memory space together
                #into one temporary memory list
                temporary=[]
                for i in range(0,len(memorylist)):
                    if memorylist[i].status=='Free':
                        temporary.append(memorylist[i])
                
                #matching jobsize with temporary's
                for j in range(0, len(temporary)):
                    if joblist[0].jobsize<=temporary[j].size:
                        index=memorylist.index(temporary[j])
                        #Calculation
                        totaljobdone+=1
                        totalprocessingtimeofjob+=joblist[0].processingt
                        waitingtime.append(time-joblist[0].arrivalt)
                        leavingt=joblist[0].arrivalt+joblist[0].processingt
                        if joblist[0].jobsize==temporary[j].size:
                            memorylist[index].status='Busy'
                            memorylist[index].jobno=joblist[0].jobno
                            memorylist[index].position_y=50+((memorylist[index].start/maxmemory)*400)
                            for j in range(1,len(eventlist)):
                                if leavingt>eventlist[j-1].time and leavingt<=eventlist[j].time:
                                    eventlist.insert(j, event(leavingt, joblist[0].jobno, memorylist[index].start, memorylist[index].end,'Leave'))
                                    break
                            if leavingt>eventlist[-1].time:
                                eventlist.append(event(leavingt, joblist[0].jobno, memorylist[index].start, memorylist[index].end,'Leave'))
                            
                        elif joblist[0].jobsize<temporary[j].size:
                            newend=memorylist[index].start+joblist[0].jobsize
                            newsize=memorylist[index].end-newend
                            memorylist.insert(index,memory(memorylist[index].start,
                                                           newend,joblist[0].jobsize,'Busy', 50+
                                                           ((memorylist[index].start/maxmemory)*400)))
                            memorylist[index+1].start,memorylist[index+1].size=newend,newsize
                            memorylist[index+1].position_y=50+((newend/maxmemory)*400)
                            memorylist[index].jobno=joblist[0].jobno
                            for j in range(1,len(eventlist)):
                                if leavingt>eventlist[j-1].time and leavingt<=eventlist[j].time:
                                    eventlist.insert(j, event(leavingt, joblist[0].jobno, memorylist[index].start, newend,'Leave'))
                                    break
                            if leavingt>eventlist[-1].time:
                                eventlist.append(event(leavingt, joblist[0].jobno, memorylist[index].start, newend,'Leave'))    
                        found=True
                        jobblocklist[0].move(memorylist[index].position_y,joblist[0].jobsize,win, red)
                        break
                if found==False:
                    waitingqueue.append(joblist[0])
                    pygame.time.delay(500)
                    pygame.draw.rect(win, purple, (150, 50,50,30)) 
                    pygame.display.update()
                    pygame.time.delay(500)
                    waitingjobblocklist.append(jobblock(joblist[0].jobno,str(joblist[0].jobsize),pink))
                    displayalljobblock(waitingjobblocklist, win)
                    pygame.time.delay(500)
                    freememory=0
                    for i in range(0,len(memorylist)):
                        if memorylist[i].status=='Free':
                            freememory+=memorylist[i].size
                    if freememory>=joblist[0].jobsize:
                        total_ext_frag+=freememory
            jobblocklist.remove(jobblocklist[0]) 
            joblist.remove(joblist[0])
            
        #if the event is 'Leave'
        elif eventlist[0].eventtype=='Leave':
            for i in range(0,len(memorylist)):
                if eventlist[0].start==memorylist[i].start and eventlist[0].end==memorylist[i].end:
                    memorylist[i].status='Free'
                    memorylist[i].jobno=None
                    pygame.draw.rect(win, white, (500,memorylist[i].position_y,
                                                     150,(memorylist[i].size/maxmemory)*400))
                    pygame.display.update()
                    #combine with the upper free memory space
                    if not i==0:
                        while memorylist[i-1].status=='Free':
                            memorylist[i].position_y=None
                            memorylist[i].start=memorylist[i-1].start
                            memorylist[i].size=memorylist[i].end-memorylist[i].start
                            memorylist.remove(memorylist[i-1])
                            i=i-1
                            if i==0:
                                break
                            
                    #combine with the lower free memory space
                    if not i==(len(memorylist)-1):
                        while memorylist[i+1].status=='Free':
                            memorylist[i+1].position_y=None
                            memorylist[i].end=memorylist[i+1].end
                            memorylist[i].size=memorylist[i].end-memorylist[i].start
                            memorylist.remove(memorylist[i+1])
                            if i==(len(memorylist)-1):
                                break
                            
                    break
        
        #check if there is job in waiting queue
        #Priority is given to waiting job
        if waitingqueue:
            if not len(eventlist)==1:
                if eventlist[0].eventtype == 'Leave' and (not(eventlist[0].time==eventlist[1].time) or 
                                                              ((eventlist[0].time==eventlist[1].time)and 
                                                               eventlist[1].eventtype == 'Arrive')
                                                              ):
                    indexwq=0
                    
                    while indexwq<len(waitingqueue):
                        #Gather free memory space together
                        #into one temporary memory list and sort
                        temporary=[]
                        for i in range(0,len(memorylist)):
                            if memorylist[i].status=='Free':
                                temporary.append(memorylist[i])
                        
                        found=False
                        win.blit(waitingjobblocklist[indexwq].block,waitingjobblocklist[indexwq].position)
                        pygame.display.update()
                        pygame.time.delay(500)
                        for b in range(0, len(temporary)):
                            if waitingqueue[indexwq].jobsize<=temporary[b].size:
                                index=memorylist.index(temporary[b])
                                #Calculation
                                totaljobdone+=1
                                totalprocessingtimeofjob+=waitingqueue[indexwq].processingt
                                waitingtime.append(time-waitingqueue[indexwq].arrivalt)
                                leavingt=time+waitingqueue[indexwq].processingt
                                found=True
                                if waitingqueue[indexwq].jobsize==temporary[b].size:
                                    memorylist[index].status='Busy'
                                    memorylist[index].jobno=waitingqueue[indexwq].jobno
                                    memorylist[index].position_y=50+((memorylist[index].start/maxmemory)*400)
                                    for j in range(1,len(eventlist)):
                                        if leavingt>eventlist[j-1].time and leavingt<=eventlist[j].time:
                                            eventlist.insert(j, event(leavingt,waitingqueue[indexwq].jobno, memorylist[index].start, memorylist[index].end,'Leave'))
                                            break
                                    if leavingt>eventlist[-1].time:
                                        eventlist.append(event(leavingt, waitingqueue[indexwq].jobno, memorylist[index].start, memorylist[index].end,'Leave'))
                                        
                                elif waitingqueue[indexwq].jobsize<temporary[b].size:
                                    newend=memorylist[index].start+waitingqueue[indexwq].jobsize
                                    newsize=memorylist[index].end-newend
                                    memorylist.insert(index,memory(memorylist[index].start,newend,
                                                                   waitingqueue[indexwq].jobsize,'Busy',50+
                                                                   ((memorylist[index].start/maxmemory)*400)))
                                    memorylist[index+1].start,memorylist[index+1].size=newend,newsize
                                    memorylist[index+1].position_y=50+((newend/maxmemory)*400)
                                    memorylist[index].jobno=waitingqueue[indexwq].jobno
                                    for j in range(1,len(eventlist)):
                                        if leavingt>eventlist[j-1].time and leavingt<=eventlist[j].time:
                                            eventlist.insert(j, event(leavingt, waitingqueue[indexwq].jobno, memorylist[index].start, newend,'Leave'))
                                            break
                                    if leavingt>eventlist[-1].time:
                                        eventlist.append(event(leavingt, waitingqueue[indexwq].jobno, memorylist[index].start, newend,'Leave'))
                                        
                                waitingjobblocklist[indexwq].move(memorylist[index].position_y,waitingqueue[indexwq].jobsize,win, pink)
                                
                                pygame.display.update()
                                pygame.time.delay(500)
                                waitingqueue.remove(waitingqueue[indexwq])
                                waitingjobblocklist.remove(waitingjobblocklist[indexwq])
                                displayalljobblock(waitingjobblocklist, win)
                                
                                break
                        if found==True:
                            continue
                        pygame.draw.rect(win, purple, (150, 50,50,30)) 
                        pygame.display.update()
                        pygame.time.delay(200)
                        #if a job is removed, the index will remain the same
                        #Otherwise, it will increment 1
                        indexwq=indexwq+1
        #Remove this event because it is done processing                    
        eventlist.remove(eventlist[0])
                        
    if not eventlist and waitingqueue:
        
        indexwq=0
        
        while indexwq<len(waitingqueue):
            #Gather free memory space together
            #into one temporary memory list and sort
            temporary=[]
            for i in range(0,len(memorylist)):
                if memorylist[i].status=='Free':
                    temporary.append(memorylist[i])
            
            found=False
            win.blit(waitingjobblocklist[indexwq].block,waitingjobblocklist[indexwq].position)
            pygame.display.update()
            pygame.time.delay(500)
            for b in range(0, len(temporary)):
                if waitingqueue[indexwq].jobsize<=temporary[b].size:
                    index=memorylist.index(temporary[b])
                    #Calculation
                    totaljobdone+=1
                    totalprocessingtimeofjob+=waitingqueue[indexwq].processingt
                    waitingtime.append(time-waitingqueue[indexwq].arrivalt)
                    leavingt=time+waitingqueue[indexwq].processingt
                    found=True
                    if waitingqueue[indexwq].jobsize==temporary[b].size:
                        memorylist[index].status='Busy'
                        memorylist[index].jobno=waitingqueue[indexwq].jobno
                        memorylist[index].position_y=50+((memorylist[index].start/maxmemory)*400)
                        if not eventlist:
                            eventlist.append(event(leavingt, waitingqueue[indexwq].jobno, memorylist[index].start, memorylist[index].end,'Leave'))
                        else:
                            for j in range(1,len(eventlist)):
                                if leavingt>eventlist[j-1].time and leavingt<=eventlist[j].time:
                                    eventlist.insert(j, event(leavingt,waitingqueue[indexwq].jobno, memorylist[index].start, memorylist[index].end,'Leave'))
                                    break
                            if leavingt>eventlist[-1].time:
                                eventlist.append(event(leavingt, waitingqueue[indexwq].jobno, memorylist[index].start, memorylist[index].end,'Leave'))
                            
                    elif waitingqueue[indexwq].jobsize<temporary[b].size:
                        newend=memorylist[index].start+waitingqueue[indexwq].jobsize
                        newsize=memorylist[index].end-newend
                        memorylist.insert(index,memory(memorylist[index].start,newend,
                                                       waitingqueue[indexwq].jobsize,'Busy',50+
                                                       ((memorylist[index].start/maxmemory)*400)))
                        memorylist[index+1].start,memorylist[index+1].size=newend,newsize
                        memorylist[index+1].position_y=50+((newend/maxmemory)*400)
                        memorylist[index].jobno=waitingqueue[indexwq].jobno
                        if not eventlist:
                            eventlist.append(event(leavingt, waitingqueue[indexwq].jobno, memorylist[index].start, newend,'Leave'))
                        else:
                            for j in range(1,len(eventlist)):
                                if leavingt>eventlist[j-1].time and leavingt<=eventlist[j].time:
                                    eventlist.insert(j, event(leavingt, waitingqueue[indexwq].jobno, memorylist[index].start, newend,'Leave'))
                                    break
                            if leavingt>eventlist[-1].time:
                                eventlist.append(event(leavingt, waitingqueue[indexwq].jobno, memorylist[index].start, newend,'Leave'))
                    waitingjobblocklist[indexwq].move(memorylist[index].position_y,waitingqueue[indexwq].jobsize,win, pink)
                    
                    pygame.display.update()
                    pygame.time.delay(500)
                    waitingqueue.remove(waitingqueue[indexwq])
                    waitingjobblocklist.remove(waitingjobblocklist[indexwq])
                    displayalljobblock(waitingjobblocklist, win)
                    break
            if found==True:
                continue
            pygame.draw.rect(win, purple, (150, 50,50,30)) 
            pygame.display.update()
            pygame.time.delay(200)
            #if a job is removed, the index will remain the same
            #Otherwise, it will increment 1
            indexwq=indexwq+1
            
    queuelength[time]=len(waitingqueue)
    totalsimulationtime=time+1
    pressspacetocontinue()
                        
pygame.quit()
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
outfile.write("throughput: "+str(throughput)+"\n")
outfile.write("average external fragmentation: "+str(total_ext_frag/totaljobdone)+"\n")
outfile.write("maximum waiting time: "+str( max(waitingtime))+"\n")
outfile.write("minimum waiting time: "+str( min(waitingtime))+"\n")
outfile.write("average waiting time: "+str(sum(waitingtime)/len(waitingtime))+"\n")
outfile.write("maximum queue length: "+str(max(queuelengthvar))+"\n")
outfile.write("minimum queue length: "+str(min(queuelengthvar))+"\n")
outfile.write("average queue length: "+str( averageql)+"\n")
outfile.close()