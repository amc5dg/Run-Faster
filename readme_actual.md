
## Let's Go Run:
### Using probabilistic programming to detect changes in runners' fitness levels

This project looks at how long it takes the human body to adjust to running. 

### Table of Contents
* [Motivation](#motivation)
* [Data](#data)
* [Methodology](#building-the-model)
* [Results](#results)
* [Further Considerations](#further-considerations)
* [Acknowledgements](#acknowledgements)

### Motivation

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/out%2Bof%2Bshape%2Bfunny.jpeg "Picture of Minion going to gym")

Since we are probably feeling a little different each time we go out for a run, it makes sense to think about our fitness level as a distribution. For example suppose you go out and run 5 laps on the track a few times a week. The first 10 sessions you might complete your laps in about 100 seconds each. But what about the next 10 sessions? The assumption is that the more laps you run (yes this is oversimplified), eventually your body will adapt and beome stronger. What this means is that the runner would see a shift in their distribution.

### Data
The data used for this project comes from Strava, "the social network for athletes". Strava is a fitness tracking app that tracks an athletes running, cycling, swimming, and nordic skiing sessions in a way that promotes friendly competition by recording an athlete's times on popular segments. Because people have to take the time to register on Strava, it is reasonable to assume that these runners are interested in some level of fitness improvement rather than just fitness tracking. 

I figured the simplest way to measure this was to look at people running on a track. A track is flat, only a quarter mile long, and the runner doesn't have to worry about traffic, trail conditions, or starting and stopping at stoplights, etc.
This project looks at the Kezar Stadium track in Golden Gate Park, San Francisco. This track was chosen because of the high density of Strava running usage (determined from Strava's heatmap) and since this is a professional sporting arena, the atmosphere might also give runners some extra 'oompf' to go a little faster (see the below).

![asdf](https://github.com/amc5dg/Run-Faster/blob/master/images/kezarstadium-small.jpg "Kezar Stadium Track")

### Building the Model     

In order to detect a change in our running fitness level, we want to see if the distributions shifts after some number of laps. This is a Bayesian MCMC switchpoint detection problem and was done using Python's probabilitic programming library pymc3.

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/pymc3.png "pymc3 logo")

Suppose a runner runs around the track 70 times and their lap times look like this:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/data_sim.png "sample data")

It looks like the runner's times got noticable quicker after ~40 laps. We will call this the switchpoint.

Using this, let's set up a model.

We have three parameters that we are interested in:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/CodeCogsEqn%20(2).gif "equation 1")

Since we are using a MCMC framework we first need to create a rule to generate a new value for each parameter. First we generate a random time for the switchpoint to take place using a discrete uniform distribution. Next we generate values for the pre-switchpoint mean and post-switchpoint mean

Here we randomly generate where the switchpoint might occur using a discrete uniform distribution:



Here we specify the generator rule for the runner's split times. At first, we assume that the runner's lap times are normally distributed. However; since life happens when we are out running: suppose we see a friend stop to have a chat but forget we're on the clock, there is a high likelihood that outliers may occur. So the model uses a Student T distribution instead to account for this:



Next we set up our update rule. We have our observed data, previous paramteter values, and new values for the parameters. We want to calculate how likely is it that we observed our data given these new parameter estimates and the old estimates. If our observed data is more likely to have occured under the new parameter values, we update our guess of the parameter. Otherwise we keep the parameters unchanged. So for each step our model is given new estimates for 'switchpoint', 'early_mean', and 'late_mean' (captured in the 'rate' variable).


Here we set up the algorithm. The 'startvals' variable uses the MAP algorithm to choose an optimal starting point. The 'trace' variable is cumulative list of each update decison. Here we are making 10000 update decisions, 10 times (njobs = 10 argument). Each run of the algorithm is called a chain and multiple chains are run to assess model convergence and performance.



Let's see what it looks like:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/data_sim_tr.png "sample traceplot")

On the left are the distributions for each parameter (on the right are the values for each parameter for each iteration for each chain)

### Results

#### The Runners

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/intro_plot.png "Introduction Graphs")
We see that most runners are running less than 200 laps. Because of this, the analysis focuses on the runners who have run less than 200 laps. 

### How long does it take to see changes?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/switchpoints.png "Switchpoints")

#### What does the data show?
Looking at the graphs we see that a shift is most likely to occur between 35 and 60 laps for people who have run less than 100 laps AND 100-200 laps. This is a very interesting result because it only takes about 45 laps whether you run 100 or 200 laps. This is a very pleasant result because it means that for someone starting to run laps, it won't take running hundreds of miles for him/her to see a noticeable change.

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/fastslowswitchpoint.png "fast vs slow switchpoints")
Here we see yet again that it doesn't matter how fast you are when you start running: it only takes about 40-70 laps for everyone to see a noticeable change in their fitness level.

### Further Considerations

There are a few refinements that can be made to this project.  

The first point that needs to be addressed is people getting slower. There are a few possibilities for why this may be: the runner started running with someone else who was slower, the runner got hurt and is gradually coming back, or the season changed and the runner slowed down. All of these are possibilities for why some runners might have gotten slower and warrant further exploration.

The next important result that warrants discussion is data collection. As stated in the beginning, the data used for this project was an aggregation of all runners' data from a track in San Francisco. Ideally I would have liked to have used data from a track or running club going out for a workout or a race.

The last important piece to discuss is the model's oversimplification. There is so much more to building fitness than just going out a running laps. For example, this model does not take into account how much other running the runner is doing. Consider two runners who each run 10 laps on the track each week. However; runner A runs only 10 laps a week and runner B runs 4 miles twice a week. It would be interesting to run further analysis and separate runners according to these other fitness factors such as total mileage logged per week, initial fitness condition, etc 


### Acknowledgements

First I want to say a huge thank-you to my instructors and fellow classmates at Galvanize.

References that made my project possible:

The code to get my data from the Strava API borrows heavily from [Ultramann's Github project Stravaboards](https://github.com/Ultramann/Stravaboards/blob/master/data_collection/segments_to_db.py)

[Bayesian Methods for Hackers](https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers)

[The Metropolis-Hastings Algorithm](https://arxiv.org/pdf/1504.01896.pdf)

LaTeX equation was made using CodeCogs





