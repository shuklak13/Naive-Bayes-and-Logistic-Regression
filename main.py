#Problems:
#	1 - Stopword filtering doesn't change accuracy
#	3 - Logistic Regression unimplemented

import os
import re #regex - used to remove non-alphabetic characters
from multinomialNaiveBayes import NBclassifier
from mcapLogisticRegression import LRclassifier

stopwords = ["", "a","about","am","an","and","are","aren't","as","at","be","by","could","couldn't","can't","did","didn't","do","does","doesn't","doing","don't","for","from","had","hasn't","have","has","he","her","here","him","hers","his","i","if","in","is","isn't","it","it's","its","itself","me","my","myself","of","on","or","our","ours","ourselves","she","should","than","that","that's","the","their","theirs","them","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","throuh","to","too","until","was","wasn't","we","we'd","we'll","we're", "we've","were","weren't","what","what's","when","when's","where","where's","while","who","who's","whom", "with", "would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]

def filterStopwords(words):
	filteredWords = []
	for word in words:
		if word not in stopwords:
			filteredWords.append(word)
	return filteredWords

#filters nonalphabetic characters and lowercases everything
def format(words):
	filteredWords = []
	regex = re.compile('[^a-zA-Z]')
	for word in words:
		newWord = regex.sub('', word).lower() 
		if "" != newWord and len(newWord) > 1:
			filteredWords.append(newWord)
	return filteredWords

def extractWordsFromFile(file, filter):
	words = []
	for line in file:
		newWords = format(line.split())
		if filter:
			newWords = filterStopwords(newWords)
		words.extend(newWords)
	return words

def getWordsFromFolder(folder, filter):
	words = []
	for file in os.listdir(os.getcwd() + folder):
		fileWords = extractWordsFromFile(open(os.getcwd() + folder + "\\" + file, "r"), filter)
		words.extend(fileWords)
	#print "Num " + folder + " words: " + str(len(list(set(words))))
	return words

def countDocsInFolder(folder):
	return len(os.listdir(os.getcwd() + folder))

def test(numberOf, classifier, testFolder, correctClass):
	for file in os.listdir(os.getcwd() + testFolder):
		fileText = extractWordsFromFile(file, filter)
		classification = classifier.classify(fileText)
		#print str(classification) + str(correctClass)
		if classification == correctClass:
			numberOf["Correct"] = numberOf["Correct"] + 1
		numberOf["Total"] = numberOf["Total"] + 1
	return numberOf

def accuracy(classifier, spamTestFolder, hamTestFolder, filter):
	numberOf = dict()
	numberOf["Correct"] = 0
	numberOf["Total"] = 0
	numberOf = test(numberOf, classifier, spamTestFolder, "spam")
	numberOf = test(numberOf, classifier, hamTestFolder, "ham")
	return float(numberOf["Correct"]) / float(numberOf["Total"])

def reportClassifierAccuracies(filter):
	spamFolderTrain = "\\train\\spam"
	spamWords = getWordsFromFolder(spamFolderTrain, filter)
	numSpamDocs = countDocsInFolder(spamFolderTrain)

	hamFolderTrain = "\\train\\ham"
	hamWords = getWordsFromFolder(hamFolderTrain, filter)
	numHamDocs = countDocsInFolder(hamFolderTrain)

	#nb = NBclassifier(spamWords, hamWords, numSpamDocs, numHamDocs)
	lr01 = LRclassifier(spamWords, hamWords, spamFolderTrain, hamFolderTrain, 0.01)

	if filter:
		print "Accuracy with Stopword Fitlering"
	else:
		print "Accuracy without Stopword Filtering"

	spamFolderTest = "\\test\\spam"
	hamFolderTest = "\\test\\ham"
	#print(accuracy(nb, spamFolderTest, hamFolderTest, filter))
	print(accuracy(lr01, spamFolderTest, hamFolderTest, filter))

###############################################################################

if __name__ == "__main__":
	reportClassifierAccuracies(False)
	reportClassifierAccuracies(True)