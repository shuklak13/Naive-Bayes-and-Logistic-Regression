from math import log
from copy import deepcopy

import operator	#used for print10MostFrequent

def countTokensOfTerm(text, term):
	return text.count(term)

def print10MostFrequent(d):
	#list of tuples
	sorted_d = sorted(d.items(), key=operator.itemgetter(1))
	print "Most common terms: " + str(sorted_d[-10:])
	print "Least common terms: " + str(sorted_d[:10])

def unique(lst):
	#print "Total words: " + str(len(list(set(lst))))
	return list(set(lst))

class NBclassifier:
	#class attributes are
		#prior					dictionary of keys="spam" and "ham", value=prior
		#terms 					list of all unique words
		#conditionalProbability	dictionary of keys "spam" and "ham"
			#values are dictionaries with keys=term, value=conditional probability of term

	def __init__(self, spamText, hamText, numSpamDocs, numHamDocs):
		self.train(spamText, hamText, numSpamDocs, numHamDocs)

	def train(self, spamText, hamText, numSpamDocs, numHamDocs):
		self.prior = dict()
		self.prior["spam"] = float(numSpamDocs) / float(numSpamDocs + numHamDocs)
		self.prior["ham"] = float(numHamDocs) / float(numSpamDocs + numHamDocs)
#		print "Prior: " + str(self.prior)

		#terms are unique, text is not
		text = deepcopy(spamText)
		text.extend(hamText)
		self.terms = unique(text)
		#print self.terms

		# print "Spam:"
		self.conditionalProbability = dict()
		self.conditionalProbability["spam"] = self.calculateConditionalProbability(spamText)
		# print self.conditionalProbability["spam"]["ect"]
		# print self.conditionalProbability["spam"]["enron"]
		# print self.conditionalProbability["spam"]["subject"]
		# print self.conditionalProbability["spam"]["convolute"]
		# print self.conditionalProbability["spam"]["osire"]
		# print "\nHam:"
		self.conditionalProbability["ham"] = self.calculateConditionalProbability(hamWords)
		# print self.conditionalProbability["ham"]["ect"]
		# print self.conditionalProbability["ham"]["enron"]
		# print self.conditionalProbability["ham"]["subject"]
		# print self.conditionalProbability["ham"]["convolute"]
		# print self.conditionalProbability["ham"]["osire"]

	def calculateConditionalProbability(self, text):
		termCounts = dict()
		for term in self.terms:
			termCounts[term] = countTokensOfTerm(text, term)+1
		#print10MostFrequent(termCounts)
		termCondProb = dict()
		for term in self.terms:
			termCondProb[term] = float(termCounts[term]+1) / float(sum(termCounts.values()))
		return termCondProb

	def classify(self, document):
		spamScore = self.calculateScore("spam", document)
		hamScore = self.calculateScore("ham", document)
		if spamScore > hamScore:
			return "spam"
		else:
			return "ham"

	def calculateScore(self, category, text):
		score = log(self.prior[category])
		for term in text:
			if term in self.conditionalProbability[category].keys():
				score += log(self.conditionalProbability[category][term])
		return score