# Electrical Load Forecasting using Machine Learning

## Table of Contents
* [Demo](#demo)
* [What is Electrical Load Forecasting](#what-is-electrical-load-forecasting)
* [Overview](#overview)
* [Motivation](#motivation)

## Demo
Link : [Electrical Load Forecasting Heroku App](https://load-prediction-v-1-5-0.herokuapp.com/)

<a href="https://imgur.com/ukQq06u"><img src="https://i.imgur.com/ukQq06u.png" title="source: imgur.com" /></a>

## What is Electrical Load Forecasting
We will start with a short explanation of what Load Forecasting is : 
-	Electrical load forecasting is the estimation of future load by an industry or a utility company. 
-	The estimation of both demand and requirements is crucial for an effective energy planning. 
-	Load forecasting are even used for determining the generation capacity, transmission and distribution systems etc.


## Overview
This is a Machine Learning model which aims to solve a Time-Series problem using __FBprophet__. The model takes input such as Temperature, Day and will print the output in the form of a table with a load chart which I created using `Chart.js`. The model is trained on `Energy Dataset.csv` which has 35,000 records over a period of 3 years i.e. 2015-2018. 

## Motivation
I am a final year Electrical Engineering student and this is my final year project.
There are some problems which are faced by modern electrical industry :
-	Intermittent Power
-	Power surges and spikes
-	Sags, dips and outrages
-	Overloaded circuits

Many of these problems can be reduced to some extend if proper load forecasting is done.

I am sure many people would have experienced atleast one of the above problem. Inconsistent power distribution is not good for the reputation of the generating company and since all our everyday appliances run on electricity, thus causing inconvenience. 

Being from Electrical domain and having Machine Learning knowledge, I have attempted to solve a real world problem which will benefit the society. 

## Technical Aspect

