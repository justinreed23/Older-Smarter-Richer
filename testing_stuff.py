import datetime
import pandas as pd
import random
import numpy as np
import seaborn as sns


rng = np.random.default_rng(123)

start_year = 1970
end_year = 2020
portfolios = ["First", "Second", "Third", "Fourth", "Fifth"]
portfolios_list = []
dates_list = []


for portfolio in portfolios:
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            dates_list.append(date)
            portfolios_list.append(portfolio)

random_returns = rng.uniform(low=(-0.1 / 12), high=(0.3 / 12), size=len(dates_list))


fake_returns = pd.DataFrame(
    {"Portfolio": portfolios_list, "date": dates_list, "ret": random_returns}
)


fake_returns["cumret"] = fake_returns.groupby("Portfolio")["ret"].apply(lambda x: (x + 1).cumprod() - 1).reset_index(drop=True)


sns.lineplot(x="date",y="cumret",style="Portfolio",data=fake_returns)

