#!/usr/bin/env python

"""
Plot iperf data
"""

import json
import os
import sys
import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from optparse import OptionParser


pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)

class iperf3_plotter(object):
    def __init__(self, upperLimit, lowerLimit,bound):
        sns.set_style("white")
        self.upperbond=upperLimit
        self.lowerbond=lowerLimit
        self.bound=bound
 
    def defTableu(self):
        tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
                     (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
                     (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
                     (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
                     (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
        for i in range(len(tableau20)):  
            r, g, b = tableau20[i]  
            tableau20[i] = (r / 255., g / 255., b / 255.)  
        return tableau20

    def plotBox(self, dataset,filename, desc, title):
        fig, ax = plt.subplots()
        # # the size of A4 paper
        fig.set_size_inches(12,14)

        # create our boxplot which is drawn on an Axes object
        sns.boxplot(data=dataset,orient="h", palette="Set2")
        filename = filename.replace(".png","_box.png")
        plt.title(title)
        plt.savefig(filename, bbox_inches="tight")

    def plotLine(self, dataset, filename, desc, title, figureN):
        sns.set_style("white")
        f, axs = plt.subplots(figureN, sharex=True, sharey=True)
        f.set_size_inches(12,14)
        i=0

        tableau20 = self.defTableu()
        upperbond=self.upperbond
        lowerbond=self.lowerbond
        for c in dataset.columns:
            axs[i].spines["left"].set_visible(False) 
            axs[i].spines["right"].set_visible(False) 
            axs[i].get_xaxis().tick_bottom()  
            axs[i].get_yaxis().tick_left()  
            axs[i].set_title(c)
            axs[i].plot(dataset.index, dataset[c],color=tableau20[i])
            if self.upperbond >0 : axs[i].plot(dataset.index,[upperbond]* len(dataset.index),"--", lw=2, color="red", alpha=0.5)
            if self.upperbond >0 : axs[i].plot(dataset.index,[lowerbond]* len(dataset.index),"--", lw=2, color="red", alpha=0.5)

            i=i+1
            if i==5: break
        # plt.title(title)
        plt.savefig(filename, bbox_inches="tight")    
        
    def plotLinePretty(self, dataset,filename, desc, title):
        tableau20 = self.defTableu()

        y_level = int((int(dataset.values.max()) - int(dataset.values.min()))/20)
        if y_level==0:
            y_level = (dataset.values.max()-dataset.values.min())/20
        
        y_max = dataset.values.max()+y_level
        y_min = dataset.values.min()

        x_max = dataset.index[-1]
        x_min = dataset.index[0]
        x_level = (x_max - x_min)/6
 

        plt.figure(figsize=(12, 14))  
        ax = plt.subplot(111)  
        ax.spines["top"].set_visible(False)  
        ax.spines["bottom"].set_visible(False)  
        ax.spines["right"].set_visible(False)  
        ax.spines["left"].set_visible(False)  

        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()  

        plt.ylim(y_min, y_max)
        plt.xlim(x_min, x_max)  

        plt.yticks(np.arange(y_min, y_max, y_level), [str(round(x,3)) for x in np.arange(y_min, y_max, y_level)], fontsize=14)
        plt.xticks(fontsize=14)  


        for y in np.arange(y_min, y_max, y_level):  
            plt.plot(np.arange(x_min, x_max), [y] * len(np.arange(x_min, x_max)), "--", lw=1, color="black", alpha=0.3)  


        plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                        labelbottom="on", left="off", right="off", labelleft="on")  

        clients = dataset.columns
        i=0;
        for rank, column in enumerate(clients):
            plt.plot(dataset.index, dataset[column].values, lw=1,color=tableau20[rank%20])  
            # y_pos = dataset[column].values[-1]
            y_pos = dataset[column].mean()
            # print(column,dataset[column].values[-1], dataset[column].mean() )
            plt.text(x_max + x_level/2, y_pos, column, fontsize=12, color=tableau20[rank % 20])
            i=i+1

        j=0;
        for (upper_bound, lower_bound, tags) in self.bound:
            # print(str(upper_bound), str(lower_bound), tags)
            if upper_bound >0 : plt.plot(dataset.index,[upper_bound]* len(dataset.index), lw=2, color=tableau20[j%20] )
            plt.text(x_max, upper_bound, tags, fontsize=12, color=tableau20[j % 20])
            if lower_bound >0 : plt.plot(dataset.index,[lower_bound]* len(dataset.index), lw=2, color=tableau20[j%20] )
            plt.text(x_max, lower_bound, tags, fontsize=12, color=tableau20[j % 20])
            j=j+1


        plt.title(title, fontsize=17)
        # plt.text(x_min+(x_max-x_min)/2, y_max, title, fontsize=17, ha="center")
        plt.text(x_max, y_max, desc, fontsize=10) 
        plt.savefig(filename, bbox_inches="tight") 

class iperf3_dataParser(object):
    def getOptionParser(self):
        usage = '%prog [ -f FOLDER | -o OUT | -p PLOTFILES | -n NOPLOTFILES | -v ]'
        return OptionParser(usage=usage)

    def parseOptions(self, args):
        parser = self.getOptionParser()
        parser.add_option('-f', '--folder', metavar='FILE',
                      type='string', dest='foldername',
                      help='Input folder absolute path. [Input Format: /Users/iperfExp]')

        parser.add_option('-o', '--output', metavar='OUT',
                      type='string', dest='output', default="iperf.png",
                      help='Plot file name. [Input Format: iperf.png]')

        parser.add_option('-p', '--plotfiles', metavar='PLOT_FILES',
                      type='string', dest='plotFiles', default="",
                      help='Choose files to be plotted. If no specified, all files in folder. [Input Format: f1,f2,f3]')

        parser.add_option('-n', '--noPlotFiles', metavar='NO_PLOT_FILES',
                      type='string', dest='noPlotFiles', default="",
                      help='Choose files not to be plotted. [Input Format: f1,f2,f3]')

        parser.add_option('-u', '--upperLimit',  metavar='UPPER_LIMIT',
                      type='float', dest='upperLimit', default=0,
                      help='The expected upper boundary. [Input Format: 0.5]')

        parser.add_option('-l', '--lowerLimit',  metavar='LOWER_LIMIT',
                      type='float', dest='lowerLimit', default=0,
                      help='The expected lower boundary. [Input Format: 0.5]')

        parser.add_option('-b', '--bound', metavar='BOUND',
                      type='string', dest='bound', default="",
                      help='Provide multiple bound in pairs. [Input Format: [upperbound, lowerbound, tag]')


        parser.add_option('-v', '--verbose',
                      dest='verbose', action='store_true', default=False,
                      help='Verbose debug output to stderr.')

        options, _ = parser.parse_args(args)
        # print(options)
        if not options.foldername:
            parser.error('Foldername is required.')
        else:
            self.foldername = options.foldername

        if options.plotFiles=="":
            self.plotFiles=[]
        else:
            self.plotFiles = map(lambda x:x.strip(), options.plotFiles.split(",")) if "," in options.plotFiles else [options.plotFiles.strip()]

        if options.noPlotFiles=="":
            self.noPlotFiles=[]
        else:
            self.noPlotFiles = map(lambda x:x.strip(), options.noPlotFiles.split(",")) if "," in options.noPlotFiles else [options.noPlotFiles.strip()]

        self.bound = []
        if options.bound=="":
            self.bound=[]
        else:
            # print(options.bound)
            bounds_tmp = map(lambda x:x.strip(), options.bound.split("]")) if "]" in options.bound else [options.bound.strip()]
            for bt in bounds_tmp:
                bt = bt.replace("[", "")
                bt_arr = map(lambda x:x.strip(), bt.split(","))
                bound_item=[]
                for b in bt_arr:
                    if b.strip()!= "":
                        bound_item.append(b)
                if len(bound_item)==3:
                    bound_item[0]=float(bound_item[0])
                    bound_item[1]=float(bound_item[1])
                    self.bound.append(bound_item)

        self.output = options.output
        return (self.foldername, list(self.plotFiles), list(self.noPlotFiles), self.output,options.upperLimit,options.lowerLimit, self.bound)

    def generate_BW(self, iperf):
        """Do the actual formatting."""
        idx=[]
        value=[]
        duration = iperf.get('start').get('test_start').get('duration')
        for i in iperf.get('intervals'):
            for ii in i.get('streams'):
                if (round(float(ii.get('start')), 0)) <= duration:
                    idx.append(round(float(ii.get('start')), 0))
                    value.append(round(float(ii.get('bits_per_second')) / (1024*1024), 3))
        return pd.Series(value, index=idx)

    def get_plotFiles(self,foldername, plotFiles, noPlotFiles):
        # print(foldername, plotFiles, noPlotFiles)
        if len(plotFiles)==0:
            for root, dirs, files in os.walk(foldername, topdown=False):
                for filename in files:
                    plotFiles.append(filename)
        else:
            for root, dirs, files in os.walk(foldername, topdown=False):
                i=0;
                while i < len(plotFiles):
                    if plotFiles[i] not in files:
                        del plotFiles[i]
                    else:
                        i = i+1;

        for f in noPlotFiles:
            if f in plotFiles: plotFiles.remove(f)

        return plotFiles

    def get_dataset(self, plotFiles):
        datasetIndex=[]
        raw_arrays=[]
        for name in plotFiles:
            if "json" in name:
                datasetIndex.append(name.replace(".json",""))
            else:
                datasetIndex.append(name)
            file_path = foldername+os.path.sep+str(name)
            with open(file_path, 'r') as fh:
                data = fh.read()

            try:
                iperf = json.loads(data)
            except Exception as ex:  # pylint: disable=broad-except
                print('Could not parse JSON from file (ex): {0}'.format(str(ex)))

            raw_arrays.append(self.generate_BW(iperf))


        dataset=pd.concat(raw_arrays, axis=1)
        dataset.columns=datasetIndex
        dataset.index.names=['start']
        # dataset.apply(lambda x: x.fillna(x.mean(),inplace=True),axis=0)
        dataset = dataset.fillna(method='ffill')

        return dataset

# if __name__ == '__main__':
#     s = iperf3_dataParser()
#     (foldername, plotFiles, noPlotFiles, output, upperLimit, lowerLimit,bound) = s.parseOptions(sys.argv[1:])
#     print (foldername, plotFiles, noPlotFiles, output, upperLimit, lowerLimit,bound)


if __name__ == '__main__':
    """Execute the read and formatting."""
    s = iperf3_dataParser()
    (foldername, plotFiles, noPlotFiles, output, upperLimit, lowerLimit, bound) = s.parseOptions(sys.argv[1:])
    print('foldername {}\nplotFiles {}\nnoPlotFiles {}\noutput {}\nupperLimit {}\nlowerLimit {}\nbound {}\n'.format(foldername,str(plotFiles), str(noPlotFiles), output, upperLimit, lowerLimit,str(bound)))

    plotFiles=s.get_plotFiles(foldername, plotFiles, noPlotFiles)
    # print (plotFiles)

    if len(plotFiles) > 0:
        dataset = s.get_dataset(plotFiles)
        plotter = iperf3_plotter(upperLimit, lowerLimit, bound)
        #plot overall box
        dataset.to_csv(output+".csv")
        dataset.describe().to_csv(output + "_stats.csv")
        desc="x_labels: Seconds\ny_lebel: Mbps\nclients: "+str(len(dataset.columns))
        title= "iperf throughput Mbps per seconds"
        # if len(bound) > 0:
        plotter.plotBox(dataset,output, desc, title)

        #plot individual
        if upperLimit>=0 and lowerLimit >=0:
            s=0
            e=0
            shift=5
            output_single = output
            while e < len(dataset.columns):
                e = e + shift
                if e >=len(dataset.columns):
                    e = len(dataset.columns)
                plotDf = dataset[dataset.columns[s:e]]
                output_single = output.replace(".png", "_line_"+str(s)+".png")
                plotter.plotLine(plotDf, output_single,desc, title, shift)
                output_single = output
                s = e

        #plot all lines, sort by mean value/column
        if len(bound) >=0:
            dataset = dataset.reindex_axis(dataset.mean().sort_values().index, axis=1)
            # last_row_name = dataset.index[-1]
            # dataset = dataset.T.sort(columns=last_row_name, ascending=False).T
            # dataset.to_csv(output + "_sort_by_mean.csv")
            plotter.plotLinePretty(dataset, output,desc, title)
