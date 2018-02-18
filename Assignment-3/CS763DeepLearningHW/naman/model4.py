import matplotlib
matplotlib.use('Agg')

import torch 
from readData import *
from imports import *
from PCA import *
import matplotlib.pyplot as plt


#print(data.size())
pca = torch.load('pca.model')

data = pca.convert_data(data)
valData = pca.convert_data(valData)

#print(data.size())
##make the model
model = Model()
model.addLayer(Linear(600, 100))
model.addLayer(ReLU())
model.addLayer(Linear(100, 60))
model.addLayer(ReLU())
# model.addLayer(Linear(200, 50))
# model.addLayer(ReLU())
model.addLayer(Linear(60, 6))

lossClass = Criterion()

learningRate = 1e-4
par_regularization = 1e-3

batchSize = 128
plotIndex = 0
losses = []
plotIndices = []

def train(iterations, whenToPrint):
	global learningRate,par_regularization
	global model, dataSize, batchSize, plotIndex, losses, plotIndices
	for i in range(iterations):
		indices = (torch.randperm(dataSize)[:batchSize]).numpy()
		currentData = data[indices, :]
		currentLabels = labels.view(dataSize, 1)[indices, :]
		yPred = model.forward(currentData)
		lossGrad, loss = lossClass.backward(yPred, currentLabels)
		if i%whenToPrint == 0:
			reg_loss = model.regularization_loss(par_regularization)
			print("Iter - %d : Training-Loss = %.4f Regularization-Loss = %.4f and Total-loss = %.4f"%(i, loss,reg_loss,loss+reg_loss))
			losses.append(loss)
			plotIndices.append(plotIndex)
		model.clearGradParam()
		model.backward(currentData, lossGrad)
		for layer in model.Layers:
			if layer.isTrainable:
				layer.weight -= (learningRate*layer.gradWeight + par_regularization*layer.weight)
				layer.bias -= (learningRate*layer.gradBias + par_regularization*layer.bias)
		plotIndex += 1


def trainAcc():
	global data
	yPred = model.forward(data)
	N = data.size()[0]
	return ((yPred.max(dim=1)[1].type(torch.LongTensor) == labels.type(torch.LongTensor)).sum())/N

def valAcc():
	global valData
	yPred = model.forward(valData)
	N = valData.size()[0]
	return ((yPred.max(dim=1)[1].type(torch.LongTensor) == valLabels.type(torch.LongTensor)).sum())/N

def makePlot():
	global losses, plotIndices
	plt.plot(plotIndices, losses)
	plt.show()

def saveModel():
	import pickle
	pickle.save(model1,open('output.dat','wb'))

def useOldModel():
	import pickle
	pickle.load(open('model1.pickle',"rb"))



