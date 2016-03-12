from math import log
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

	self.learningRate = 0.01
	self.features = []	#words in our text
	self.weights = []	#weights for each feature - default to 1.0

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

		gradientAscent(spamFolder, "spam", regularizationParameter)
		gradientAscent(hamFolder, "ham", regularizationParameter)

	def gradientAscent(self, folder, category, regularizationParameter):
		for iteration in range(100):	#update each weight 100 times
			for i in range(1, numFeatures+1):
				updatewi(folder, category, regularizationParameter)

	def updatewi(self, i, category, regularizationParameter):
		if category is "spam":
			y = 1.0
		elif category is "ham":
			y = 0.0

		sumDifference = 0.0
		for file in os.listdir(os.getcwd() + folder):
			fileText = extractWordsFromFile(open(os.getcwd() + folder + "\\" + file, "r"), filter)
			X = [0.0]	#we skip the first element of X
			for i in range(1, numFeatures+1)
				X.append(countTokensOfTerm(fileText, features[i]))
			for i in 1:(numFeatures+1):
				difference = y - calculateProbabilitySpam
				sumDifference = sumDifference + X[i] * difference

		regularizationTerm = learningRate*regularizationParameter*self.weights[i]

		self.weights[i] = self.weights[i] + learningRate * sumDifference - regularizationTerm

	def calculateProbabilitySpam(self, X):
		sumwiXi = 0.0
		for i in range(1, self.numFeatures+1):
			sumwiXi = sumwiXi + float(weights[i] * X[i])
		return 1.0 / (1 + exp(wiXi[0] + sumwiXi))

	#document should be a list of words
	def classify(self, document):
		if self.calculateProbabilitySpam(document) > 0.5:
			return "spam"
		else:
			return "ham"

