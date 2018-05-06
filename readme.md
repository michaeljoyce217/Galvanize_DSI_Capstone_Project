## Data Science Immersive Capstone Project - Property Crime Prediction by Neighborhood in Vancouver, BC, Canada
This project predicts spikes in crime rates by neighborhood in Vancouver, BC, Canada. The goal is to proactively reduce criminal activity through targeted police prevention and intervention tactics.



<br>


## Overview
<img align="left" src="resources/4279439952_76eae82b20_o.png" width="200"> Vancouver is routinely rated one of the world's most livable cities ([ref](https://biv.com/article/2017/08/vancouver-third-most-livable-city-world-economist)). However, the city has some of the highest illegal drug consumption rates in North America ([ref](https://en.wikipedia.org/wiki/Downtown_Eastside)).

<br>

<img align="right" src="resources/256px-VPD_and_perp.png" width="200">As a result, the crime rate is high by Canadian standards ([ref](https://globalnews.ca/news/4064656/bc-crime-justice-system-report/)). The objective of this predictive model is to aid planning departments in the allocation of resources, such as police and emergency services.

The Vancouver Police Department (VPD) ran a six-month pilot program in 2016 that attempted to predict property crimes by neighborhood. This led to a significant drop in property crime rates  ([ref](http://mediareleases.vpd.ca/2017/07/21/vancouver-police-adopt-new-technology-to-predict-property-crime/)) and has since been adopted as an ongoing police tactic. However, the VPD does not publish its methodology.



This capstone project will be submitted to the VPD upon completion, in an attempt to improve on the previous model. The property crime data published by the VPD will be considered along with data from addtional sources, including illegal drug prices, number of arrests for possession of heroin and cocaine, weather data, and economic data.

My interest in this project is derived from my love of my hometown. It is a wonderful city and beloved by many. However, it is scarred by its drug problem and the inherent property crimes that come with drug addiction. The area with the worst difficulties is locally known as the Downtown Eastside but the VPD refers to it as the Central Business District. ([ref](https://www.vice.com/en_ca/article/nev4p8/why-vancouver-has-always-been-an-addiction-ground-zero))

Many different approaches are being tried to attempt to alleviate this problem. ([ref](http://www.cbc.ca/radio/ondrugs/city-on-drugs-the-dark-pull-of-vancouver-s-downtown-eastside-1.4229455)) I am hoping that I can play a small part in these efforts.

Note that Vancouver has disadvantaged neighborhoods, but they are not racially homogeneous. Therefore, I am confident that this tool will not be used for racial profiling.

<br>




## Datasets

* The primary data is collected weekly from the Vancouver Police Department's crime database (491,459 property related crimes from 2003 to 2017). ([ref](http://data.vancouver.ca/datacatalogue/crime-data.htm))
* Climate data is collected daily from the (US) National Weather Service with Bellingham airport in Washington acting as a substitute for Vancouver weather. The two cities are 50 miles apart and have very similar climates. (This will be changed to Vancouver specific data in future.) ([ref](https://www.weather.gov/help-past-weather))
* Data pertaining to the number of arrests for possession of heroin and cocaine and economic data, such as unemployment rates, the consumer price index and gross national product, is taken from Statistics Canada. ([ref](http://www5.statcan.gc.ca/researchers-chercheurs/index.action?lang=eng&univ=7&search=&start=1&end=25&sort=0&themeId=0&date=&series=&author=&themeState=-1&dateState=-1&seriesState=-1&authorState=-1&showAll=false))  
* Data on the price of wholesale heroin given is taken from United Nations Office on Drugs and Crime.




INSERT GRAPHIC


The information that follows might be over-technical for some readers. The slideshow presentation is more accessible if that is preferred. (INSERT LINK)

<br>

## Methodology

Various feature engineering methods were applied to the data and each variation was tested as outline below. These involved various divisions of the neighborhoods and breaking the day into segments.

Two different day segmentations were considered in each model:
* 1200am-759am, 800am-359pm, 4pm-1159pm
* 1200am-1159am, 1200pm-1159pm

Neighborhoods were divided in two different ways due to differing crime rates and all models were trained on each subgroup individually:

* Division into low crime rate, medium crime rate, and high crime rate subgroups.
* Division into a subgroup containing only the  Central Business District and  another subgroup containing all other neighborhoods.

Day segments:
* 1200am-759am, 800am-359pm, 4pm-1159pm
* 1200am-1159am, 1200pm-1159pm

Many machine learning methods were applied to these various setups and the results were recorded.

Methods used to perform regression:

* Linear
* Lasso
* Logistic
* Elastic net
* Bayesian ridge  
* Random forest
* Adaptive boosting
* Bootstrap aggregating
* Stochastic gradient descent
* Gradient boosting
* Neural networks
* Extreme gradient boosting

The best results were obtained by using the 1200am-1159am, 1200pm-1159pm day segmentation and the dividing the neighborhoods into one subgroup containing only the  Central Business District and  another subgroup containing all other neighborhoods. Due to differing crime rates, separate models were trained on each subgroup of neighborhoods.

In terms of models, the best results were achieved using one of the Sci-kit Learn neural network model packages. However, this model was not chosen as it is a "black box" model. That is, determining the importance of certain data features is not clear given this model. Feature importance can be determined using variable subset selection but this is very expensive computationally.

The model using extreme gradient boosting came in a close second in all of the metrics used and has a measure of feature importance built in to the associated machine learning package. As a result, this is my model of choice for this project.



<br>

## Analysis of results

The models were evaluated using several metrics.
* R-squared (R2)- explains the percentage of variance in the target variable explained by the model
* Mean average error (MAE)- measurement of error of the model, less affected by outliers (large errors)
* Root Mean square error (RMSE)- measurement of error of the model, more affected by outliers (large errors)

The first train and test setup involved the usual test-train-split on all of the data. The results are given.

Central Business District
* R2 = 0.42949206337502333
* MAE = 3.07285251584
* RMSE = 3.93125075121

All other neighborhoods
* R2 = 0.30417653767054731
* MAE = 1.10146954427
* RMSE = 1.52630997545

The second train and test setup involved training the model on the data from 2003 to 2016 and using the data from 2017 as the test set.


Central Business District
* R2=0.31603303901865065
* MAE=3.58505860289
* RMSE=4.62383884462

All other neighborhoods
* R2 = 0.27866945771134088
* MAE = 1.05137735611
* RMSE = 1.44359975183

<br>

## Comparison to a less engineered dataset (THINKING OF PUTTING THE ACTUAL SCORES HERE IN THE APPENDIX)

In both setups, the results weren't striking outside the Central Business District but these are relatively low crime areas to begin with (2.43 property crimes per day segment on average). The results were far better in the high crime Central Business District (10.59 property crimes per day segment on average), which supports the validity of the model.

<br>

All of these setups were then further evaluated. This involved training the same models on the same setups but with a minimal dataset. This dataset consisted solely of the police data with some basic feature engineering.

* Day of week added only
* Same day segmentation as above
* Same neighborhood segmentation as above

The first train and test setup involved the usual test-train-split on all of the data. The results are given.

Central Business District
* R2 = 0.4404134166445236
* MAE = 3.00166645333
* RMSE = 3.84530425352                 

All other neighborhoods
* R2 = 0.29950300823917786
* MAE = 1.10348459841
* RMSE = 1.52476447252

The second train and test setup involved training the model on the data from 2003 to 2016 and using the data from 2017 as the test set.


Central Business District
* R2 = 0.33075163983589795
* MAE = 3.58069969465
* RMSE = 4.57381700885

All other neighborhoods
* R2=0.26924793183618834
* MAE=1.05867743692
* RMSE=1.45299682284

It was initially a shock to note that the metrics were very similar with or without the new data being considered. This might imply that the added data was unnecessary. However, the feature importance varied greatly between the models, particularly in the high crime Central Business District (see appendix). In the Central Business District, using the model with extra data, the initial VPD data features were not ranked very highly in importance relative to the features from the added data.

This implies that there may be significant predictive gains to be made with further investigation. Moreover, it seems like there is a better chance of further improvements with the extra datasets.



## Conclusions

* The model constructed was predictive in general but much more predictive in the Central Business District. As this is where most of the crime occurs, the model may have significant value to the Vancouver Police Department.

* This data should be examined using time series forecasting. This may provide further insight and hopefully increase the predictive power of the model.

* The Central Business District should be subdivided and examine further. This is possible as the VPD data gives street, hundred block, latitude and longitude data.

* Data should be added or refined to the model inputs (see improvements and extensions below)

<br>


## Delivery of predictions

The predictive model is demonstrated on a webpage that is updated daily. Users are able to click on any of Vancouver's 24 neighborhoods (shown on a map), and a predicted property crime rate will be given for that neighborhood for the next three days. In addition, a data table will be presented below the interactive map with the next 3 days of predicted property crime rates for all neighborhoods.

This model is updated daily as weather data proved to be predictive. The Vancouver Police Department publishes their crime report weekly on Sunday while most of the other data is updated monthly. This process is currently run locally but will eventually run through an EC2 instance on Amazon Web Services.
<br>




## Extensions and improvements

* Examine the predictive model using time series data analysis.

* Set up the EC2 instance to update automatically.

* The Central Business District has a uniquely high crime rate, hence has been considered separately in the predictive model. However, the Vancouver Police Department releases the hundred block and street, as well as the latitude and the longitude, of each incident. Build a separate predictive model for this neighborhood that predicts by city block. This is unlikely to be useful in the lower crime neighborhoods.

* The illegal drug possession data currently being used is annually for British Columbia (BC) as a whole. A request has been made to the BC government for monthly data specific to Vancouver.

* The price of wholesale heroin given is yearly and for Canada as a whole. Monthly and/or Vancouver specific data would be preferable. A request has been made to the United Nations Office on Drugs and Crime for this information.

* The weather data used is from the (US) National Weather Service for Bellingham airport in Washington. A web-scraping tool will be built to scrape equivalent data for Vancouver, Canada.


## Toolkit

* Jupyter Notebook - integrated development environment for python; used to explore data and test code
* Pandas - provides high-performance, easy-to-use data structures and data analysis tools for Python; used for basic data manipulation & some file reading
* NumPy - the fundamental package for scientific computing with Python; used for math functionality
* Sci-kit learn - data modeling library
* XGBoost - scalable machine learning system for boosting
* MongoDB - a NoSQL database; used for storing my scrapes
* Pymongo - a python wrapper for MongoDB
* Pickle - a python library for serializing objects; used for saving requests objects for later parsing
* Datetime - a python library for time related functions
* Matplotlib - math plotting library for python
* Seaborn - statistical data visualization library for python



<br>
