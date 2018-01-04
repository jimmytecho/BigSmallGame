# -*- coding: utf-8 -*-
import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import h5py
import BSG


class Agent:
	def __init__(self, state_size, action_size):
		self.state_size = state_size
		self.action_size = action_size
		self.memory = deque(maxlen = 200)
		self.gamma = 0.95
		self.tau = 10.0
		self.tau_min = 0.1
		self.tau_decay = 0.995
		self.learning_rate = 0.001
		self.model = self._build_model()
	
	def _build_model(self):
		#The Neural Net Model
		model = Sequential()
		model.add(Dense(64, input_dim = self.state_size, activation = 'tanh'))
		model.add(Dense(64, activation = 'tanh'))
		model.add(Dense(self.action_size, activation = 'tanh'))
		model.compile(loss='mse', optimizer = Adam(lr=self.learning_rate))
		return model

	def save(self, name):
		self.model.save_weights(name)

	def act(self, state):
		act_values = self.model.predict(state)
		nom = np.exp(act_values/self.tau)
		denom = np.sum(np.exp(act_values/self.tau))
		prob = nom/denom
		return np.random.choice(range(self.action_size), p = prob[0])

	def remember(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))
	# bank1 bank2 win1 win2 round	

	def replay(self, batch_size):
		minibatch = random.sample(self.memory, batch_size)
		for state, action, reward, next_state, done in minibatch:
			target = reward
			if not done:
				target = (reward+self.gamma*np.amax(self.model.predict(next_state)[0]))
			target_f = self.model.predict(state)
			onset = state[0][0]
			target_f[0][onset+1:] = -1
			if reward == 1:
				target_f[0][:onset-1] = 0
			target_f[0][action] = target
			self.model.fit(state, target_f, epochs=1, verbose=0)
		if self.tau > self.tau_min:
			self.tau = self.tau_min

	def load(self, name):
		self.model.load_weights(name)
		self.tau = self.tau_min

	def callpredict(self, state):
		return self.model.predict(state)
	def callp(self, state):
		act_values = self.model.predict(state)
		nom = np.exp(act_values/self.tau)
		denom = np.sum(np.exp(act_values/self.tau))
		probability = nom/denom
		return probability

#if __name__ == "__main__"

### main function starts here###

import BSG

bankroll = 100
limit = 5

EPS = 500 #Episodes

unv = BSG.Game(bankroll,limit)
state_size = 5
action_size = bankroll + 1
agent = Agent(state_size, action_size)
batch_size = 32
try: 
	agent.load("./save/BSG-dqn2.h5")
except:
	pass
for e in range(EPS):
	A = unv.reset()
	B = unv.reset()
	A = np.reshape(A, [1, state_size])
	B = np.reshape(B, [1, state_size])
	done = 0
	while 1:
		bank1, bank2, win1, win2, stage = A[0]
		B = np.array([[bank2, bank1, win2, win1, stage]])
		act1 = agent.act(A)
		act2 = agent.act(B)
		result = unv.play(act1, act2) #a BSG state
		bank1, bank2, win1, win2, stage = result
		
		reward1, reward2 = 0,0
		if win1 == win2+1: reward1, reward2 = 0.1,-0.1		
		if win1 == win2+2: reward1, reward2 = 0.5,-0.5
		if win1 == win2-1: reward1, reward2 = -0.1,0.1
		if win1 == win2-2: reward1, reward2 = -0.5,0.5
		if stage == limit:
			if win1>win2: reward1 = 1
			elif win2>win1: reward2 = 1
			done = 1
		if bank1 < 0:
			reward1 = -1
			done = 1
		if bank2 < 0:
			reward2 = -1
			done = 1
		print result
	
		T = result
		result_B = [T[1],T[0],T[3],T[2],T[4]]
		result = np.reshape(result, [1,5])
		result_B = np.reshape(result_B, [1,5])

		agent.remember(A, act1, reward1, result, done)
		agent.remember(B, act2, reward2, result_B, done)
		A = result
		B = result_B
		if done:
			print("episode: {}/{}, stage: {}, tau: {:.2}".format(e, EPS, stage, agent.tau))
			unv.reset()
			break
		if len(agent.memory) > batch_size:
			agent.replay(batch_size)
		
	if e % 100 == 0:
		agent.save("./save/BSG-dqn2.h5")



		



