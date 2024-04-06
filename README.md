### Team member: 
Yiqing Xia, Yizhou Shen, Eric Liu, Henry Ye 

### Basic Idea:
Explore different cryptocurrency exchanges, study their API within the documentation, and (possibly, if we have time after research) implement automated programs to exploit arbitrage opportunities.

The property of blockchain causes the arbitrage performance to be different from the usual ones. We will study the influence caused by failed transactions in blockchain on cryptocurrency arbitrage (for example, the price in exchange B was higher than in exchange A but the immediate transaction failed due to some reasons, and later the price is no longer profitable). What we are going to implement is an automated program that exploits arbitrage opportunities based on our studied model of expectations on prices in different exchanges.
We will study the price expectation of each exchange based on their past transaction records on price fluctuations and transaction fee (gas fee) fluctuations.

We will try to start with cryptocurrencies of medium market cap including Dogecoin, Shiba Inu…

Google Doc link: https://docs.google.com/document/d/1MIFtHyvE4Qb7iO7dMlvubtsNCXxcCDtgrwsV9sn01Uk/edit
Google Sheets link: https://docs.google.com/spreadsheets/d/1vp_-G1hRQcD1IdCpPBNsdEQ9aKRx4G1DtvEghktitBY/edit#gid=0


Pre Package install:
```pip install ccxt```
```pip install pyxt```
```pip install Falsk```

Run the simulator:
```python Simulator/run.py```