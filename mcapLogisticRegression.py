#highly inefficient! Too much looping! Store more information in the program

	#One iteration: start 10:14

from sys import maxint
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
	learningRate = 0.05
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

		#numIterations = 50 #abstractly chosen
		numIterations = 1

		self.gradientAscent(numIterations, spamFolder, "spam", regularizationParameter)
		self.gradientAscent(numIterations, hamFolder, "ham", regularizationParameter)

		outputFile = open("weights.txt", "w")
		for w in range(0, self.numFeatures):
			outputFile.write("\n"+self.features[w] + ": " + str(self.weights[w]))
		print "finished training!"

	def gradientAscent(self, numIterations, folder, category, regularizationParameter):
		#X is a list containing Xl
			#Xl is a list containing the number of occurances of each feature in document l
				#So Xl[i] is the # of occurances of feature i in document l
				
		X = []
		for file in os.listdir(os.getcwd() + folder):
			fileText = extractWordsFromFile(open(os.getcwd() + folder + "\\" + file, "r"))
			X.append(self.numOfEachFeatureInDocument(fileText))

		if category is "spam":
			y = 0.0
		elif category is "ham":
			y = 1.0

		for iteration in range(numIterations):	#update each weight 100 times
			print "iteration " + str(iteration) + " out of " + str(numIterations)
			for i in range(1, self.numFeatures):
				print "updating weight " + str(i)
				self.updatewi(y, X, i, folder, category, regularizationParameter)

	def updatewi(self, y, X, i, regularizationParameter):

		regularizationTerm = self.learningRate * regularizationParameter * self.weights[i]

		#calculate sumDifference
		sumDifference = 0.0
		for Xl in X:
			if(Xl[i] is not 0):
				difference = y - self.calculateProbabilitySpam(Xl)
				sumDifference = sumDifference + Xl[i] * difference

		self.weights[i] = self.weights[i] + self.learningRate * sumDifference - regularizationTerm

	def numOfEachFeatureInDocument(self, fileText):
		Xl = [0.0]
		for i in range(1, self.numFeatures):
			#print str(len(self.features)) + " " + str(self.numFeatures) + " " + str(i)
			Xl.append(countTokensOfTerm(fileText, self.features[i]))
		return Xl

	def calculateProbabilitySpam(self, Xl):
		sumwiXli = 0.0
		for i in range(1, self.numFeatures):
			sumwiXli = sumwiXli + self.weights[i] * Xl[i]
		try:
			denominator = 1 + exp(self.weights[0] + sumwiXli)
		except OverflowError:
			denominator = maxint
		return 1.0 / denominator

	#document should be a list of words
	def classify(self, document):
		Xl = self.numOfEachFeatureInDocument(document)

		if self.calculateProbabilitySpam(Xl) > 0.5:
			return "spam"
		else:
			return "ham"

