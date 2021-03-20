# Project 2 - NJ Movers Guide - Back Benchers

### Our Members
![Intro](ScreenShots/Intro.png)


# Our Goals
## Our goal is to create a guide that would educate potential movers on where to live in New Jersey based on certain criteria such geography, crime rate, education level, and tax rate.


### Our Process
![Flow](static/images/etl-flowchart.jpg)

### Our Challenges & ### Solutions

#### Our Data Sources

 1) https://www.state.nj.us/treasury/taxation/lpt/taxrate.shtml
 2) http://data.ci.newark.nj.us/dataset/new-jersey-counties-polygon/resource/95db8cad-3a8c-41a4-b8b1-4991990f07f3

Our biggest challenege from the Data sources was combining the all the different sets that would be useable for us. We had to convert the data, clean the data, synchronize key names such as country names, create a new jsn from Sqlitt, and merge multiple json and geojsons. 

#### D3 Page
Our D3 page is heavily influence by the D3 assignment. 
  1) The X-Axis is based on Poverty Rate, Average School Rank, House Hold Median Income
  2) The Y-Axis is based Crime Data which are Crime Rate per 100K, Total Offense, Total Arrest.
With this anyone can compare any of the X axis, and be measured against the data on the Y axis. The chart will plot the counties data based on which X and Y axis pair are activated.



####
