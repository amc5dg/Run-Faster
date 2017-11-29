


# I am Faster: Using probabilistic programming to detect changes in runners' fitness levels

For this project, I decided to look at how long it takes the human body to adjust to running. I figured the simplest way to measure this was to look at people running on a track. A track is flat and 400 meters long and in addition the runner doesn't have to worry about traffic, trail conditions, or starting and stopping at stoplights, etc.

The data used for this project comes from Strava, "the social network for athletes". Because people have to take the time to register on Strava, it is reasonable to assume that these runners are interested in some level of fitness improvement rather than just fitness tracking. And since my aim is to determine when a runners' body has adapted to a higher level of running fitness, this makes an ideal place to find data. This project looks at the Kezar Stadium track in Golden Gate Park, San Francisco. This track was chosen because of the high density of Strava running usage (determined from Strava's heatmap) and since this is a professional sporting arena, the atmosphere might also give runners some extra 'oompf' to go a little faster (see the top picture). 

## Table of Contents
* [Motivation](#what-does-a-change-in-my-running-fitness-level-look-like)


## What does a change in my running fitness level look like?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/out%2Bof%2Bshape%2Bfunny.jpeg "Picture of Minion going to gym")

Since we are probably feeling a little different each time we go out for a run, it makes sense to think about our fitness level as a distribution. For example suppose you go out and run 5 laps on the track a few times a week. The first 10 sessions you might complete your laps in about 100 seconds each. But what about the next 10 sessions? The assumption is that the more laps you run (yes this is oversimplified), eventually your body will adapt and beome stronger. What this means is that the runner would see a shift in their distribution. 

## Building a Model     

In order to detect a change in our running fitness level, we want to see if the distributions shifts after some number of laps. This is a Bayesian MCMC switchpoint detection problem and was done using Python's probabilitic programming library pymc3.

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/pymc3.png "pymc3 logo")

Suppose a runner runs around the track 70 times and their lap times look like this:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/data_sim.png "sample data")

It looks like the runner's times got noticable quicker after ~40 laps. We will call this the switchpoint.

Using this, let's set up a model.

We have three parameters that we are interested in:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/CodeCogsEqn%20(2).gif "equation 1")

Since we are using a MCMC framework we first need to create a rule to generate a new value for each parameter.

Here we randomly generate where the switchpoint might occur using a discrete uniform distribution:



Here we specify the generator rule for the runner's split times. At first, we assume that the runner's lap times are normally distributed. However; since life happens when we are out running: suppose we see a friend stop to have a chat but forget we're on the clock, there is a high likelihood that outliers may occur. So the model uses a Student T distribution instead to account for this:



Next we set up our update rule. We have our observed data, previous paramteter values, and new values for the parameters. We want to calculate how likely is it that we observed our data given these new parameter estimates and the old estimates. If our observed data is more likely to have occured under the new parameter values, we update our guess of the parameter. Otherwise we keep the parameters unchanged. So for each step our model is given new estimates for 'switchpoint', 'early_mean', and 'late_mean' (captured in the 'rate' variable).


Here we set up the algorithm. The 'startvals' variable uses the MAP algorithm to choose an optimal starting point. The 'trace' variable is cumulative list of each update decison. Here we are making 10000 update decisions, 10 times (njobs = 10 argument). Each run of the algorithm is called a chain and multiple chains are run to assess model convergence and performance.



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

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/fastslowswitchpoint.png "fast vs slow switchpoints")
Here we see yet again that it doesn't matter how fast you are when you start running: it only takes about 40-70 laps for everyone to see a noticeable change in their fitness level.

### How big were those changes?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/howmuchfaster.png "Faster")
For those who saw a positive change in their fitness, we see that most runners were able to shave up to 40 seconds off. We see again that the improvement does not depend on whether you have run 100 or 200 laps. This is consistent with switchpoint graphs, in that you don't need to be runnin hundreds of laps to see a very noticaeable improvement.  

(Note: this is also only for those who saw a decrease in their mean lap times)

## Further Considerations

There are a few refinements that can be made to this project.  

The first point that needs to be addressed is people getting slower. There are a few possibilities for why this may be: the runner started running with someone else who was slower, the runner got hurt and is gradually coming back, or the season changed and the runner slowed down. All of these are possibilities for why some runners might have gotten slower and warrant further exploration.

The next important result that warrants discussion is data collection. As stated in the beginning, the data used for this project was an aggregation of all runners' data from a track in San Francisco. Ideally I would have liked to have used data from a track or running club going out for a workout or a race.

The last important piece to discuss is the model's oversimplification. There is so much more to building fitness than just going out a running laps. For example, this model does not take into account how much other running the runner is doing. Consider two runners who each run 10 laps on the track each week. However; runner A runs only 10 laps a week and runner B runs 4 miles twice a week. It would be interesting to run further analysis and separate runners according to these other fitness factors such as total mileage logged per week, initial fitness condition, etc 


