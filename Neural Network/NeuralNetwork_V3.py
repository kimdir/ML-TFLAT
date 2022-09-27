import os, csv, time, sys, random
from AdvancedStatistics import AdvancedStatistics
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, TimeDistributed 
#from tensorflow import keras
from keras.callbacks import EarlyStopping,ModelCheckpoint,ReduceLROnPlateau
from keras.initializers import RandomUniform


class NeuralNetwork:
    def __init__(self,
                 modelID,
                 pathList,
                 architecture,
                 nnOptions,
                 units,
                 trainGenList,
                 evalGenList,
                 metrics):

        self.model = None
        self.modelID = modelID
        self.modelPath = pathList[0]

        self.architecture = filter(lambda x: x != "", architecture)
        self.buildOptions = nnOptions['build']
        self.compileOptions = nnOptions['compile']
        self.trainOptions = nnOptions['train']
        self.evalOptions = nnOptions['evaluate']
        self.metrics = metrics
        self.units = units

        self.trainPath =pathList[1]
        self.trainGenList = trainGenList
        self.trainingHistory = None
        self.trainTime = 0
        self.trainFails = 0
        self.trainDate = None
        self.randomSeed = random.randrange(sys.maxsize)

        self.evalPath = pathList[2]
        self.evalGenList = evalGenList
        self.evalGenStats = []
        self.evalStats = []

    def BuildNN(self):

        # Initialize Model
        print("Initializing model...")
        modelName = "Model #" + str(self.modelID)
        self.model = Sequential(name=modelName)
        self.inputShape=(None,self.units)

        # Add layers to model per Architecture instructions
        print(">> Adding layers to ",modelName)
        for i in self.architecture:
            self.LayerSelect(int(i))

        # Build the model
        self.model.build()
        print("Building model...")

        # Compile the model
        self.model.summary()
        self.model.compile(optimizer=self.compileOptions[0],
                           loss=self.compileOptions[1],
                           metrics=self.metrics)

        print("\nModel %s has been built and compiled successfully!\n" % (self.modelID))
        print("-----------------------------------------------------------------")

    def TrainNN(self):

        # Variable Initialization
        trainCount = 0
        failCount = 0
        totalGen = len(self.trainGenList)
        historyList = []
        successfulTrain = False
        trainTimeStart = time.time()
        checkpointPath = os.path.join(self.modelPath,"Model Weights.hdf5")

         # Training Hyperparameters -  See Practice File for descriptions
        set_epochs=int(self.trainOptions[0])
        set_verbose=int(self.trainOptions[1])
        set_initial_epoch=int(self.trainOptions[2])
        set_max_queue_size=int(self.trainOptions[3])

        # Train until successful training occurs
        while not successfulTrain:
            # Set Callbacks
            es = EarlyStopping(monitor="loss",min_delta=0.001,patience=10)
            mc = ModelCheckpoint(checkpointPath,monitor='loss',
                                 verbose=0, save_best_only=True)
            rlr = ReduceLROnPlateau(monitor='loss',factor=0.5,patience=5,
                                    min_delta=0.01)
            my_callbacks = [es,mc,rlr]

            # Train the model
            for gen in self.trainGenList:
                print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")

                history = self.model.fit_generator(gen,
                          epochs=set_epochs,
                          verbose=set_verbose,
                          callbacks=my_callbacks,
                          initial_epoch=set_initial_epoch,
                          steps_per_epoch=len(gen),
                          max_queue_size=set_max_queue_size)

                # Check training quality
                if all(elem == history.history['loss'][0] for elem in history.history['loss']):
                    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                    print("\nBad training, resetting random seed and variables.\n")
                    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                    #trainCount = 0
                    #historyList = []
                    failCount += 1
                    # self.randomSeed = random.randrange(sys.maxsize)
                    # self.BuildNN()
                    # break

                historyList.append(history)
                trainCount += 1
                pctComplete = trainCount/totalGen*100
                print("Training...%0.0f%%" % (pctComplete))
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                print("-----------------------------------------------------------------")
                if trainCount==totalGen:
                    successfulTrain=True

        trainTimeEnd = time.time()
        self.trainingHistory = historyList
        self.trainTime = trainTimeEnd-trainTimeStart
        self.trainFails = failCount
        self.trainDate = time.asctime()

        print("Training Complete for Model %s" % (self.modelID))
        print("Total training time: %0.0f" % (self.trainTime))
        print("Total Fails: %0.0f/%0.0f" % (failCount,len(self.trainGenList)))
        print("\nRandom Seed: ",self.randomSeed,"\n")

        self.OutputTrainingData()

    def EvaluateNN(self):

        # Initialize Evaluation Variables
        evalCount = 0
        resultsHistory = []
        totalEvals = len(self.evalGenList)

        # Evaluate model on all evaluation datasets
        for gen in self.evalGenList:
            results=self.model.evaluate(
                        x=gen,
                        verbose=int(self.evalOptions[0]),
                        steps=len(gen),
                        callbacks=None)
            results = {out: results[i] for i, out in enumerate(self.model.metrics_names)}
            resultsHistory.append(results)
            evalCount += 1
            pctComplete = evalCount/totalEvals*100

            print("Evaluated %0.0f of %0.0f (%0.0f)" % (evalCount,totalEvals,pctComplete))

        # Initialize Statistics Variables
        lossStatPath = os.path.join(self.evalPath,"Loss Statistics.txt")
        lossDataPath = os.path.join(self.evalPath,"Loss Data.csv")
        accStatPath = os.path.join(self.evalPath,"Accuracy Statistics.txt")
        accDataPath = os.path.join(self.evalPath,"Accuracy Data.csv")
        indexPath = os.path.join(self.evalPath,"Epoch Indices.csv")
        statPaths = [lossStatPath,accStatPath]
        csvPaths = [lossDataPath,accDataPath,indexPath]

        lossResults = []
        accResults = []
        indexResults = []

        for index, result in enumerate(resultsHistory):
            # Collect metrics data into a combined list for each metric
            lossResults.append(resultsHistory[index]['loss'])
            accResults.append(resultsHistory[index]['accuracy'])
            indexResults.append(len(resultsHistory[index]))
            
            # # Generate statistics for each generation and output
            # self.evalGenStats = [AdvancedStatistics(result.history['loss']),
            #                      AdvancedStatistics(result.history['accuracy'])]
            # for label_index, stats_class in self.evalGenStats: 
            #     genDataName = "Model %s - Eval Generator %s (% Data)" % (self.modelID, index, self.metrics[label_index])
            #     genStatPath = os.path.join(self.evalPath,"Generator Stats",genDataName + ".txt")
            #     stats_class.OutputToFile(genStatPath,genDataName)

        # Calculate and output Evaluation Statistics
        for dataIndex, data in enumerate([lossResults,accResults]):
            dataName = ("Model %s: %s Data" % (self.modelID,self.metrics[dataIndex]))
            self.evalStats.append(AdvancedStatistics(data))
            self.evalStats[dataIndex].OutputToFile(statPaths[dataIndex],dataName)

        for index, data in enumerate([lossResults,accResults,indexResults]):
            with open (csvPaths[index],'w') as oFile:
                oWriter = csv.writer(oFile)
                oWriter.writerows([data])

        print('------------------------------------------------------------------')
        print("\nEvaluation of Model %f completed!\n" % self.modelID)
        print('------------------------------------------------------------------')

    def LayerSelect(self,index):

        # Kernel Initializer Setup
        ru = RandomUniform(minval=-0.5, maxval=0.5, seed=self.randomSeed)

        # Switch Cases
        if index==0: # Initial Dense Layer
            print("Adding Initial Dense layer...")
            self.model.add(Dense(self.units,
                                 input_shape = self.inputShape,
                                 use_bias = self.buildOptions[index][0],
                                 activation = self.buildOptions[index][1],
                                 kernel_initializer = ru,
                                 bias_initializer = self.buildOptions[index][3]))

        if index==1: # Dense Layer
            print("Adding Dense layer...")
            self.model.add(Dense(self.units,
                                 use_bias = self.buildOptions[index][0],
                                 activation = self.buildOptions[index][1],
                                 kernel_initializer = ru,
                                 bias_initializer = self.buildOptions[index][3]))
            
        elif index==2: # Final Dense Layer
            print("Adding Final Dense layer...")
            self.model.add(Dense(1,
                                 use_bias = self.buildOptions[index][0],
                                 activation = self.buildOptions[index][1],
                                 kernel_initializer = ru,
                                 bias_initializer = self.buildOptions[index][3]))

        elif index==3: # Initial Solo LSTM Layer
            print("Adding Initial Solo LSTM layer...")
            self.model.add(LSTM(self.units,
                                input_shape = self.inputShape,
                                return_sequences = False,
                                use_bias = self.buildOptions[index][0],
                                activation = self.buildOptions[index][1],
                                kernel_initializer=ru,
                                bias_initializer=self.buildOptions[index][3]))
            
        elif index==4: # Solo LSTM Layer
            print("Adding Solo LSTM layer...")
            self.model.add(LSTM(self.units,
                                return_sequences = False,
                                use_bias = self.buildOptions[index][0],
                                activation = self.buildOptions[index][1],
                                kernel_initializer=ru,
                                bias_initializer=self.buildOptions[index][3]))

        elif index==5: # Initial Multi LSTM Layer
            print("Adding Initial Multi LSTM layer...")
            self.model.add(LSTM(self.units,
                                input_shape = self.inputShape,
                                return_sequences = True,
                                use_bias = self.buildOptions[index][0],
                                activation = self.buildOptions[index][1],
                                kernel_initializer=ru,
                                bias_initializer=self.buildOptions[index][3]))


        elif index==6: # Multi LSTM Layer
            print("Adding Multi LSTM layer...")
            self.model.add(LSTM(self.units,
                                return_sequences = True,
                                use_bias = self.buildOptions[index][0],
                                activation = self.buildOptions[index][1],
                                kernel_initializer=ru,
                                bias_initializer=self.buildOptions[index][3]))

        elif index==7: # Final LSTM Layer
            print("Adding Final LSTM layer...")
            self.model.add(LSTM(1,
                                return_sequences = False,
                                use_bias = self.buildOptions[index][0],
                                activation = self.buildOptions[index][1],
                                kernel_initializer=ru,
                                bias_initializer=self.buildOptions[index][3]))
        elif index==8: #TimeDistributed Layer
            print("Adding TimeDistributed layer...")
            self.model.add(TimeDistributed(Dense(self.units,
                                 use_bias = self.buildOptions[index][0],
                                 activation = self.buildOptions[index][1],
                                 kernel_initializer = ru,
                                 bias_initializer = self.buildOptions[index][3])))

        else:
            print("Bad architecture")

    def OutputTrainingData(self):
        # File Path Definitions
        trainingInfoPath = os.path.join(self.trainPath,"Training Info.txt")
        trainingLossPath = os.path.join(self.trainPath,"Training Loss.csv")
        trainingAccPath = os.path.join(self.trainPath,"Training Accuracy.csv")
        trainingIndexPath = os.path.join(self.trainPath,"Training Epoch Indices.csv")

        # Initialize output list variables
        lossOutput = []
        accOutput = []
        indexOutput = []

        # Combine history values
        for history in self.trainingHistory:
            lossOutput.append(history.history['loss'])
            accOutput.append(history.history['accuracy'])
            indexOutput.append(len(history.history['loss']))

        # Training Info Output
        with open(trainingInfoPath,'w') as infoFile:
            infoFile.write("Training Date: %s\n" % self.trainDate)
            infoFile.write("Training Random Seed: %f\n" % self.randomSeed)
            infoFile.write("Training Time: %f\n" % self.trainTime)
            infoFile.write("Training Failures: %f/%f\n" % (self.trainFails,
                                                           len(self.trainGenList)))

        # Training Loss Output
        with open(trainingLossPath,'w') as lossFile:
            lossWriter = csv.writer(lossFile)
            lossWriter.writerows(lossOutput)

        # Training Accuracy Output
        with open(trainingAccPath,'w') as accFile:
            accWriter = csv.writer(accFile)
            accWriter.writerows(accOutput)

        # Training Index Output
        with open(trainingIndexPath,'w') as indexFile:
            indexWriter = csv.writer(indexFile)
            indexWriter.writerows([indexOutput])

    def LoadNN(self,loadPath):
        self.model = load_model(loadPath)
