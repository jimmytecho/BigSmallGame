import numpy as np

class Game:
	def __init__(self, bankroll, limit) #limit should be odd
		self.bankroll = bankroll #bankroll is the total amount
		self.limit = limit		 #limit is the number of plays
		self.bank1 = self.bankroll
		self.bank2 = self.bankroll
		self.win1 = 0
		self.win2 = 0
		self.state = np.array([])

	def stage(self, bid1, bid2):
		if bid1 == bid2:
			#nothing happens
		else:
			self.bank1 -= bid1
			self.bank2 -= bid2
			if bid1 > bid2:
				self.win1 += 1
			else:
				self.win2 += 1
		self.state = [self.bank1, self.bank2, self.win1, self.win2, self.win1+self.win2]
		
		if self.win1+self.win2 == self.limit: self.reset()
		
		return self.state

	def reset(self)
		self.bank1 = self.bankroll
		self.bank2 = self.bankroll
		self.win1 = 0
		self.win2 = 0
		return [self.bank1, self.bank2, 0, 0, 0]
				
