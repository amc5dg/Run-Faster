![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/kezar.jpg "Picture of Kezar Stadium")


# AM I RUNNING FASTER?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/Usain-Bolt3.jpg "Running Really Fast")


For those of us who want to increase our running fitness level, running on the track is a classic. A track is rubberized, flat, and comes in very specific sizes ie 400 meters. For my project I looked at runners' data from a 400 meter track to see how people's running fitness levels change over time. This project looks at whether having access to a 400 meter track in Kezar Stadium, San Francisco produces changes in a runners' fitness level.  

## What does a change in my 'running fitness level' look like?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/out%2Bof%2Bshape%2Bfunny.jpeg "Picture of Minion going to gym")

The easiest way to think about this is to look at a distribution of your times. For example suppose you go out and run 6 laps on the track a few times a week. The first 50 laps you might complete your laps in 100 seconds each. But what about the next 100 laps? As you run more laps, your body adapts and gets more efficients, and then boom you're running those next 100 laps 10 seconds faster.

## How can we determine if we've improved?     

In order to detect a change in our running fitness level, we want to see if the distributions of my split times change after some number of laps. This was done using probabilistic prgramming in Python's pymc3 library.

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/pymc3.png "pymc3 logo")

To give a visual example of what a change in someone's fitness would look like consider the following plot of their lap times:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/data_sim.png "sample data")

As we can see, it looks like there might be a point where his/her completion times have dropped to a lower sustained level. But this is just what are eyes are telling us. We can use an MCMC algorithm to 'prove' that this person is in fact better.

Let's set up our model.

We have three parameters parameters that we are interest in finding the distributions of:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/CodeCogsEqn%20(2).gif "equation 1")

Here we randomly assign where his/her leveling up might occur:

```python
with runner_model:
  switchpoint = DiscreteUniform('switchpoint',lower=0, upper=attempts)
```

Here we specify a distribution for his/her split times. Since the times they can run is mostly likely normally distributed [add caveats an further details about this here ex) 'this may be overly simplistic']. However; since life happens when we are out running (like seeing a friend out and about and stopping to have a chat but forgetting that you're on the clock), there is a highlikelihood that outliers may occur. So we fit the model with a Student T distribution instead to account for this:

```python
with runner_model:  
  early_mean = StudentT('early_mean',mu=250,sd=10,nu=5)
  late_mean = StudentT('late_mean',mu=250,sd=10,nu=5)
```

Next we set up the distribution (called 'times') of our runner for the MCMC to sample from:

```python
with runner_model: 
  rate = switch(switchpoint >= np.arange(attempts),early_mean,late_mean)
  times = StudentT('times',mu=rate,sd=10,nu=5,observed=data)
```
And finally setting up the sampler. Note that we use MAP to set the initial locations of each chain

```python
with runner_model:
  startvals = find_MAP(model=runner_model)
  trace = pm.sample(10000,start=startvals,njobs=10)
  ```

Let's see what it looks like:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/data_sim_tr.png "sample traceplot")

Let's break down what we're looking at. At the upper left we see the distribution for his/her laps before they leveled up. And right below that plot we see the distribution of their level 2 times. And then below that we see the distribution of the when the switch occured. (To see a more technical breakdown see the <filename> file)  

## Results

### The Runners

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/intro_plot.png "Introduction Graphs")
We see that most runners are running less than 200 laps. I would say this makes sense as running on a track, when you're inside Gold Gate Park and have so much access to much more 'simulating' routes. Because of this, the analysis focuses on the runners who have run less than 200 laps.  

### How long does it take to see changes?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/switchpoints.png "Switchpoints")

#### What does the data show?
Looking at the graphs we see that the switchpoint is most likely to occur between 35 and 60 laps for people who have run less than 100 laps and less than 200 laps. This is a very important result in that for anyone running less than 200 laps, it only takes about 45 laps for someone's fitness level to change(see further considerations). This is a very pleasant result because it means that for someone starting to run laps, it won't take running hundreds of miles for him/her to see a noticeable change.

### How big were those changes?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/howmuchfaster.png "Faster")
For those who saw a positive change in their fitness, we see that most runners were able to shave uo to 40 seconds off of thier mean lap times in only 35-60 laps (see further considerations). Note: this is also only for those who saw a decrease in their mean lap times

## Further Considerations

