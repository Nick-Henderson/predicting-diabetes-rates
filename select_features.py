import pandas as pd

def select_features(df, keep_lst = (['Diagnosed Diabetes Percentage',
                        'Obesity Percentage','Physical Inactivity Percentage',
                        'TOT_POP','PCT_MALE','PCT_FEMALE',
                        'EP_POV','EP_UNEMP','EP_UNINSUR','E_PCI',
                        'EP_NOHSDP','EP_AGE65','EP_AGE17',
                        'EP_SNGPNT','EP_MOBILE',
                        'EP_NOVEH','NHWA_PCT','NHBA_PCT','NHAA_PCT','H_PCT','NHNA_PCT','NHIA_PCT',
                        'in_south','in_northeast','in_midwest','in_west'
                        ])):

    df['PCT_MALE'] = round(df['TOT_MALE']/df['TOT_POP']*100,2)
    df['PCT_FEMALE'] = round(df['TOT_FEMALE']/df['TOT_POP']*100,2)

    south = ['Alabama', 'Arkansas', 'Florida', 
                'Georgia', 'Kentucky', 'Louisiana', 
                'Mississippi', 'North Carolina', 'Oklahoma', 'South Carolina',
                'Tennessee', 'Texas', 'Virginia' ,'West Virginia']

    northeast = ['connecticut','maine','massachusetts',
        'new hampshire','new jersey','new york',
        'maryland','delaware',
        'pennsylvania','rhode island','vermont','district of columbia']

    midwest = ['michigan','ohio','wisconsin','minnesota','illinois','indiana',
        'iowa','missouri','north dakota','south dakota','nebraska','kansas']

    west = ['arizona','colorado','utah','nevada','new mexico','idaho','montana','wyoming',
        'california','washington','oregon','hawaii','alaska']
    south = list(map(lambda x: x.lower(),south))

    for region,string in zip([south, northeast,midwest,west],['south', 'northeast','midwest','west']):
        df[f'in_{string}'] = 0
        df.loc[region,f'in_{string}'] = 1
        
        
    keep_columns_lst = keep_lst

    fdf = df[keep_columns_lst].copy()

    return fdf