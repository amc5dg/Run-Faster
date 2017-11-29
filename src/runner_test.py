import numpy as np
import matplotlib.pyplot as plt
import pymc3 as pm
from pymc3 import DiscreteUniform, Normal, Exponential, Poisson, traceplot, Uniform, StudentT
from pymc3.math import switch
import scipy.stats as scs
from pymc3.backends.base import merge_traces
from pymc3 import *
import matplotlib


data2early = scs.norm.rvs(loc=270,scale=10,size=40)
data2late = scs.norm.rvs(loc=220,scale=10,size=30)

data2 = np.append(data2early,data2late)
attempts = data2.shape[0]

fig = plt.figure(figsize=(12.5, 3.5))
ax = fig.add_subplot(111)
plt.bar(np.arange(0,attempts),data2,color="#348ABD")
plt.xlabel("Effort Number")
plt.ylabel("Elapsed Time")
plt.title("Runner Segment Completion Times")
plt.xlim(0,attempts)

rec_points_x = [35,35,45,45 ,35]
rec_points_y = [150,290,290,150,150]
plt.plot(rec_points_x,rec_points_y,c='red')


ax.quiver(49,290,-25,-10)

# runner_model = pm.Model()
# with runner_model:
#     switchpoint = DiscreteUniform('switchpoint',lower=0, upper=attempts)
#
#     early_mean = StudentT('early_mean',mu=250,sd=10,nu=5)
#     late_mean = StudentT('late_mean',mu=250,sd=10,nu=5)
#
#     rate = switch(switchpoint >= np.arange(attempts),early_mean,late_mean)
#
#     disasters = StudentT('disasters',mu=rate,sd=10,nu=5,observed=data2)
#
#     startvals = find_MAP(model=runner_model)
    # trace = pm.sample(10000,start=startvals,njobs=10)
# traceplot(trace,varnames=['early_mean','late_mean','switchpoint'])

plt.show()
