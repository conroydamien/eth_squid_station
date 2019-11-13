![alt text](https://github.com/dmintercept/eth_squid_station/blob/master/assets/squid-logo-1.png)

# Squid Station 
### Gas Forcasting with Machine Learning

http://www.squidstation.com:8050/

## Inspiration

Gas adds up--especially for large transactions!  We were tired of waiting for longer-than-predicted transaction times and overpaying for gas based on incorrect predictions.

## What it does

The program uses machine learning models to predict the best gas prices for five categories:

- Safe <30 min
- Standard <5 min
- Fast <2min
- Fastest ~1 Block (<30 sec)

The program also compares gas estimates against ETH Gas Station to show how much better our model forecasts gas prices. :)

## How we built it

Built using:

- SKLearn Machine Learning Models
- Dash
- Infura
- Web3.py

## Challenges we ran into

We ran into issues editing Dash as it was our first time using it with callbacks.

## Accomplishments that we're proud of

We are proud of the product we produced and for the capability users have to pay significantly less in gas with our forecasting technology.

## What we learned

We learned how to use Dash and web3.py.

## What's next for Squid Station

Integrate into current projects with high transaction volume and/or large data transactions.

![alt text](https://github.com/dmintercept/eth_squid_station/blob/master/assets/Front-End-Image.png)

