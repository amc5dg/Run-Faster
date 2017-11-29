import matplotlib.pyplot as plt
import pickle as pickle
from pymc3 import *
from pymc3.math import switch
import numpy as np

class IsRunnerBetter(object):

    def __init__(self,efforts):
        self.switchpoint = None
        self.lvl1 = None
        self.lvl2 = None
        self.lvl = None
        self.my_runs = None
        self.efforts = np.array(efforts)
        self.num_efforts = self.efforts.shape[0]
        self.mu = np.mean(self.efforts)
        self.sd = np.std(self.efforts)
        self.nu = 15

    def is_runner_better(self):
        runner_model = Model()
        with runner_model:
            self.switchpoint = DiscreteUniform('switchpoint',lower=0,upper=self.num_efforts)

            self.lvl1 = StudentT('lvl1',mu=95,lam=10**-2,nu=5)

            self.lvl2 = StudentT('lvl2',mu=95,lam=10**-2,nu=5)

            self.lvl = switch(self.switchpoint >= np.arange(self.num_efforts),self.lvl1,self.lvl2)

            self.my_runs = StudentT('runs',mu = self.lvl,lam=15**-2,nu=5,observed=self.efforts)

            startvals = find_MAP(model=runner_model)

            self.trace = sample(10000,start=startvals,njobs=5)

    def plot_runner(self):
        plt.figure(figsize=(12.5, 3.5))
        plt.bar(np.arange(0,self.num_efforts),self.efforts,color="#348ABD")
        plt.xlabel("Effort Number")
        plt.ylabel("Elapsed Time")
        plt.title("Runner Segment Completion Times")
        plt.xlim(0,self.num_efforts)


    def plot_model(self):
        traceplot(self.trace,varnames=['lvl1','lvl2','switchpoint'])

    def model_diagnostics(self):
        print(gelman_rubin(self.trace))
        print(effective_n(self.trace))

if __name__ == '__main__':

    with open("a2.pkl", "rb") as fp:
        a_list = pickle.load(fp)
    with open("t2.pkl", "rb") as fp:
        t_list = pickle.load(fp)
    with open("d.pkl", "rb") as fp:
        d_list = pickle.load(fp)

    runners = { k:v for k,v in a_list[1].items() if v > 50}
    their_times = { k:v for k,v in t_list[1].items() if k in runners.keys()}
    their_training_period = {k:v for k,v in d_list[1].items() if k in runners.keys()}

    good_runners = []
    traces = []
    switchpoint_means = []
    lvl1_means = []
    lvl2_means = []

    for k,v in their_times.items():
        run_faster = IsRunnerBetter(v)
        run_faster.plot_runner()
        run_faster.is_runner_better()
        print(summary(run_faster.trace))
        run_faster.model_diagnostics()
        if gelman_rubin(run_faster.trace)['switchpoint'] <= 1.5 and gelman_rubin(run_faster.trace)['lvl1'] <= 1.5:
            good_runners.append(k)
            run_faster.plot_model()
            traces.append(run_faster.trace)
            switchpoint_means.append(np.mean(run_faster.trace[2500:9000]['switchpoint']))
            lvl1_means.append(np.mean(run_faster.trace[2500:9000]['lvl1']))
            lvl2_means.append(np.mean(run_faster.trace[2500:9000]['lvl2']))

    plt.show()
