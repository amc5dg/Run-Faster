![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/kezar.jpg "Picture of Kezar Stadium")


# AM I RUNNING FASTER?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/Usain-Bolt3.jpg "Running Really Fast") 

For this project, I decided to look at how long it takes the human body to adjust to running. I figured the simplest way to measure this was to look at people running on a track. A track is flat and 400 meters long and in addition the runner doesn't have to worry about traffic, trail conditions, or starting and stopping at stoplights, etc.

The data used for this project comes from Strava, "the social network for athletes". Because people have to take the time to register on Strava, it is reasonable to assume that these runners are interested in some level of fitness improvement rather than just fitness tracking. And since my aim is to determine when a runners' body has adapted to a higher level of running fitness, this makes an ideal place to find data. This project looks at the Kezar Stadium track in Golden Gate Park, San Francisco. This track was chosen because of the high density of Strava running usage (determined from Strava's heatmap) and since this is a professional sporting arena, the atmosphere might also give runners some extra 'oompf' to go a little faster (see the top picture). 

## What does a change in my 'running fitness level' look like?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/out%2Bof%2Bshape%2Bfunny.jpeg "Picture of Minion going to gym")

Since we are probably feeling a little different each tie we go out for a run, it makes sense to think about our fitness level as a distribution. For example suppose you go out and run 5 laps on the track a few times a week. The first 10 sessions you might complete your laps in about 100 seconds each. But what about the next 10 sessions? The assumption is that the more laps you run (yes this is oversimplified), eventually your body will adapt and beome stronger. What this means is that the runner would see a shift in their distribution. 

## Building a Model     

In order to detect a change in our running fitness level, we want to see if the distributions shifts after some number of laps. This is a Bayesian switchpoint detection problem and was done using Python's probabilitic programming library pymc3.

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/pymc3.png "pymc3 logo")

Suppose a runner runs around the track 70 times and their lap times look like this:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/data_sim.png "sample data")

It looks like the runners' times got noticable quicker after ~40 laps.

Using this runner, let's set up a model.

We have three parameters that we are interest in:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/CodeCogsEqn%20(2).gif "equation 1")

Since we are using a Bayesian framework we first need to assign a prior distribtion to each parameter.

Here we randomly assign where his/her switchpoint might occur using a discrete uniform distribution:

```python
with runner_model:
  switchpoint = DiscreteUniform('switchpoint',lower=0, upper=attempts)
```

Here we specify a distribution for his/her split times. Since the times they can run is mostly likely normally distributed . However; since life happens when we are out running (like seeing a friend out and about and stopping to have a chat but forgetting that you're on the clock), there is a high likelihood that outliers may occur. So we fit the model with a Student T distribution instead to account for this:

```python
with runner_model:  
  early_mean = StudentT('early_mean',mu=250,sd=10,nu=5)
  late_mean = StudentT('late_mean',mu=250,sd=10,nu=5)
```

Next we set up the distribution (called 'times') to sample from:

```python
with runner_model: 
  rate = switch(switchpoint >= np.arange(attempts),early_mean,late_mean)
  times = StudentT('times',mu=rate,sd=10,nu=5,observed=data)
```
And finally setting up the sampler. Note that we use MAP to set the initial locations of each chain.

```python
with runner_model:
  startvals = find_MAP(model=runner_model)
  trace = pm.sample(10000,start=startvals,njobs=10)
  ```

Let's see what it looks like:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/data_sim_tr.png "sample traceplot")

On the left are the distributions for each parameter (on the right are the values for each parameter for each iteration for each chain)

## Results

### The Runners

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/intro_plot.png "Introduction Graphs")
We see that most runners are running less than 200 laps. Because of this, the analysis focuses on the runners who have run less than 200 laps. 

These results are only for those runners where the model performed well. This means that the algorithm converged and had Gelman-Rubin scores of less than 1.7 for each parameter.

### How long does it take to see changes?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/switchpoints.png "Switchpoints")

#### What does the data show?
Looking at the graphs we see that a shift is most likely to occur between 35 and 60 laps for people who have run less than 100 laps and less than 200 laps. This is a very interesting result because it only takes about 45 laps whether you run 100 or 200 laps. This is a very pleasant result because it means that for someone starting to run laps, it won't take running hundreds of miles for him/her to see a noticeable change.

### How big were those changes?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/howmuchfaster.png "Faster")
For those who saw a positive change in their fitness, we see that most runners were able to shave up to 40 seconds off. We see again that the improvement does not depend on whether you have run 100 or 200 laps. This is consistent with switchpoint graphs, in that you don't need to be runnin hundreds of laps to see a very noticaeable improvement.  

(Note: this is also only for those who saw a decrease in their mean lap times)

## Further Considerations

There are a few refinements that can be made to this project. 
