#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 21:39
# @Author  : falingling
# @File    : skeleton_nomination1.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/13 14:23
# @Author  : falingling
# @File    : skeloton_nomination.py

#read skeleton column from files
from pylab import *
from numpy import *
import os
import os.path
import numpy as np
import random
from keras.utils import np_utils
def getdata1(path, timesteps):
#read trainlist.txt,test.txt,get the data
#get the 40 frames,calculate the number between <100,100-200,200-300
 traindir = path
 maxframe=1
 frame11=0
 frame12=0
 frame23=0
 f=open(traindir,"r")
 x_train_torso=[]
 x_train_lhand=[]
 x_train_rhand=[]
 x_train_lleg=[]
 x_train_rleg=[]
 y_train=[]
 y_tag=[]
 tree=[0,19,1,2,1,7,8,9,10,23,22,23,10,9,8,7,3,4,5,6,21,20,21,6,5,4,3,0,15,16,17,18,17,16,15,11,12,13,14,13,12,11,0]
 tree_torso=[0,19,1,2,1,19,0]
 tree_lhand=[7,8,9,10,23,22,23,10,9,8,7]
 tree_rhand=[3,4,5,6,21,20,21,6,5,4,3]
 tree_lleg=[15,16,17,18,17,16,15]
 tree_rleg=[11,12,13,14,13,12,11]
 for i in range(60):
    y_tag.extend([0])
 n=0
#read all the train files
 lines=f.readlines()
 joint3=[]
 for i in range(144):
    joint3.extend([-1])
 for line1 in lines:
   #print "process : ",n
   #print "maxframe: ", maxframe   
   line1=line1.strip('\n')
   train=line1.split("\t")
  # print train
  #read tag
   #print train[0]
   #print train[1]
   tag1=int(train[1])
#   y_tag.extend([tag1-1])
  #print tag1
   tag=[]
   for i in range(60):
      tag.extend([0])
   tag[tag1-1]=1
  # print tag
  #print len(tag)
 #  y_train.append(tag)
 # print y_train
  #break
  #for filename in filenames :
       #if filename.endswith('.txt'):
        #  print "parent is :"+ parent
         # print "filename is:" + filename
          #print "the full name of the file is:" + os.path.join(parent,filename) #Ê³öþ·¾¶ÐϢ
        #  thefile=os.path.join(parent,filename)


  # read y-train

   file_object = open(train[0])

              #for line in file_object.readlines():
              #  print line
                #print file_object.read(4)
   line=file_object.readline()
              #all the frames skeleton
   body_torso = []
   body_lhand = []
   body_rhand = []
   body_lleg = []
   body_rleg = []
   body_mirror =[]
   done=0
   #p1=1
   while line:
           # print line
            #read the number of frames
            
            framecount=line
           # print "framecount:", framecount
            #if timesteps >framecount,add with value -1
            #framecount=timesteps
            for i in range(int(framecount)):
               line = file_object.readline()
              # p1+=1
               #read the number of body
              # print i
              # print line
              # print p1
               if(line==''):
                   done=1
               if(done):
                  framecount=i
                 # print "new framecount",framecount
                  break
               while(int(line) == 0):
                 line = file_object.readline()
                 if(line==''):
                     done=1
                     break
               
               if(done):
                  framecount=i
                #  print "new framecount",framecount
                  break 
               # p1+=1
               bodycount=int(line)
               #print "the process frame:",i
               #print "bodycount:" ,bodycount
               #process the body
               joint_torso=[]
               joint_lhand=[]
               joint_rhand=[]
               joint_lleg=[]
               joint_rleg=[]
               
               joint_mirror=[]
               for m in range(bodycount):
                #skip the information
                #if bodycount < 2,add with value 0
                 line = file_object.readline()
            #     print line
                #rad skeleton
                 line = file_object.readline()
                # p1+=2
             #    print line
                 jointcount=int(line)
                 #basejoint
                 baseskeleton = file_object.readline()
                 baseskeleton=baseskeleton.strip()
                 basejoint1=baseskeleton.split()
                 basejoint=[]
                 basejoint.extend(map(eval, basejoint1[:3]))
                #24 skeleton
                 onejoints=[]
                 mirrorjoints=[]
                 for j in range(jointcount-1):
                     line = file_object.readline()
              #       print line
                     #split for 7
                      #read single person
                    # p1+=1
                     #joint2=[]
                     otherjoint1=line.split(" ")
                     otherjoint=[]
                     otherjoint_m=[]
                    #mirror joint
                    #batch for float *7
                     otherjoint.extend(map(eval,otherjoint1[:3]))
                     for m in range(3):
                         otherjoint[m]=otherjoint[m]-basejoint[m]
                     #mirror,x:-x
                     otherjoint_m.extend([-otherjoint[0]])
                     otherjoint_m.extend([otherjoint[1]])
                     otherjoint_m.extend([otherjoint[2]])
                     onejoints.append(otherjoint)
                    # mirrorjoints.append(otherjoint_m)
                 #skeleton sequence:2,21,3,4,3,9,10,11,12,25,24,25,12,11,10,9,5,6,7,8,23,22,23,8,7,6,5,2,17,18,19,20,19,18,17,13,14,15,16,15,14,13,2    
                 #skeleton sequance tag:0,19,1,2,1,7,8,9,10,23,22,23,10,9,8,7,3,4,5,6,21,20,21,6,5,4,3,0,15,16,17,18,17,16,15,11,12,13,14,13,12,11,0
                 for t in tree_torso:
                       joint_torso.extend(onejoints[t])
                 for t in tree_lhand:
                       joint_lhand.extend(onejoints[t])
                 for t in tree_rhand:
                       joint_rhand.extend(onejoints[t])
                 for t in tree_lleg:
                       joint_lleg.extend(onejoints[t])
                 for t in tree_rleg:
                       joint_rleg.extend(onejoints[t])
                      # joint_mirror.extend(mirrorjoints[tree[t]])
                # print len(joint)
                   #  joint.extend(map(eval,joint1[7:11]))
               #      print joint
                               #*25
                               #joint.append(joint2)
              # print len(joint)
                #add another body
                #*frame(timestep)
                 #if(m == 0):
               ''' if (bodycount == 1):
                   for i in range(129):
                     joint.extend([0])
               '''  
               ''' if(len(joint)!=350):
                   
                   print n
                   print "error:" ,train[0]
               '''       
               body_torso.append(joint_torso)
               body_lhand.append(joint_lhand)
               body_rhand.append(joint_rhand)
               body_lleg.append(joint_lleg)
               body_rleg.append(joint_rleg)
               
              # body_mirror.append(joint_mirror)
                #   print len(body[i])
                 #  print len(body)
                  # print body
               
                  #add value 175*0
                    
                        #line = file_object.readline()
            f1=int(framecount)
            f2=f1
            '''
            if (maxframe<f1):
                 maxframe=f1
            if(f1 < 100):
                 frame11+=1
            elif (f1 > 200):
                 frame23+=1
            else:
                 frame12+=1
            '''
            #test border
            if(timesteps>f2):            
               while(timesteps > f1):
                 f1+=1
                 body_torso.append(body_torso[-1])
                 body_lhand.append(body_lhand[-1])
                 body_rhand.append(body_rhand[-1])
                 body_lleg.append(body_lleg[-1])
                 body_rleg.append(body_rleg[-1])
                # body_mirror.append(body_mirror[-1])
               x_train_torso.append(body_torso)
               x_train_lhand.append(body_lhand)
               x_train_rhand.append(body_rhand)
               x_train_lleg.append(body_lleg)
               x_train_rleg.append(body_rleg)
              # x_train.append(body.mirror)
              # y_train.append(tag)
               y_train.append(tag)
              # y_tag.extend([tag1-1])
            #clip the video
            else:
                      step=f2/timesteps
              # print "frame:",f2,step:-3,3-6,6-:1,3,5
             #  for j in range(2):
                      body1_torso=[]
                      body1_lhand=[]
                      body1_rhand=[]
                      body1_lleg=[]
                      body1_rleg=[]
                     # body1_m=[]
                      for i in range(timesteps):
                         a=i*step
                         b=(i+1)*step
                # r=random.randint(a,b)
                         r=random.randrange(a,b,1)
                # print i,a,b,r
                         if(r==f2):
                            r=f2-1
                 #multiful the dataset
                         body1_torso.append(body_torso[r])
                         body1_lhand.append(body_lhand[r])
                         body1_rhand.append(body_rhand[r])
                         body1_lleg.append(body_lleg[r])
                         body1_rleg.append(body_rleg[r])
                        # body1_m.append(body_mirror[r])
                     # print "b:",len(body1)
                      x_train_torso.append(body1_torso)
                      x_train_lhand.append(body1_lhand)
                      x_train_rhand.append(body1_rhand)
                      x_train_lleg.append(body1_lleg)
                      x_train_rleg.append(body1_rleg)
                      y_train.append(tag)
                     # x_train.append(body1_m)
                     # y_train.append(tag)
                     # y_tag[tag1-1]+=1
            break  
            line=file_object.readline()
            #print body
            #print len(body)
            #*video
 #  x_train.append(body1)
 #  y_train.append(tag) 
 # print x_train
  # print len(x_train)
  # print len(x_train[n])
  # if(len(x_train[n])!=timesteps):
   #  print "error:" ,train[0]
  
   #if(len(x_train[n][0])!=350):
    # print len(x_train[n][0])
  # print x_train[n]
  # print x_train[n][0]
  # break
                   #print len(body[1])
   n+=1
   file_object.close()
 #print y_tag
 '''
 print "frame < 100:",frame11
 print "frame 100 -200:",frame12
 print "frame 200-300:",frame23
 '''
 f.close()
 return np.array(x_train_torso),np.array(x_train_lhand),np.array(x_train_rhand),np.array(x_train_lleg),np.array(x_train_rleg),np.array(y_train)

