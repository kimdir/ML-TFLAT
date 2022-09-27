

class AdvancedStatistics:
    def __init__(self,data):
        import statistics as stat
        import math

        # Data set being analyzed
        self.data = sorted(data)

        # >>> Basic Descriptive Statistics <<<
        # Central Measures
        self.mean = stat.mean(data)
        self.harmonicMean = stat.harmonic_mean(data)
        #self.low_median = stat.low_median(data)
        self.median = stat.median(data)
        #self.high_median = stat.high_median(data)
        try:
            self.mode = stat.mode(data)
        except:
            self.mode = 0

        self.CentralMeasures = [self.mean,
                                self.harmonicMean,
                                #self.low_median,
                                self.median,
                                #self.high_median,
                                self.mode]

        # Spread Measures
        self.stdev = stat.stdev(data)
        self.variance = stat.variance(data)
        self.range = data[-1]-data[0]

        self.SpreadMeasures = [ self.stdev,
                                self.variance,
                                self.range]

        # >>> Advanced Descriptive Statistics <<<
        # Percentiles
        self.pct10 = self.GetPercentile(10)
        self.pct25 = self.GetPercentile(25)
        self.pct50 = self.GetPercentile(50)
        self.pct75 = self.GetPercentile(75)
        self.pct90 = self.GetPercentile(90)
        self.IQR = self.pct75 - self.pct25

        self.Percentiles = [self.pct10,
                            self.pct25,
                            self.pct50,
                            self.pct75,
                            self.pct90,
                            self.IQR]

        # Deviations
        self.MAD = self.M_Function(mode='MAD')
        self.MADM = self.M_Function(mode='MADM')

        self.Deviations = [self.MAD,
                           self.MADM]

        # Coefficients
        self.COV = self.stdev/self.mean
        self.COD = self.MADM/self.median

        self.Coefficients = [self.COV,
                             self.COD]

        # Distribution Descriptors
        try:
            self.skewness = self.M_Function(exp=3)/(self.M_Function(exp=2)**(3/2))
        except:
            self.skewness = 0
        try:
            self.kurtosis = self.M_Function(exp=4)/(self.M_Function(exp=2)**(2))
        except:
            self.kurtosis = 0

        self.DistributionDescriptors = [self.skewness,
                                        self.kurtosis]

    def OutputToFile(self,path,dataName):

        with open(path,'w') as oFile:
            oFile.write(">>> Statistics for %s <<<\n\n" % dataName)
            oFile.write("\n--------------------------------------")
            oFile.write("\n---------- Basic Statistics ----------")
            oFile.write("\n--------------------------------------")

            oFile.write("\n~~~~~~~~~~ Central Measures ~~~~~~~~~\n")
            oFile.write("\nMean: %f" % self.mean)
            oFile.write("\nHarmonic Mean: %f" % self.harmonicMean)
            #oFile.write("Low Median: %f" % self.low_median)
            oFile.write("\nMedian: %f" % self.median)
            #oFile.write("High Median: %f" % self.high_median)
            oFile.write("\nMode: %f" % self.mode)

            oFile.write("\n~~~~~~~~~~ Spread Measures ~~~~~~~~~~\n")
            oFile.write("\nStandard Deviation: %f" % self.stdev)
            oFile.write("\nVariance: %f" % self.variance)
            oFile.write("\nRange: %f" % self.range)

            oFile.write("\n\n--------------------------------------")
            oFile.write("\n-------- Advanced Statistics ---------")
            oFile.write("\n-------------------------------------")

            oFile.write("\n~~~~~~~~~~~~ Percentiles ~~~~~~~~~~~~\n")
            oFile.write("\n10th Percentile: %f" % self.pct10)
            oFile.write("\n25th Percentile: %f" % self.pct25)
            oFile.write("\n50th Percentile: %f" % self.pct50)
            oFile.write("\n75th Percentile: %f" % self.pct75)
            oFile.write("\n90th Percentile: %f" % self.pct90)
            oFile.write("\nInterquartile Range: %f" % self.IQR)

            oFile.write("\n~~~~~~~~~~~~~ Deviations ~~~~~~~~~~~~\n")
            oFile.write("\nMean Absolute Deviation: %f" % self.MAD)
            oFile.write("\nMean Absolute Deviation from the Median: %f" % self.MADM)

            oFile.write("\n~~~~~~~~~~~~ Coefficients ~~~~~~~~~~~\n")
            oFile.write("\nCoefficient of Variation : %f" % self.COV)
            oFile.write("\nCoefficient of Dispersion: %f" % self.COD)

            oFile.write("\n~~~~~ Distribution Descriptions ~~~~~\n")
            oFile.write("\nSkewness: %f" % self.skewness)
            oFile.write("\nKurtosis: %f" % self.kurtosis)

    def GetPercentile(self,percentile):
        import math
        pctIndex = math.floor(len(self.data)*(.01*percentile))
        pctVal = self.data[int(pctIndex)]

        return pctVal

    def M_Function(self,mode=None,exp=1):
        try:
        # MAD Mode: Computes the Mean Absolute Deviation
            if(mode=='MAD'):
                M_Val = sum([abs(x-self.mean) for x in self.data])/len(self.data)
    
            # MADM Mode: Calculates the Mean Absolute Deviation from the Median
            elif(mode=='MADM'):
                M_Val = sum([abs(x-self.median) for x in self.data])/len(self.data)
    
            # Default Mode, used for skewness and kurtosis
            else:
                M_Val = sum([(x-self.mean)**exp for x in self.data])/len(self.data)
        except:
            return 0
        return M_Val


