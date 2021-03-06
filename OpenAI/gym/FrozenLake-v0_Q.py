import gym
from gym import envs
import numpy as np
import sys

state_num = 4*4    # $B>uBV?t(B
action_num = 4      # $B9TF0?t(B
epiode_num = 10000  # $BI>2A$r9T$&%(%T%=!<%I?t(B
step = 1000
policySelect = 1    # 0: e-greedy$B<jK!(B 1: softmax$B<jK!(B
alpha = 0.7
gamma = 0.9
tau = 0.0016        # softmax$B<jK!$N29EY(B
goal = 0            # $B:G8e$N(B100$B2sCf%4!<%k$7$?2s?t(B
goal_total = 0

class Qlearning:
    """ class for Q Learning """
    @classmethod
    def choose_action(self, Q, new_state, epsilon):
        """ $B9TF07hDj(B """
        if policySelect == 0: # e-greedy
            if epsilon < np.random.uniform():
                # greedy$BK!$rE,MQ$9$k(B
                return np.argmax(Q[new_state,:])
            else:
                return np.random.randint(env.action_space.n)

        elif policySelect == 1: # softmax
            policy = np.exp(Q[new_state,:]/tau) / np.sum(np.exp(Q[new_state,:]/tau))
            
            # $B5U4X?tK!$G9TF0A*Br(B
            random = np.random.uniform()
            cprob = 0
            for a in range(action_num):
                cprob = cprob + policy[a]
                action = a
                if random < cprob:
                    break

            return action

    @classmethod
    def Qupdate(self, Q, new_state, state, action, reward):
        """ Q$BCM$N99?7(B """
        return (Q[state][action] + alpha*(reward-Q[state][action]+gamma*np.max(Q[new_state,:])))

if __name__=='__main__':
    Ql = Qlearning
    Q = np.zeros([state_num, action_num])
    epsilon = 0.4

    env = gym.make('FrozenLake-v0')

    for i_episode in range(epiode_num):
        state = env.reset()
        epsilon *= 0.999
        if epsilon < 1e-3:
            epsilon = 0.001
        print("Episode {}".format(i_episode+1))
        for t in range(step):
            #env.render()

            # $B9TF0(Ba$B$N3MF@(B
            # action = env.action_space.sample()
            action = Ql.choose_action(Q, state, epsilon)

            # $B<B9T(B
            new_state, reward, done, _ = env.step(action)

            # Q$B3X=,$N99?7(B
            Q[state][action] = Ql.Qupdate(Q, new_state, state, action, reward)

            if np.max(Q) < 0 and t > 100:
                print("ERROR: Q=0")
                sys.exit()

            # $B>uBV$H9TF0$N5-O?(B
            state = new_state

            if done:
                if new_state == state_num-1:
                    goal_total += 1
                    if i_episode > epiode_num-101:
                        goal += 1

                print("Episode finished after {} timesteps".format(t+1))
                break

    print("Q(s,a) =\n{}".format(Q))
    print("Goal total: {}".format(goal_total))
    print("{}/100".format(goal))
    print(epsilon)

    env.close()
