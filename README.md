# Flight-Delay-prediction-2015

In the year 2015, a delay was observed in most of the flights from the Airports in USA. Develop a model aimed at predicting flight delays at the Destination Airport. Create a Data set which can be used for visualization and model Building so as to predict the Delays of Flights. Find out which parameter is mainly responsible for the delay of flights.


## Dataset Overview

Three datasets were obtained from Kaggle which included the [flights](), [airlines]() and [airports]() dataset each of which having some useful parameters. These parameters were selected and merged into one single daatset which was finally used.


## Data Cleaning and Preprocessing
 1. First all the null values were dropped from all the three dataset
    ```bash
        airport = airport.dropna(subset = ['LATITUDE','LONGITUDE'])
    ```
    This was done for all the three datasets

2.  A function Format_Hourmin was written to format the time and the date was converted to Datetime format
    ```bash
        data2['Actual_Departure'] =data1['DEPARTURE_TIME'].apply(Format_Hourmin
    ```
    ```bash
        data2['Date'] = pd.to_datetime(data2[['YEAR','MONTH','DAY']])
    ```
3. Finally all the relevant columns from the three datasets were renamed and merged creating our final dataset
    ![finaldataset](https://drive.google.com/uc?export=view&id=1F3MUswquMTsJoI0LDMKdWJiDkmpRDK5P)
## Plots
Data visualization techniques were applied on the final dataset and some of them are given below

### Pie Chart
This pie chart shows the distribution flights per airline    
![piechart](https://drive.google.com/uc?export=view&id=1e_IwyVlvt2JaHCcPYAoYZ2ZgOIT6ZGbQ)  


### Strip plot 
This plot shows the arrival delay for each airline  
![strip plot](https://drive.google.com/uc?export=view&id=1pNbbfZsEPPTUeIyWRMD7T63nNYqh0PbW)  

### Heat Maps
Heat maps show the correlation between two vatiables this was plotted for all of the pairs
![Heatmap](https://drive.google.com/uc?export=view&id=19TbU8TOmDHJDGW-ZYj05-KAv2NjptKFB)  

## Conclusion
We observe that most of the Arrival Delays are dependent on the Departure Delays of the Airport from the Correlation Matrix. American Airlines had the highest Arrival Delay. We may also observe that even though maximum of the Arrival Delays are due to the Departure Delays but some flights has still arrived on time even after departed late from the Origin Airport. We are required to further inspect why departure Delay is happening in the origin Airport.

We can see that departure delay is the main problem which is creating Delay in the aviation industry. Departure Delays can be caused due Security Delay, Airline System Delays, Airlines Delay etc. The Delays affect the revenue of the company to a great extent so the delays have to be reduced as much as possible so as to increase the profitability in the Airline Industry. This can be achieved by considering the main reason for Departure Delay from the Origin Airport. Customer Satisfaction will also be greatly enhanced if the delays can be brought down as low as possible.


## Contributors

[Aruna Jayarajan](https://github.com/Aruna-Jayarajan)  
[Pritam Suttraway](https://github.com/PritamSS)


