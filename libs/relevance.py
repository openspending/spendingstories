#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 16-Aug-2013
# Last mod : 16-Aug-2013
# -----------------------------------------------------------------------------

class Relevance:

	def __init__(self, amount=None, compared_to=None, discrete=True):
		self.score = None
		self.value = None
		self._amount      = amount
		self._compared_to = compared_to
		if amount and compared_to:
			self.compute(amount, compared_to, discrete)

	def compute(self, amount=None, compared_to=None, discrete=True):
		amount      = amount      or self._amount
		compared_to = compared_to or self._compared_to
		if discrete:
			return self.__compute_discrete_relevance(float(amount), float(compared_to))
		else:
			return self.__compute_continue_relevance(float(amount), float(compared_to))

	def __compute_discrete_relevance(self, amount, compared_to):
		ratio = amount/compared_to * 100
		if 90 <= ratio <= 110:
			return self.__set_values(10, "equivalent")
		else:
			if ratio < 100:
				if not ratio < 1:
					if 49 < ratio < 51:
						# near
						return self.__set_values(9, "half")
					else:
						if round(ratio) % 10 == 0:
							# multiple of 10
							return self.__set_values(8, "multiple")
			else:
				if ratio < 1000:
					if round(ratio) in (200, 500, 1000):
						# for instance: the query is twice the amount
						return self.__set_values(8, "multiple")
		return self.__set_values(0)

	def __compute_continue_relevance(self, amount, compared_to):
		raise Exception("To be implemented")

	def __set_values(self, score, value=None):
		self.score = score
		self.value = value

	def values(self):
		return (self.score, self.value)

# EOF
