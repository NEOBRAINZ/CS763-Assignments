import torch
import numpy as np
import math

class CE_criterion():
    def __init__(self):
        pass
    
    def backward(self, y_hat, y):
        #y_hat and y both are encoded/embedded
        nC = y_hat.size()[0]
        logProbabs = torch.log(y_hat)*y
        loss = -1*torch.sum(logProbabs)/nC
        grad = y_hat - y
        return loss, grad


class Criterion():
	def __init__(self):
		pass

	def forward(self, input, target):
		lenn = input.size()[0]
		indices = target.view(lenn).numpy()
		hotTarget = (torch.zeros(input.size())).type(torch.DoubleTensor)
		hotTarget[np.arange(lenn), indices] = 1

		##convert input using softmax
		probabs = input - torch.max(input, dim=1, keepdim=True)[0]
		probabs = probabs.exp()
		probabs = probabs/probabs.sum(dim = 1, keepdim = True)
		
		##compute log probabs for cross entropy
		#probabs = hotTarget*probabs +  (1 - hotTarget)*(1 - probabs)
		logProbabs = ((probabs).log())*hotTarget
		return -(logProbabs.sum())/float(lenn)

	def backward(self, input, target):
		lenn = input.size()[0]
		b = input.size()[1]
		indices = target.view(lenn).numpy()
		hotTarget = (torch.zeros(input.size())).type(torch.DoubleTensor)
		hotTarget[np.arange(lenn), indices] = 1

		##convert input using softmax
		probabs = input - torch.max(input, dim=1, keepdim=True)[0]
		probabs = probabs.exp()
		probabs = probabs/probabs.sum(dim = 1, keepdim = True)
		#probabs = hotTarget*probabs +  (1 - hotTarget)*(1 - probabs)
		
		##calculate the loss
		logProbabs = (probabs).log()*hotTarget 
		loss = -(logProbabs.sum())/float(lenn)

		##calculate derivative
		grad = probabs - hotTarget
		grad = grad/float(lenn)
		return grad, loss