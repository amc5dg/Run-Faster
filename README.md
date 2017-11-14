# Run-Faster

We all know how great it feels when do we do something better than we did before. However, a one-time improvement, while in the moment is great, are you really any better...? This is a problem that I plan to tackle. What constitutes "being better"? One way to think about this is to think in terms of a distribution. Say for example I run my usual route in 40 min. On any given day I may be a little faster or I may be a little slower. So I have a baseline level of fitness that allows me to complete my run in 40 min with some degree of variation. 

But one day I wake up and decide that I'd like to run with my friends. I go run with them and we finish my usual route in 35 minutes, way faster than I normally do it. Okay so I set a new personal best, but is my average level any better after having killed myself to keep up with my friends? This means that when I go out and run my usual route, do I finish my route, on average, faster. In order to statistically show that I have run faster, I will need to show that my distribution has shifted.

Given this set-up, it makes sense to tackle this problem from a Basyesian standpoint, specifically switchpoint detection. What this means is that at time=0, I have a baseline fitness level distribution. And I want to know that if I run my route with my friends occasionally, when will my average fitness level change. The goal of this project is to use probabilistic programming to when I level up.

To find data for this project I will be using the Strava API. Strava is a fitness app that tracks your running, cycling, and swimming workouts. What makes this so appealing is that they have data grouped into what they call segments. Segments are standardized routes that anyone can access. 

Using the Strava heat map, which shows the distribution of Strava users, I will be able to find popular areas. Because I know where the popuar areas are, I will be able to find athletes that do this segment frequently and I will be able to track their progress. 

After finding athletes and determining their switchpoints, I will then "aggregate" (method TBD) their switchpoints to create an average profile for how long it takes for someone's baseline to actually change. 
