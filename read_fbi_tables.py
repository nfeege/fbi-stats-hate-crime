# Define a function that reads multiple FBI tables from multiple files and returns a combined dataframe.
def read_tables():

    # Import reqired libraries.
    import pandas as pd

    # Read FBI Hate Crime Statistics (2016) tables from Excel files into dataframes with MultiIndexing of columns.
    # Skip header and footer rows which contain meta information and are not part of the actual tables.
    df_table11 = pd.read_excel("data/fbi/Table_11_Offenses_Offense_Type_by_Participating_State_2016.xls", header=[0,1], index_col=None, skiprows=4, skip_footer=3, sheet_name="Table 11")
    
    df_table13 = pd.read_excel("data/fbi/Table_13_Hate_Crime_Incidents_per_Bias_Motivation_and_Quarter_by_State_and_Agency_2016.xls", header=[0,1], index_col=None, usecols=[0,3,4,5,6,7,8], skiprows=4, skip_footer=3, sheet_name="Table 13")


    # When reading in the tables, 'Participating state' and None end up being used as names for the first and second level multiindex for the columns.
    # These names are not related to the index levels, so change these names here:
    df_table11.columns.names = ['Category','Type']
    df_table13.columns.names = ['Category','Type']

    # Name index.
    df_table11.index.name = ['State']
    df_table13.index.name = ['State']

    # Drop row with index = "Total"
    df_table11 = df_table11.drop( 'Total', axis = 0 )

    # Rename first-level columns.
    df_table11 = df_table11.rename( index = str, columns = { "Crimes against persons":    "Crimes against persons",
                                                             "Crimes against property":   "Crimes against property",
                                                             "Crimes\nagainst\nsociety3": "Crimes against society",
                                                             "Total\noffenses":           "Crimes total" } )

    df_table13 = df_table13.rename( index = str, columns = { "Number of incidents per bias motivation":    "Incidents per bias motivation" } )


    # Rename second-level columns.
    df_table11 = df_table11.rename( index = str, columns = { "Murder and\nnonnegligent\nmanslaughter": "Murder",
                                                             "Rape\n(revised\ndefinition)1":           "Rape",
                                                             "Rape\n(legacy\ndefinition)2":            "Rape (legacy definition)",
                                                             "Aggravated\nassault":                    "Aggravated assault",
                                                             "Simple\nassault":                        "Simple assault",
                                                             "Other3":                                 "Other",
                                                             "Larceny-\ntheft":                        "Larceny, theft",
                                                             "Destruction/\ndamage/\nvandalism":       "Destruction, damage, vandalism",
                                                             "Motor\nvehicle\ntheft":                  "Motor vehicle theft",
                                                             "Other3":                                 "Other",
                                                             "Unnamed: 15_level_1":                    "Crimes against society",
                                                             "Unnamed: 0_level_1":                     "Crimes total" } )

    df_table13 = df_table13.rename( index = str, columns = { "Race/\nEthnicity/\nAncestry": "Race, ethnicity, ancestry",
                                                             "Sexual\norientation":         "Sexual orientation",
                                                             "Gender\nIdentity":            "Gender identity" } )

    # Table 11: Drop column with "Rape (legacy definition)". All entries are '0' in this column.
    df_table11 = df_table11.drop( columns = 'Rape (legacy definition)', axis = 1, level = 1 )

    # Table 13: Table 13 provides data per state and separated by individual agency types and names within those states. Here, we only want
    # to extract the totals for each state. With the way the table is read into the dataframe, the 'State' column from the original Excel table
    # is used as dataframe index. The rows that have the actual state name as index contain the values for the respective state totals. The rows
    # with 'nan' in the dataframe index correspond to the numbers reported from individual agencies. To remove the latter, we select only rows
    # where index is not 'nan'.
    df_table13 = df_table13.loc[ df_table13.index != 'nan' , : ]

    # Add column to tables: Sum of incidents in first-level column categoreis
    # df_table11[ 'CrimesAgainstPersons', 'Total' ] = df_table11[ 'CrimesAgainstPersons' ].sum( axis = 1 )
    # df_table11[ 'CrimesAgainstProperty', 'Total' ] = df_table11[ 'CrimesAgainstProperty' ].sum( axis = 1 )
    # df_table11[ 'CrimesAgainstSociety', 'Total' ] = df_table11[ 'CrimesAgainstSociety', 'CrimesAgainstSociety' ]

    # df_table13[ 'IncidentsPerBiasMotivation', 'Total' ] = df_table13[ 'IncidentsPerBiasMotivation' ].sum( axis = 1 )

    # Lexical sort columns.
    # df_table11.sort_index( axis=1 , inplace=True )
    # df_table13.sort_index( axis=1 , inplace=True )

    # Merge dataframes from individual tables into one dataframe. Use index (i.e. 'State') as key for merging.
    df_fbi = pd.merge( df_table11 , df_table13 , left_index=True, right_index=True )

    return df_fbi

# ----- end of function -----


# Define a main function.
def main():

    print( "\nReading tables from FBI Hate Crime Statistics (2016):\n" )

    df_new = read_tables()

    print( df_new.sum() )

# ----- end of function -----


# Call main function if macro is being called directly with python.
if __name__ == "__main__":
    main()
