
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

"Too much, too soon"

As a life-long runner, I have had many injuries all owing to doing "too much, too soon". So for my project I did a Bayesian switchpont analysis to determine when a runner's fitness distribution shifts. As much to prove to myself that indeed, "patience is a virtue". 

### Data
The data used for this project comes from Strava, "the social network for athletes". Strava is a fitness tracking app that tracks an athletes running, cycling, swimming, and nordic skiing sessions in a way that promotes friendly competition by recording an athlete's times on popular segments. Because people have to take the time to register on Strava, it is reasonable to assume that these runners are interested in some level of fitness improvement rather than just fitness tracking. 

I figured the simplest way to measure this was to look at people running on a track. A track is flat, only a quarter mile long, and the runner doesn't have to worry about traffic, trail conditions, or starting and stopping at stoplights, etc.
This project looks at the Kezar Stadium track in Golden Gate Park, San Francisco. This track was chosen because of the high density of Strava running usage (from looking at Strava's heatmap) and since this is a professional sporting arena, the atmosphere might also give runners some extra 'oompf' to go a little faster (see the below).

The data was webscraped from Strava's public API. While much of a runner's information is private, Strava has designated certain routes as segments and segment data is open to the public. Which means that I was able to extract every effort by every runner on any segment. This was ideal because it gave me a large and varied dataset to look at.
I was able to scrape the running efforts of ~4500 runners running about half a million laps. 

![asdf](https://github.com/amc5dg/Run-Faster/blob/master/images/kezarstadium-small.jpg "Kezar Stadium Track")

### Building the Model     

In order to detect a change in our running fitness level, we want to see if the distributions shifts after some number of laps. This is a Bayesian MCMC switchpoint detection problem and was done using Python's probabilitic programming library pymc3.

Suppose a runner runs around the track 70 times and their lap times look like this:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/data_sim.png "sample data")

It looks like the runner's times got noticable quicker after ~40 laps. We will call this the switchpoint.

Because I am using probabilistic programming, I can build a custom model to detect switchpoints given any parameterization. There were 3 parameters that were of interest to this problem:

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/CodeCogsEqn%20(2).gif "equation 1")

(The code used to produce this graph can be found [here](https://github.com/amc5dg/Run-Faster/blob/master/src/runner_test.py))


Because lap times are most likely normally distributed, a normal prior for early_mean and late_mean was initially used. However; after looking at the noisiness of the data and poor model performance, a T distribution was assigned to give the model more flexibility. Since the switchpoint could happen after any number of laps, a discrete uniform was used as the prior for the switchoint distribution. 

The model uses the MAP algorithm to choose optimal starting points to improve model performance. After the traces were compiled for each runner, the means of each parameter were collected for summarization. The first 2500 iterations were discarded as a burn-in period. The last 1000 iterations were also discarded. So the means were only calculated on iterations 2500-9000.  

The main point of this project is to figure out how long it takes a runner to reach the switchpoint (it is important to note that these runners are not going out and running all of their laps in a row; but rather incorporating the track into their running routine). In order to figure out how long the adaptation process took, I looked at how many days passed until they ran the 'switchpoint' amount of laps. Since Strava provides dates along with every effort, I just needed to look at how many days had passed since their first lap and the 'switchpoint' number of laps. Instead of looking at each runner's 'switchpoint' number of laps, I used the overall 'switchpoint' number of laps and built a histogram for the number of days that passed until each runner had ran that many laps. I did this because I wanted to see the general trend across runners.  

Some filtering of runners was done. First, any runner who ran less than 50 laps was not considered because I wanted to make sure that the runner ran often and consistently. Secondly, only runners who had nice convergence of the algorithm were included using only those runners who had Gelman-Rubin scores of less than 1.5 for each parameter. Thirdly, only runners who saw a positive improvement in their times were used.  


### Results

### How long does it take to see changes? How BIG are those changes?

![alt text](https://github.com/amc5dg/Run-Faster/blob/master/images/switchpoints.png "Switchpoints")

(Most runners were running less than 200 laps. Because of this, the analysis focused on runners who had run less than 200 laps)

![](https://github.com/amc5dg/Run-Faster/blob/master/images/duration_improvement.png "results")

(Plots were made using a jupyter notebook found [here](https://github.com/amc5dg/Run-Faster/blob/master/src/plotting.ipynb). And the code that was used for analysis can be found [here](https://github.com/amc5dg/Run-Faster/blob/master/src/building_model.py))

### Further Considerations

There are a few refinements that can be made to this project.  

The first thing would be to build in switchpoint sensitivity to the model. Since I am using a Bayesian framework for detecting switchpoints, I would like to build in a threshold for determining whether or not a switchpoint exists. In my model, I assume there is a switchpoint and am calculating when it is most likely to have occured. I would do this by caluclating 95% confidence intervals on the posterior early_mean and late_mean distributions and if there more than some threshold amount of overlap, I would conclude that there was no switchpoint for that runner. 

The second point that needs to be addressed is people getting slower. There are a few possibilities for why this may be: the runner started running with someone else who was slower, the runner got hurt and is gradually coming back, or the season changed and the runner slowed down. All of these are possibilities for why some runners might have gotten slower and warrant further exploration.

The next important result that warrants discussion is data collection. As stated in the beginning, the data used for this project was an aggregation of all runners' data from a track in San Francisco. Ideally I would have liked to have used data from a track or running club going out for a workout or a race.

The last important piece to discuss is the model's oversimplification. There is so much more to building fitness than just going out a running laps. For example, this model does not take into account how much other running the runner is doing. Consider two runners who each run 10 laps on the track each week. However; runner A runs only 10 laps a week and runner B runs 4 miles twice a week. It would be interesting to run further analysis and separate runners according to these other fitness factors such as total mileage logged per week, initial fitness condition, etc 


### Acknowledgements

First I want to say a huge thank-you to my instructors and fellow classmates at Galvanize.

References that made my project possible:

* The code to get my data from the Strava API borrows heavily from [Ultramann's Github project Stravaboards](https://github.com/Ultramann/Stravaboards/blob/master/data_collection/segments_to_db.py)

* [Bayesian Methods for Hackers](https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers)

* [The Metropolis-Hastings Algorithm](https://arxiv.org/pdf/1504.01896.pdf)

LaTeX equation was made using CodeCogs

A huge thanks goes out to Strava having their data open to the public; without which, this project would not have happened.





