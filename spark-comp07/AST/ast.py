class AST(object):
	def __init__(self, type):
		self.type = type
		self._kids = []

	#
	#  Not all these may be needed, depending on which classes you use:
	#
	#  __getitem__		GenericASTTraversal, GenericASTMatcher
	#  __len__		GenericASTBuilder
	#  __setslice__		GenericASTBuilder
	#  __cmp__		GenericASTMatcher
	#
	def __getitem__(self, i):
		return self._kids[i]
	def __len__(self):
		return len(self._kids)
	def __setslice__(self, low, high, seq):
		self._kids[low:high] = seq
	def __cmp__(self, o):
		return cmp(self.type, o)
