import pandas as pd
import week

def join_and_aggregate(d=dict, sdate = str, edate = str, cntry = list):
    
    demdf = d["demographics"] # type: ignore
    epdf = d["epidemiology"] # type: ignore
    hldf = d["health"] # type: ignore
    hpdf = d["hospitalizations"] # type: ignore
    vacdf = d["vaccinations"] # type: ignore
    
    #creating a country index
    country_dict = dict(d["index"]) # type: ignore



    #JOINING ALL THE DFs
    joined_df = pd.merge(pd.merge(pd.merge(pd.merge(epdf, hpdf, on= ["date", "location_key"], how="left"), vacdf, on= ["date", "location_key"], how="left"), demdf, on= ["location_key"], how="left"), hldf, on= ["location_key"], how="left")


    #AGGREGATING THE JOINED DF

    #aggregating the dataframe
    final_df = pd.DataFrame(joined_df)
    
    #filtering by start & end date
    final_df = final_df[(final_df["date"]>= sdate) & (final_df["date"]<= edate)]

    #creating week & country columns
    final_df["country"] = final_df["location_key"].str[:2].map(country_dict)
    final_df["week"] = final_df["date"].map(week.week_extractor(final_df["date"]))

    final_df = final_df.drop(["location_key", "date"], axis="columns")

    final_df = final_df.groupby(["week", "country"]).agg({"population" : "mean", "population_male": "mean", "population_female": "mean", "population_density": "mean", 
                                     "population_age_00_09": "mean", "population_age_10_19": "mean", "population_age_20_29": "mean", 
                                     "population_age_30_39": "mean", "population_age_40_49": "mean", "population_age_50_59": "mean", 
                                     "population_age_60_69": "mean", "population_age_70_79": "mean", "population_age_80_and_older": "mean",
                                     "life_expectancy": "mean", "new_persons_fully_vaccinated" : "mean", "cumulative_persons_fully_vaccinated" : "max",
                                     "new_hospitalized_patients" : "mean", "cumulative_hospitalized_patients" : "max", "new_confirmed" : "mean", 
                                     "cumulative_confirmed" : "max", "new_deceased" : "mean", "cumulative_deceased" : "max" 
    })


    #resetting index of aggregated df
    final_df = final_df.reset_index()

    #filling 0 in place of nulls
    final_df = final_df.fillna(0)

    # filling average in place of 0 in the columns where 52 out of 53 rows belonging to USA have a non-null value
    for i in range(len(final_df)):
        if final_df.at[i, "country"] == "United States of America" and final_df.at[i, "new_persons_fully_vaccinated"]==0:
            final_df.at[i, "new_persons_fully_vaccinated"] = final_df[final_df.country == "United States of America"]["new_persons_fully_vaccinated"].mean()
    
        if final_df.at[i, "country"] == "United States of America" and final_df.at[i, "cumulative_persons_fully_vaccinated"]==0:
            final_df.at[i, "cumulative_persons_fully_vaccinated"] = final_df[final_df.country == "United States of America"]["cumulative_persons_fully_vaccinated"].mean()


    #filtering by country
    final_df = final_df[final_df["country"].isin(cntry)]


    return final_df



if __name__ == '__main__':
    join_and_aggregate()
