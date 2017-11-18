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

    # def set_switchpoint(self,dist=DiscreteUniform):
    #     self.switchpoint = dist('switchpoint',lower=0,upper=self.num_efforts)

    # def set_lvl1(self,dist=StudentT,nu=15):
    #     self.lvl1 = dist('lvl1',self.mu,self.sd,nu)
    #
    # def set_lvl2(self,dist=StudentT,nu=15):
    #     self.lvl2 = dist('lvl2',self.mu,self.sd,nu)
    #
    # def set_my_runs(self,dist=StudentT,sd=10):
    #     self.my_runs = dist('runs',mu=self.lvl,sd=sd,observed=self.efforts)

    def is_runner_better(self):
        runner_model = Model()
        with runner_model:
            self.switchpoint = DiscreteUniform('switchpoint',lower=0,upper=self.num_efforts)

            self.lvl1 = StudentT('lvl1',self.mu,self.sd,self.nu)

            self.lvl2 = StudentT('lvl2',self.mu,self.sd,self.nu)

            self.lvl = switch(self.switchpoint >= np.arange(self.num_efforts),self.lvl1,self.lvl2)

            self.my_runs = StudentT('runs',mu = self.lvl,nu=10,observed=self.efforts)

            startvals = find_MAP(model=runner_model)

            self.trace = sample(100000,start=startvals,njobs=10)

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
        gelman_rubin(self.trace)
        effective_n(self.trace)

if __name__ == '__main__':

    with open("a.pkl", "rb") as fp:
        a_list = pickle.load(fp)
    with open("t.pkl", "rb") as fp:
        t_list = pickle.load(fp)
    with open("d.pkl", "rb") as fp:
        d_list = pickle.load(fp)

    runners = { k:v for k,v in a_list[0].items() if v > 100}
    their_times = { k:v for k,v in t_list[0].items() if k in runners.keys() and np.mean(v) > 500}

    for k,v in their_times.items():
        run_faster = IsRunnerBetter(v)
        run_faster.plot_runner()
        run_faster.is_runner_better()
        run_faster.plot_model()
    plt.show()
