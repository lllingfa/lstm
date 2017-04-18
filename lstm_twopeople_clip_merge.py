import sys
from getdata_twopeople_clipmn_tree_merge import getdata
from getdata_twopeople_clip_tree_merge import getdata1
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dropout, Activation, Dense, Embedding, Masking
from keras.layers import LSTM, Merge
from keras.callbacks import ModelCheckpoint
from keras.regularizers import l2, activity_l2
from keras.optimizers import RMSprop
import keras
import time
sys.setrecursionlimit(10000)
TIMESTEPS = 8
samplesnum = 512
samplesnum1 = 1000
X_train, X_train1 , y_train = getdata('/home/icme/datasets/trainlist_twopeople', timesteps = TIMESTEPS)
X_test, X_test1 , y_test = getdata1('/home/icme/datasets/testlist_twopeople', timesteps = TIMESTEPS)
class Callback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch,logs={}):
        score, acc = model.evaluate([X_test,X_test1],y_test)
        print('epoch: ',epoch)
        print('Test score:', score)
        print('Test accuracy:', acc)
    
        
print X_train.shape,y_train.shape, X_train1.shape,y_train.shape
print X_test.shape,y_test.shape
callback = Callback()
#model.load_weights('my_weights/weights-2017-03-17-15:59:36.hdf5')
#for layer in model.layers:
 #   layer.trainable=True 

sgd = keras.optimizers.SGD(lr = 0.1, decay = 1e-5, momentum=0.9, nesterov=True)
adadelta = keras.optimizers.Adadelta(lr = 1e-09,rho=0.95, epsilon=1e-6)
#for two people merge
submodels = [0] * 2
for i in range(2):
 # modelc = 'model'+i
  submodels[i]= Sequential()
#process variable size
  submodels[i].add(Masking(mask_value= -1,input_shape=(TIMESTEPS, 129)))
  submodels[i].add(LSTM(512,input_length=TIMESTEPS, input_dim = 129,dropout_W=0.2, dropout_U=0.2,return_sequences = True))
  submodels[i].add(Dropout(0.2))
  submodels[i].add(LSTM(512,dropout_W=0.2, dropout_U=0.2,return_sequences = False))
#model1.add(Dropout(0.2))
#model1.add(Dense(60,W_regularizer=l2(0.02), activity_regularizer=activity_l2(0.01),activation='softmax'))
  print submodels[i].summary()
 # print submodels[i].name
#merge 
model = Sequential()
model.add(Merge(submodels,mode='concat'))
#model.add(Lambda(f, output_shape=(70,600))
#model.add(Flatten())
#model.add(Dense(60))
#model.add(Activation('softmax'))
model.add(Dense(60,W_regularizer=l2(0.02), activity_regularizer=activity_l2(0.01),activation='softmax'))
rmsprop=RMSprop(lr=0.0001,rho=0.9,epsilon=1e-08,decay=0.0)

model.load_weights('model/weights-twopeoplemerge-clip-8-lstmtreemn-2017-04-05-21:56:30.hdf5')
for layer in model.layers:
    layer.trainable = True
#model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics = ['accuracy'])
model.compile(loss='categorical_crossentropy', optimizer=rmsprop,metrics = ['accuracy'])
#model.compile(loss='categorical_crossentropy', optimizer=adadelta, metrics = ['accuracy'])
#model.compile(loss='categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
#  model.compile(loss='mean_absolute_error',
#            optimizer=sgd,
#            metrics=['accuracy'])

ISOTIMEFORMAT='%Y-%m-%d-%X'
times=time.strftime( ISOTIMEFORMAT, time.localtime(time.time()))

checkpointer = ModelCheckpoint(filepath='model/weights-twopeoplemerge-clip-8t-lstmtreemn-'+str(times)+'.hdf5', verbose=1, save_best_only=True)
#write to log
#csv_logger = CSVLogger('/model_log/training.log')
model.fit([X_train,X_train1], y_train,nb_epoch = 200,batch_size=64,verbose=1,callbacks=[callback,checkpointer],validation_split=0.05)
#model.save('model/my_model.h5') #hdf5
#model.save_weights('model/my_model_weight.h5')
#load
#model=load_model('model/my_model.h5')
#print model.summary()
