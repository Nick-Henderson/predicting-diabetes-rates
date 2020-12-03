# predicting-diabetes-rates

Diabetes affects over 30 million Americans (~10% of the population). Moreso than many diseases, diabetes is linked to lifestyle choices, diet, and exercise. These lifestyle factors, and thus diabetes rates, are likely related to socioeconomic status, geographic region, and other factors. To better understand the factors that influence diabetes rates, I will analyze data on diabetes rates, socioeconomic factors, and demographics accross all counties in the United States. I will attempt to fit a model that can predict diabetes rates for US counties. Such a tool, if it were sufficiently accurate, could be used to inform counties of the number of cases they should expect, which could be used to estimate healthcare costs, and might also provide some indication of whether diabetes is underdiagnosed in a particular county.  

### Data Sources

Intro statistics:
https://www.diabetes.org/resources/statistics/statistics-about-diabetes

Diabetes/obesity/physical activity rates: https://gis.cdc.gov/grasp/diabetes/DiabetesAtlas.html#

Socioeconomic data: https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html

Race/Demographics: https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/asrh/cc-est2019-alldata.csv

### Importing Data

After downloading, all datasets were cleaned and joined on state/county name in the python file import_data.py. See file for documentation on cleaning and joining datasets.

Final dataframe before feature selection: 

![](figs/df_ss.png)
This dataframe has 3141 rows (2 fewer than the total number of counties in the US due to missing data), and 273 columns/features. These features include many reduntant features from the socioeconomic dataset, and very granular racial demographics. Before doing any in depth EDA or modeling, I needed to select a subset of the columns. 

Feature selection/engineering was performed in the python file select_features.py

Exploratory data analysis, and early model testing was performed in the notebook Diabetes-feature-selection-and-EDA.ipynb

## Exploratory Data Analysis

First, lets look at the overall distribution of diabetes rates in US counties:

![](figs/diabetes_hist.png)

Mean: 8.7% 
Standard Deviation: 1.8%

We can see that diabetes rates vary over a large range, with some counties as low as ~4%, and others as high as ~18%, with the bulk of the counties falling between about 6-12%. Interestingly, we don't have symmetrical distribution - the peak is at about 7%, and there is a standard bell curve fall off to the right, but a much sharper drop to the left. That is, very few counties have less than ~7% diabetes. 

Lets take a look at the counties with the highest and lowest diabetes rates:

![](figs/diabetes_high_low_bar.png)

Interesting - it looks like southern and midwest counties make up the bulk of the top 15 counties, while western counties make up the bulk of the bottom 15. Let's see whether that pattern is maintained over the full dataset:

![](figs/diabetes_full_bar.png)

Again, we see more blue and now some purple toward the left, indicating that western and northeastern counties have lower diabetes rates, while we see more red to the right, indicating that southern counties have higher diabetes rates. Gray (midwestern) counties are sprinkled fairly uniformly throughout.

## Feature selection for modeling

Now let's explore our other features and how they relate to diagnosed diabetes percentage. As a first pass, we can plot all variables against diagnosed diabetes percentage: 

![](figs/diabetes_scatter.png)

From this plot, we can see some variables that are likely to be useful. Obesity percentage and physical inactivity percentage correlate fairly well with diabetes rates. To a lesser degree, we can see correlations for EP_POV (the percentage of people living in below the poverty line), EP_UNEMP (percentage unemployed), EP_NOHSDP (percentage with no high school diploma), and E_PCI (estimated per capita income, a negative correlation in this case).  

The fourth row of the plot (and the first plot of the 5th row) features various racial demographics. It is much less clear whether any of these will be useful in the regression. There does seem to be a very slight negative correlation with NHWA_PCT (non-hispanic white alone percent) and a slight positive correlation with NHBA_PCT (non-hispanic black alone percent), so these may be worth including. There is a fairly strong positive correlation with NHIA_PCT (non-hispanic american indian and alaskan native percent), however a fairly low number of counties have a high percentage.

In the bottom row, we see the same pattern from the bar graphs above. A negative correlation between diabetes percentage and a county being in the northeast or west, and a positive correlation between diabetes percentage and a county being in the south or midwest. 

We have some candidate variables to use and not use based on this analysis. Now lets start testing some models!

# Modeling Diabetes Rates

Our first step is to split the data into test and train sets. I did an 80:20 Train:Test split. From here on, until we have a final model, we will be working exlusively with the training set, and saving the final test set for the end. From this point on, when I refer to a training set, it will really be training set within this initial training set.

## Baseline Model

First, we will generate a "dumb" model to serve as a baseline to compare to our other models. Our dumb model will be to simply use the mean of our diabetes rates as an estimate.

### Mean of Training Set = 0.087 (8.7% diabetes)

## Baseline model error

We will use root mean squared error (RMSE) as our error metric. A function to calculate RMSE is in the python file error.py

![](figs/initial_error.png)

### Baseline error = 0.0177

Perhaps a more fair comparison is to use KFold cross validation even on this model. We will do so with a K of 6.

![](figs/kf_dumb_error.png)

### Real baseline error = 0.018

Because we are using RMSE, we can actually interpret this value. On average, our predicted values differ from our real values by about 0.018, or 1.8 percent (remember, we are predicting a percentage). This might not sound bad, but recall that most of our values fall within 1-2% of the mean: 

![](figs/diabetes_hist.png)

As a matter of fact, our RMSE for our dumb model is equivalent to our sample standard deviation (1.8%), as we should expect for a model that uses the mean.


## Simple Linear Regression

Let's build in complexity towards our final model. The next most basic approach is to use a simple linear regression. 