import pandas as pd

def load_df(ipath):
    #import CSVs to dataframes
    demographics = pd.read_csv(ipath + "/demographics.csv")
    epidemiology = pd.read_csv(ipath + "/epidemiology.csv")
    health = pd.read_csv(ipath + "/health.csv")
    hospitalizations = pd.read_csv(ipath + "/hospitalizations.csv")
    index = pd.read_csv(ipath + "/index.csv")
    vaccinations = pd.read_csv(ipath + "/vaccinations.csv")

    return {
        "demographics": demographics,
        "epidemiology": epidemiology,
        "health": health,
        "hospitalizations": hospitalizations,
        "index": index,
        "vaccinations": vaccinations
    }

if __name__ == '__main__':
    load_df()