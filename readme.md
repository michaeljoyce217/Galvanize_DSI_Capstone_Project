
## Data Science Immersive Capstone Project - Property Crime Prediction by Neighborhood in Vancouver, Canada
This project predicts spikes in crime rates by neighborhood in Vancouver, BC, Canada. The goal is to proactively reduce criminal activity through targeted police prevention and intervention tactics.



<br>


## Overview
<img align="left" src="resources/4279439952_76eae82b20_o.png" width="200"> Vancouver is routinely rated one of the world's most livable cities ([ref](https://biv.com/article/2017/08/vancouver-third-most-livable-city-world-economist)). However, the city has some of the highest illegal drug consumption rates in North America ([ref](https://en.wikipedia.org/wiki/Downtown_Eastside)).

<br>

<img align="right" src="resources/256px-VPD_and_perp.png" width="200">As a result, the crime rate is high by Canadian standards ([ref](https://globalnews.ca/news/4064656/bc-crime-justice-system-report/)). The objective of this predictive model is to aid planning departments in the allocation of resources, such as police and emergency services.

The Vancouver Police Department (VPD) ran a six-month pilot program in 2016 that attempted to predict property crimes by neighborhood. This led to a significant drop in property crime rates  ([ref](http://mediareleases.vpd.ca/2017/07/21/vancouver-police-adopt-new-technology-to-predict-property-crime/)) and has since been adopted as an ongoing police tactic. However, the VPD does not publish its methodology.



This capstone project will be submitted to the VPD upon completion, in an attempt to improve on the previous model. The property crime data published by the VPD will be considered along with data from addtional sources, including illegal drug prices, number of arrests for possession of heroin and cocaine, weather data, and economic data.

My interest in this project is derived from my love of my hometown. It is a wonderful city and beloved by many. However, it is scarred by its drug problem and the inherent property crimes that come with drug addiction. The area with the worst difficulties is colloquially called the Downtown Eastside but the VPD refers to it as the Central Business District. ([ref](https://www.vice.com/en_ca/article/nev4p8/why-vancouver-has-always-been-an-addiction-ground-zero))

Many different approaches are being tried to attempt to alleviate this problem. ([ref](http://www.cbc.ca/radio/ondrugs/city-on-drugs-the-dark-pull-of-vancouver-s-downtown-eastside-1.4229455)) I am hoping that I can play a small part in these efforts.

Note that Vancouver has disadvantaged neighborhoods, but they are not racially homogeneous. Therefore, I am confident that this tool will not be used for racial profiling.

<br>




## Datasets

* The primary data is collected weekly from the Vancouver Police Department's crime database (491,459 property related crimes from 2003 to 2017). ([ref](http://data.vancouver.ca/datacatalogue/crime-data.htm))
* Climate data is collected daily from the (US) National Weather Service with Bellingham airport in Washington acting as a substitute for Vancouver weather. The two cities are 50 miles apart and have very similar climates. (This will be changed to Vancouver specific data in future.) ([ref](https://www.weather.gov/help-past-weather)
* Data pertaining to the number of arrests for possession of heroin and cocaine and economic data, such as unemployment rates, the consumer price index and gross national product, is taken from Statistics Canada. ([ref](http://www5.statcan.gc.ca/researchers-chercheurs/index.action?lang=eng&univ=7&search=&start=1&end=25&sort=0&themeId=0&date=&series=&author=&themeState=-1&dateState=-1&seriesState=-1&authorState=-1&showAll=false)  
* Data on the price of wholesale heroin given is taken from United Nations Office on Drugs and Crime.




INSERT GRAPHIC


<br>

## Methodology

To be inserted

<br>

## Analysis of results

To be inserted

<br>



## Delivery of predictions

The predictive model will be demonstrated on a webpage that is updated daily. Users will be able to click on any of Vancouver's 24 neighborhoods (shown on a map of Vancouver), and a predicted property crime rate will be given for that neighborhood for the next three days. In addition, a data table will be presented below the interactive map with the next 7 days of predicted property crime rates for all neighborhoods.

This model will be updated daily as weather data proved to be predictive. The Vancouver Police Department publishes their crime report weekly on Sunday while most of the other data is updated monthly. This process will run through an EC2 instance on Amazon Web Services.


## Additional applications of this methodology

1) I especially want to study the correlation between crime and street drug prices. If the UN won't authorize the data use, web scraping could be slow.

2) The model might not be predictive of non-property crime, leading to a less impressive result.

3) If publicly available, the model could become a tool for criminals. Access might have to be restricted to government officials.

Note that Vancouver has disadvantaged neighborhoods, but they are not racially homogeneous. Therefore, I am confident that this tool will not be used for racial profiling.




## Extensions and improvements

* Examine the predictive model using time series data analysis.

* The Central Business District has a uniquely high crime rate, hence has been considered separately in the predictive model. However, the Vancouver Police Department releases the hundred block and street, as well as the latitude and the longitude, of each incident. Build a separate predictive model for this neighborhood that predicts by city block. This is unlikely to be useful in the lower crime neighborhoods.

* The illegal drug possession data currently being used is annually for British Columbia (BC) as a whole. A request has been made to the BC government for monthly data specific to Vancouver.

* The price of wholesale heroin given is yearly and for Canada as a whole. Monthly and/or Vancouver specific data would be preferable. A request has been made to the United Nations Office on Drugs and Crime for this information.

* The weather data used is from the (US) National Weather Service for Bellingham airport in Washington. A web-scraping tool will be built to scrape equivalent data for Vancouver, Canada.
