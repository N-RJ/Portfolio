import pandas as pd

def clean_data(d = dict):

    demographics = d["demographics"]
    epidemiology = d["epidemiology"]
    health = d["health"]
    hospitalizations = d["hospitalizations"]
    vaccinations = d["vaccinations"]
    index = d["index"]


    #CLEANING DEMOGRAPHICS DF
    #1. creating a new demdf to make all changes there
    demdf = pd.DataFrame(demographics)

    #2. deleting duplicate rows
    demdf = demdf.drop_duplicates()

    #3. removing columns population_rural, population_urban, population_largest_city, population_clustered, human_development_index
    demdf = demdf.dropna(axis="columns", how="all")

    #4. handling null values in population_male, population_female
    # creates a list of ratios of population_female to poulation columns for each row & only for rows which are not null
    pop_f = [demdf.at[i, "population_female"]/demdf.at[i, "population"] for i in range(len(demdf)) if pd.isna(demdf.at[i, "population_female"]) == False]
    ratio_f = sum(pop_f)/ len(pop_f)


    # replaces all NaN values in population_female with ratio_f * total population
    for i in range(len(demdf)):
        if pd.isna(demdf.at[i, "population_female"]) == True:
            demdf.at[i, "population_female"] = ratio_f * demdf.at[i, "population"]


    # replaces all NaN values in population_male with (1-ratio_f) * total population
    for i in range(len(demdf)):
        if pd.isna(demdf.at[i, "population_male"]) == True:
            demdf.at[i, "population_male"] = (1-ratio_f) * demdf.at[i, "population"]

    # replacing NaN values in population_density & age segmented columns with 0, because there is no fixed proportion to apply any other imputation technique
    demdf = demdf.fillna(0)





    #CLEANING EPIDEMIOLOGY DF
    #1. creating a new demdf to make all changes there
    epdf = pd.DataFrame(epidemiology)

    #2. deleting duplicate rows
    epdf = epdf.drop_duplicates()

    #3. correcting datatypes of all columns
    epdf['date'] = epdf['date'].astype('datetime64[ns]')


    #4. handling nulls
    # replacing nulls in new_confirmed by calculating its value from two consecutive cumulative_confirmed values & imputing 0 in the remaining
    for i in range(len(epdf)):
        if pd.isna(epdf.at[i, "new_confirmed"]) == True and epdf.at[i, "location_key"] == epdf.at[(i-1), "location_key"]:
            epdf.at[i, "new_confirmed"] = epdf.at[i, "cumulative_confirmed"] - epdf.at[i-1, "cumulative_confirmed"]

    epdf.new_confirmed = epdf.new_confirmed.fillna(0)


    # reverse engineering nulls in new_deceased column using cumulative_deceased wherever possible & imputing 0 in the remaining
    for i in range(len(epdf)):
        if pd.isna(epdf.at[i, "new_deceased"]) == True and epdf.at[i, "location_key"] == epdf.at[(i-1), "location_key"]:
            epdf.at[i, "new_deceased"] = epdf.at[i, "cumulative_deceased"] - epdf.at[i-1, "cumulative_deceased"]

    epdf.new_deceased = epdf.new_deceased.fillna(0)


    # filling nulls in cumulative_deceased using new_deceased
    for i in range(len(epdf)):
        if pd.isna(epdf.at[i, "cumulative_deceased"]) == True and epdf.at[i, "location_key"] == epdf.at[(i-1), "location_key"]:
            epdf.at[i, "cumulative_deceased"] = epdf.at[i, "new_deceased"] + epdf.at[i-1, "cumulative_deceased"]

    epdf.cumulative_deceased = epdf.cumulative_deceased.fillna(0)


    # dropping reamaining columns which have only 10% of non-null values
    epdf = epdf.dropna(axis="columns", thresh=2800000)        






    #CLEANING HEALTH DF
    #1. creating a new demdf to make all changes there
    hldf = pd.DataFrame(health)

    #2. deleting duplicate rows
    hldf = hldf.drop_duplicates()

    #3. handling nulls
    # dropping all columns except the first two as they only comprise NaN values
    hldf = hldf.dropna(axis="columns", how="all")







    #CLEANING HOSPITALISATIONS DF
    #1. creating a new demdf to make all changes there
    hpdf = pd.DataFrame(hospitalizations)

    #2. deleting duplicate rows
    hpdf = hpdf.drop_duplicates()

    #3. correcting datatypes
    hpdf["date"] = hpdf['date'].astype('datetime64[ns]')

    
    #4. handling nulls
    # dropping columns - new & cumulative ICU patients; new, current & cumulative ventilator patients because they all contain 0 non-null values 
    # and there is no certain calculation to derive their values from other given columns in this dataframe
    hpdf = hpdf.dropna(axis="columns", how="all")


    # filling all NaN values in new_hospitalised in a two step method by taking the difference & imputing 0
    hpdf.at[0, "new_hospitalized_patients"] = 0
    for i in range(1, len(hpdf)):
        if pd.isna(hpdf.at[i, "cumulative_hospitalized_patients"]) == True:
            if hpdf.at[i, "current_hospitalized_patients"] > hpdf.at[(i-1), "current_hospitalized_patients"] and hpdf.at[i, "location_key"] == hpdf.at[(i-1), "location_key"]:
                hpdf.at[i, "new_hospitalized_patients"] = hpdf.at[i, "current_hospitalized_patients"] - hpdf.at[(i-1), "current_hospitalized_patients"]
            else:
                hpdf.at[i, "new_hospitalized_patients"] = 0

        elif pd.isna(hpdf.at[i, "cumulative_hospitalized_patients"]) == False:    
            if hpdf.at[i, "cumulative_hospitalized_patients"] > hpdf.at[(i-1), "cumulative_hospitalized_patients"] and hpdf.at[i, "location_key"] == hpdf.at[(i-1), "location_key"]:
                hpdf.at[i, "new_hospitalized_patients"] = hpdf.at[i, "cumulative_hospitalized_patients"] - hpdf.at[(i-1), "cumulative_hospitalized_patients"]
            else:
                hpdf.at[i, "new_hospitalized_patients"] = 0


    # filling all NaN in cumulative_hospitalised
    hpdf.at[0, "cumulative_hospitalized_patients"] = 0
    for i in range(1, len(hpdf)):
        if pd.isna(hpdf.at[i, "cumulative_hospitalized_patients"]) == True and hpdf.at[i, "location_key"] == hpdf.at[(i-1), "location_key"]:
            hpdf.at[i, "cumulative_hospitalized_patients"] = hpdf.at[i, "new_hospitalized_patients"] + hpdf.at[(i-1), "cumulative_hospitalized_patients"]

    hpdf["cumulative_hospitalized_patients"] = hpdf["cumulative_hospitalized_patients"].fillna(0)


    # dropping current_ICU & current_hospitalized column due to insufficient data
    hpdf = hpdf.drop(columns=["current_intensive_care_patients", "current_hospitalized_patients"])







    # CLEANING VACCINATIONS DF
    #1. creating a new demdf to make all changes there
    vacdf = pd.DataFrame(vaccinations)

    #2. deleting duplicate rows
    vacdf = vacdf.drop_duplicates()

    #3. correcting column's datatypes
    vacdf.date = vacdf.date.astype('datetime64[ns]')


    #4. handling nulls
    # dropping all columns except the first two as they only comprise NaN values
    vacdf = vacdf.dropna(axis="columns", how="all")

    # imputing nulls in new_vaccinated column
    vacdf.at[0, "new_persons_fully_vaccinated"] = 0
    for i in range(1, len(vacdf)):
        if pd.isna(vacdf.at[i, "new_persons_fully_vaccinated"]) == True and vacdf.at[i, "location_key"] == vacdf.at[(i-1), "location_key"]:
            vacdf.at[i, "new_persons_fully_vaccinated"] = vacdf.at[i, "cumulative_persons_fully_vaccinated"] - vacdf.at[(i-1), "cumulative_persons_fully_vaccinated"]

    vacdf["new_persons_fully_vaccinated"] = vacdf["new_persons_fully_vaccinated"].fillna(0)



    # creating a set of pairs of country_code & country_names from index_df
    s1 = {(index.at[i, "country_code"], index.at[i, "country_name"]) for i in range(len(index))}



    return {
        "demographics": demdf,
        "epidemiology": epdf,
        "health": hldf,
        "hospitalizations": hpdf,
        "vaccinations": vacdf,
        "index" : s1
    }



if __name__ == '__main__':
    clean_data()