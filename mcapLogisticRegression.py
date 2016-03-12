#highly inefficient! Too much looping! Store more information in the program

import os
import re #regex - used to remove non-alphabetic characters
from math import log, exp
from copy import deepcopy

def countTokensOfTerm(text, term):
	return text.count(term)

def unique(lst):
	return list(set(lst))

#filters nonalphabetic characters and lowercases everything
def format(words):
	filteredWords = []
	regex = re.compile('[^a-zA-Z]')
	for word in words:
		newWord = regex.sub('', word).lower() 
		if "" != newWord and len(newWord) > 1:
			filteredWords.append(newWord)
	return filteredWords

def extractWordsFromFile(file):
	words = []
	for line in file:
		newWords = format(line.split())
		words.extend(newWords)
	return words


class LRclassifier:

	learningRate = 0.01
	features = []	#words in our text
	weights = []	#weights for each feature - default to 1.0

	def __init__(self, spamText, hamText, spamFolder, hamFolder, regularizationParameter):
		self.train(spamText, hamText, spamFolder, hamFolder, regularizationParameter)

	def train(self, spamText, hamText, spamFolder, hamFolder, regularizationParameter):

		#initialize features and weights
		text = deepcopy(spamText)
		text.extend(hamText)
		self.features = unique(text)
		self.numFeatures = len(self.features)
		for i in range(self.numFeatures+1):
			self.weights.append(1.0)

		numIterations = 100 #abstractly chosen

		self.gradientAscent(numIterations, spamFolder, "spam", regularizationParameter)
		self.gradientAscent(numIterations, hamFolder, "ham", regularizationParameter)

		print "weight 0 " + str(self.weights[0])
		print "weight 1 " + str(self.weights[1])
		print "weight 2 " + str(self.weights[2])

	def gradientAscent(self, numIterations, folder, category, regularizationParameter):

		#Xs is a list containing a list for each file
			#each sublist containing the number of occurances of each feature in that file
		Xs = []
		for file in os.listdir(os.getcwd() + folder):
			print "Extracting text from file..."
			fileText = extractWordsFromFile(open(os.getcwd() + folder + "\\" + file, "r"))
			print "Finding number of each feature in file"
			Xs.append(self.numOfEachFeatureInDocument(fileText))

		for iteration in range(numIterations):	#update each weight 100 times
			print "iteration " + str(iteration) + " out of " + str(numIterations)
			for i in range(1, self.numFeatures):
				print "updating weight " + str(i)
				self.updatewi(i, folder, category, regularizationParameter)

	def updatewi(self, i, folder, category, regularizationParameter):
		if category is "spam":
			y = 1.0
		elif category is "ham":
			y = 0.0

		regularizationTerm = self.learningRate * regularizationParameter * self.weights[i]

		#calculate sumDifference
		sumDifference = 0.0
		for X in Xs:
			for j in range(1, self.numFeatures):
				difference = y - self.calculateProbabilitySpam(X)
				sumDifference = sumDifference + X[j] * difference

		self.weights[i] = self.weights[i] + self.learningRate * sumDifference - regularizationTerm

	def numOfEachFeatureInDocument(self, fileText):
		X = [0.0]
		for i in range(1, self.numFeatures):
			#print str(len(self.features)) + " " + str(self.numFeatures) + " " + str(i)
			X.append(countTokensOfTerm(fileText, self.features[i]))
		return X

	def calculateProbabilitySpam(self, X):
		sumwiXi = 0.0
		for i in range(1, self.numFeatures):
			sumwiXi = sumwiXi + float(self.weights[i] * X[i])
		return 1.0 / (1 + exp(self.weights[0] + sumwiXi))

	#document should be a list of words
	def classify(self, document):
		if self.calculateProbabilitySpam(document) > 0.5:
			return "spam"
		else:
			return "ham"

