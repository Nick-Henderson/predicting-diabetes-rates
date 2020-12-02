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

We can see that diabetes rates vary over a large range, with some counties as low as ~4%, and others as high as ~18%, with the bulk of the counties falling between about 7-11%. Interestingly, we don't have symmetrical distribution - the peak is at about 8%, and there is a standard bell curve fall off to the right, but a much sharper drop to the left. That is, very few counties have less than ~7% diabetes. 

Lets take a look at the counties with the highest and lowest diabetes rates:

![](figs/diabetes_high_low_bar.png)

Interesting - it looks like southern and midwest counties make up the bulk of the top 15 counties, while western counties make up the bulk of the bottom 15. Let's see whether that pattern is maintained over the full dataset:

![](figs/diabetes_full_bar.png)

Again, we see more blue and now some green toward the left, indicating that western and northeastern counties have lower diabetes rates, while we see more red to the right, indicating that southern counties have higher diabetes rates.

## Feature selection for modeling



![](figs/diabetes_scatter.png)


