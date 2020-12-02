import pandas as pd

def import_diabetes():

    #import socioeconomic/education data
    svi = pd.read_csv('data/2018SVI.csv')
    #remove problematic top row
    svi.drop([0],inplace=True)

    #import diabetes, new diabetes, obesity, and physical inactivity data 
    diabetes = pd.read_csv('data/2018diabetes.csv')
    nd = pd.read_csv('data/2018newdiabetes.csv')
    obe = pd.read_csv('data/2018obesity.csv')
    phys = pd.read_csv('data/2018physicalinactivity.csv')

    # clean up these four dataframes (they are formatted the same and have the same errors)
    for DF in [diabetes,nd,obe,phys]:

        #fix errors with counties that have "'s" and move data back to correct columns in those rows
        mask = DF['State']=='s County'
        DF.loc[mask,'County'] = DF.loc[mask,'County'].str.slice(stop=-4)+"'s"
        DF.loc[mask,'State'] = 'Maryland'
        DF.loc[mask,DF.columns[4]] = DF.loc[mask,DF.columns[5]]
        DF.loc[mask,DF.columns[5]] = DF.loc[mask,DF.columns[6]]

        # fix error with O'Brien County and move data back to correct columns in those rows
        mask = DF['State']=='brien County'
        DF.loc[mask,'County'] = DF.loc[mask,'County'].str.slice(stop=-4)+ "'Brien County"
        DF.loc[mask,'State'] = 'Iowa'
        DF.loc[mask,DF.columns[4]] = DF.loc[mask,DF.columns[5]]
        DF.loc[mask,DF.columns[5]] = DF.loc[mask,DF.columns[6]]

        # fix typo on Prince of Wales-Hyder Census Area
        mask = DF['County']=='Prince of Wales-Hyder Censu'
        DF.loc[mask,'County'] = 'Prince of Wales-Hyder'

        # drop the extra column that was added where typos moved data to the right one column
        DF.drop(columns='Unnamed: 6',inplace=True)
    
    # join the three obesity, diabetes, new diabetes, and inactivity dataframes on County and State, and select relevant columns
    # note, it would have been possible to just take the relevant columns 
    # and add them to one dataframe, but I wasn't certain the order would be correct, 
    # so a 'join' seemed safer. 
    diabetes = pd.merge(left=diabetes, right=nd, on=['State','County'], how='inner')
    diabetes = pd.merge(left=diabetes, right=obe, on=['State','County'], how='inner')
    diabetes = pd.merge(left=diabetes, right=phys, on=['State','County'], how='inner')
    diabetes = diabetes[['County','State','Diagnosed Diabetes Percentage','Newly Diagnosed Diabetes Rate per 1000','Obesity Percentage','Physical Inactivity Percentage']]
    
    # convert percentage columns to numbers (they were objects)
    for column in ['Diagnosed Diabetes Percentage','Newly Diagnosed Diabetes Rate per 1000','Obesity Percentage','Physical Inactivity Percentage']:
        diabetes[column] = diabetes[column].astype('float')
    

    # import population demographic data
    demo = pd.read_csv('data/cc-est2019-alldata.csv')
    # select the relevant year (2018), and relevant age group (all ages)
    demo = demo[demo['YEAR'] == 11]
    demo = demo[demo['AGEGRP'] == 0]
    #drop the county that was dropped from previous dataframes
    demo = demo[demo['CTYNAME']!='Rio Arriba County']

    # Create total (combine male and female) and percentage (total/population) 
    # columns for all categories 
    headers = []
    cats = demo.columns[10:]
    for cat in cats:
        if 'FEMALE' in cat:
            headers.append(cat[:-6])
    for header in headers:
        demo[f'{header}TOT'] = demo[f'{header}MALE'] + demo[f'{header}FEMALE']
        demo[f'{header}PCT'] = round(demo[f'{header}TOT']/demo['TOT_POP']*100,2)



    # clean demographic data county formatting to match svi county formatting
    # truncate county, census area, borough, parish, and municipality from county names
    for row in range(len(demo)):
        if demo.iloc[row,4][-6:] == 'County':
            demo.iloc[row,4] = demo.iloc[row,4][:-7]
        elif demo.iloc[row,4][-11:] == 'Census Area':
            demo.iloc[row,4] = demo.iloc[row,4][:-12]
        elif demo.iloc[row,4][-12:] == ' and Borough':
            demo.iloc[row,4] = demo.iloc[row,4]
        elif demo.iloc[row,4][-7:] == 'Borough':
            demo.iloc[row,4] = demo.iloc[row,4][:-8]
        elif demo.iloc[row,4][-6:] == 'Parish':
            demo.iloc[row,4] = demo.iloc[row,4][:-7]
        elif demo.iloc[row,4][-12:] == 'Municipality':
            demo.iloc[row,4] = demo.iloc[row,4][:-13]
            
    # clean diabetes county formatting to match svi county formatting
    for row in range(len(diabetes)):
        if diabetes.iloc[row,0][-6:] == 'County':
            diabetes.iloc[row,0] = diabetes.iloc[row,0][:-7]
        elif diabetes.iloc[row,0][-11:] == 'Census Area':
            diabetes.iloc[row,0] = diabetes.iloc[row,0][:-12]
        elif diabetes.iloc[row,0][-12:] == ' and Borough':
            diabetes.iloc[row,0] = diabetes.iloc[row,0]
        elif diabetes.iloc[row,0][-7:] == 'Borough':
            diabetes.iloc[row,0] = diabetes.iloc[row,0][:-8]
        elif diabetes.iloc[row,0][-6:] == 'Parish':
            diabetes.iloc[row,0] = diabetes.iloc[row,0][:-7]
        elif diabetes.iloc[row,0][-12:] == 'Municipality':
            diabetes.iloc[row,0] = diabetes.iloc[row,0][:-13]
            
    # fix formatting of dona ana
    demo.loc[411046,'CTYNAME'] = 'Doña Ana'

    #rename columns to match other dataframes
    demo.rename(columns={"CTYNAME": "County", "STNAME": "State"},inplace=True)

    # lowercase state names and county names and rename columns to match
    svi['State']=svi['STATE'].str.lower().values
    svi.drop(columns = ['STATE'],inplace=True)
    svi.rename(columns={'COUNTY':'County'},inplace=True)
    svi['County']=svi['County'].str.lower()

    demo['County']=demo['County'].str.lower()
    demo['State']=demo['State'].str.lower()

    diabetes['County']=diabetes['County'].str.lower()
    diabetes['State']=diabetes['State'].str.lower()

    # set State and County to index in all dataframes to make join easy
    demo.set_index(['State', 'County'],inplace=True)
    diabetes.set_index(['State', 'County'],inplace=True)
    svi.set_index(['State', 'County'],inplace=True)

    df = diabetes.join(demo,how='inner').join(svi,how='inner')

    return df