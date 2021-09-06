# MLPP-Assignment-One
Data Collection Assignment for MLPP, Fall 2021

For this data loading assignment, I used an ACS API key I already had in my name. I acquired this key during my summer internship as I was interacting with the ACS on a daily basis. I used code to build my API key that I learned on my own last year, but am open to new or more efficient ways to do this!

For my data selection, I opted to look at New York block data since that is my home state. Since this project felt very exploratory, I decided to pull more general demographic data at the block level for every county in the state. I pulled nine variables, including the total population in that block, as well as median income, total male population, total female population, and the total populations of the following racial groups: white, black, Asian, other, and two or more races. 

My rational behind this is that, if I am trying to solve a problem that involves needing ACS data, I’m probably going to get a lot out of knowing the financial and racial/gender makeup of the area. For a true project, I’d probably want to know income and gender breakdowns by race as well, but I did not pull those variables for this assignment. 

Once I had my API request completed, I requested the data, created column names for each variable, and merged the data and column names into a Pandas dataframe so that I could make any necessary adjustments before loading it into the database. 

I converted all income and population columns to integers and then did a high-level look at my data. I noticed that a few block groups had outlying median incomes in negative dollars, so I converted those outliers to $0. 

I also determined it would be useful to not only have the state and county FIPS codes in the dataset, but to also include the corresponding state and county name for ease of understanding when reading the data. I created functions to match the FIPS code with its corresponding name. For the state, since it was just NY, it’s a small function but I can expand it when working with other states. For county, my function is not as efficient as it could be. I at first attempted to iterate through a dictionary of county codes and names, but ran into trouble with the mapping beyond Albany County and am not sure why. I will look into that further so I can keep my code shorter going forward. 

After creating these mapping functions, I adding two new columns to my dataframe, State Name and County Name. I also removed the column that had the entire geography in one cell since I now had individual cell blocks for each piece of data, which is better for analysis going forward. Finally, I rearranged the columns in my dataframe to make it easier to read, putting state and county name at the beginning, followed by total population, income, and then demographic data.

I then converted my dataframe to a CSV and then converted that CSV to a list of lists to prepare to load into the database. I connected to the database, created the structure of my table, and used the executemany command to execute my insertion code along with the list of lists. Executemany took a very long time to run on my 15,000+ dataset, so I’d be curious to learn a more efficient way to load data going forward. After the data loaded, I pulled all the data from the table and loaded it into a dataframe to confirm it actually loaded. 
