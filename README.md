# Stock Mutt
A Linear Regression Stock Prediction Engine built on Polygon.io</sub>


## Currently a Work In Progress. 

### Completed
- Request data from [Polygon.io](https://polygon.io/) while respecting access limits 
    - Defaults to 5 req/min as allowed on [Polygon Basic Tier](https://polygon.io/pricing)
- Cache data from requests
    - Currently only Local Cache is implemented 
- Stock ticker list collection 
- Stock ticker data collection
    - Defaults to 710 days of history

### Planned
- Load data into [pandas](https://pandas.pydata.org/) DataFrame
- Use [scikit](https://scikit-learn.org/stable/) to find linear regressions on various date ranges
- Present stocks with most consistent, positive regressions for selection 