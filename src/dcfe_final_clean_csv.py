# the usual imports for Jupyter notebook explanations
import pandas as pd
import numpy as np
import calendar
import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost.sklearn import XGBRegressor
from sklearn import metrics
from sklearn.metrics import r2_score




def year_change(year):
    '''
    function to convert one and two digit years into four digits
    '''
    if len(year)==1:
        year='200'+ year
    else:
        year='20'+year

    return year


def update_databases():
    '''
    function that will update all database files and include forecasts for the
    next three days weather scraped from the web.
    '''

    pass


def get_police_data():
    # import the Vancouver Police Department's most recent data, available every Sunday.
    # this will be automated in the next iteration of this project
    df=pd.read_csv('data/crime_csv_all_years.csv',parse_dates={'dttime':[1,2,3]}, keep_date_col=True)
    # dttime added for the next step which is gatherind day of the week data

    # make a copy of the original data to keep an original dataframe intact
    df_temp=df.copy()

    # add day of the week to original data
    df_temp['day_of_week']=df_temp['dttime'].dt.weekday_name

    # remove missing data, all (or nearly all) of which is the non-property crime data
    # non-property crime data lacks all address information due to privacy concerns
    df2=df_temp.dropna()



    # rename columns as all caps is tedious to work with
    df3=df2.rename(index=str, columns={"YEAR": "year", "MONTH": "month", "DAY":"day","HOUR":"hour",
                                   "MINUTE":"minute", "NEIGHBOURHOOD":"neighborhood"})


    # sort by date
    df4=df3.sort_values(['year','month','day','hour','minute'])

    # remove extraneous data
    df5=df4.drop(['minute', 'HUNDRED_BLOCK','TYPE'], axis=1)

    # change all possible values to numeric form
    df6=df5.apply(pd.to_numeric, errors='ignore')

    # bin by 1200am-1159am, 1200pm -1159pm
    hourbins = [-0.1,12.0,24.1]
    hourlabels = ['1200am-1159am', '1200pm-1159pm']
    # group by neighborhood, by day_segment
    df6['day_segment'] = pd.cut(df6["hour"], bins=hourbins,labels=hourlabels)

    # remove extraneous data
    df7=df6[['year', 'month', 'day', 'day_of_week','day_segment', 'neighborhood']]

    # group by neighborhood, by day_segment
    df8=df7.groupby(df7.columns.tolist()).size()
    df9=pd.DataFrame(df8).reset_index()
    df10=df9.rename(index=str, columns={ 0 :"number_of_crimes"})
    # make final copy for merging

    # remove outlier of 499 crimes due to 2011 Stanley Cup riot
    df11=df10.loc[df10['number_of_crimes']!=df10['number_of_crimes'].max()]

    # remove second outlier of 104 crimes due to unknown reason
    df12=df11.loc[df11['number_of_crimes']!=df11['number_of_crimes'].max()]


    df_final=df12.copy()

    return df_final


def get_weather_data():
    # import the (US) National Weather Service's most recent data for Bellingham, WA, airport, available every day
    # this will be automated in the next iteration of this project and will use Vancouver weather data
    wdf=pd.read_csv('data/BA_weather_data.csv')

    # make a copy of the original data to keep an original dataframe intact
    wdf2=wdf.copy()

    # remove extraneous data
    wdf3=wdf2[['DATE', 'TMAX', 'TMIN']]

    # rename columns as all caps is tedious to work with
    wdf4=wdf3.rename(index=str, columns={ "DATE":"date", "TMAX":"tmax","TMIN":"tmin"})

    # extract data from wdf3 in a more usable form
    wdf4['year'] = wdf4.date.str.split('/').str.get(2)
    wdf4['month'] = wdf4.date.str.split('/').str.get(0)
    wdf4['day']=wdf4.date.str.split('/').str.get(1)
    wdf4=wdf4.drop('date', axis=1)
    # change year from 2 digits to 4 for merging
    wdf4.year='20'+ wdf4.year
    # change all possible values to numeric form
    wdf4=wdf4.apply(pd.to_numeric, errors='ignore')

    # make final copy for merging
    wdf_final=wdf4.copy()

    return wdf_final


def get_cpi_data():
    # import the consumer price index for Vancouver, available monthly from Statistics Canada
    # this will be automated in the next iteration
    cpi_df=pd.read_csv('data/consumer_price_index_nohead.csv')
    # make a copy of the original data to keep an original dataframe intact
    cpi_df2=cpi_df.copy()

    # import the consumer price index for Vancouver, available monthly from Statistics Canada
    # this will be automated in the next iteration
    cpi_df=pd.read_csv('data/consumer_price_index_nohead.csv')
    # make a copy of the original data to keep an original dataframe intact
    cpi_df2=cpi_df.copy()

    # extract data from cpi_df2 in a more usable form
    cpi_df2['year'] = cpi_df2.date.str.split('-').str.get(0)
    cpi_df2['month'] = cpi_df2.date.str.split('-').str.get(1)
    cpi_df2.drop('date', axis=1,inplace=True)
    cpi_df3=cpi_df2.copy()

    # change month from name to numeric
    import calendar
    d=dict((v,k) for k,v in enumerate(calendar.month_abbr))
    cpi_df3.month=cpi_df3.month.map(d)

    # change year from 1 or 2 digits to 4 for merging
    cpi_df3['year']=cpi_df3['year'].apply(year_change)

    # change all possible values to numeric form
    cpi_df3=cpi_df3.apply(pd.to_numeric, errors='ignore')

    # make final copy for merging
    cpi_df_final=cpi_df3.copy()

    return cpi_df_final


def get_gpd_data():
    # import the gross domestic product for British Columbia, available monthly from Statistics Canada
    # this will be automated in the next iteration and will be for Vancouver at best and British Columbia
    # if this is not possible
    gdp_df=pd.read_csv('data/gdp_2007dollars_nohead.csv')
    # make a copy of the original data to keep an original dataframe intact
    gdp_df2=gdp_df.copy()

    # extract data from cpi_df2 in a more usable form
    gdp_df2['year'] = gdp_df2.date.str.split('-').str.get(0)
    gdp_df2['month'] = gdp_df2.date.str.split('-').str.get(1)
    gdp_df3=gdp_df2.drop('date', axis=1)
    gdp_df4=gdp_df3.copy()

    # change month from name to numeric
    d=dict((v,k) for k,v in enumerate(calendar.month_abbr))
    gdp_df4.month=gdp_df4.month.map(d)
    # change year from 1 or 2 digits to 4 for merging
    gdp_df4['year']=gdp_df4['year'].apply(year_change)

    # change all possible values to numeric form
    gdp_df5=gdp_df4.apply(pd.to_numeric, errors='ignore')

    # make final copy for merging
    gdp_df_final=gdp_df5.copy()

    return(gdp_df_final)


def get_employment_data():
    # import unemployment data for British Columbia, available monthly from Statistics Canada
    # this will be automated in the next iteration
    emp_df=pd.read_csv('data/employment_nohead.csv')
    # make a copy of the original data to keep an original dataframe intact
    emp_df2=emp_df.copy()

    # extract data from cpi_df2 in a more usable form
    emp_df2['year'] = emp_df2.date.str.split('-').str.get(0)
    emp_df2['month'] = emp_df2.date.str.split('-').str.get(1)
    emp_df3=emp_df2.drop('date', axis=1)

    # change month from name to numeric
    import calendar
    d=dict((v,k) for k,v in enumerate(calendar.month_abbr))
    emp_df3.month=emp_df3.month.map(d)
    # change year from 1 or 2 digits to 4 for merging
    emp_df3['year']=emp_df3['year'].apply(year_change)

    # change all possible values to numeric form
    emp_df4=emp_df3.apply(pd.to_numeric, errors='ignore')

    # make final copy for merging
    emp_df_final=emp_df4.copy()

    return emp_df_final


def get_drug_data():
    # import drug posession data for British Columbia, available monthly from Statistics Canada
    # this will be automated in the next iteration
    drugs_df=pd.read_csv('data/drug_offences_2006_to_2016.csv')
    # make a copy of the original data to keep an original dataframe intact
    drugs_df2=drugs_df.copy()

    # remove extraneous data
    drugs_df3=drugs_df2[['year','Possession, cocaine ','Heroin, possession ',]]
    # make final copy to avoid slicing issues in Pandas
    drugs_df4=drugs_df3.copy()

    # insert row using means for 2017
    drugs_df4.loc[14]=[2017, drugs_df4['Possession, cocaine '].mean(),drugs_df4['Heroin, possession '].mean()]

    # insert row using means for 2018
    drugs_df4.loc[15]=[2018, drugs_df4['Possession, cocaine '].mean(),drugs_df4['Heroin, possession '].mean()]

    # make final copy for merging
    drugs_df_final=drugs_df4.copy()

    return drugs_df_final


def get_heroin_price_data():
    # import annual heroin price data for Canada, gathered manually from various publications of the United Nations
    # this will be automated in the next iteration
    hp_df=pd.read_csv('data/Heroin_Prices.csv')
    # make a copy of the original data to keep an original dataframe intacthp_df=pd.read_csv('data/Heroin_Prices.csv')
    hp_df2=hp_df.copy()

    # insert row using means for 2018
    hp_df2.loc[15]=[2018, hp_df2['Heroin Price Canada'].mean()]

    # make final copy for merging
    hp_df_final=hp_df2.copy()

    return hp_df_final



def compile_data(df):
    '''
    function that compiles all databases and also performs feature engineering
    '''

    # merge exisitng dataframes
    new_df1=pd.merge(wdf_final,df, how='left', on=['year','month','day'])



    # merge exisitng dataframes
    new_df2=pd.merge(new_df1,cpi_df_final, how='left', on=['year','month'])



    # merge exisitng dataframes
    new_df3=pd.merge(new_df2,gdp_df_final, how='left', on=['year','month'])



    # merge exisitng dataframes
    new_df4=pd.merge(new_df3,emp_df_final, how='left', on=['year','month'])



    # merge exisitng dataframes
    new_df5=pd.merge(new_df4,drugs_df_final, how='left', on=['year'])



    # merge exisitng dataframes
    new_df6=pd.merge(new_df5,hp_df_final, how='left', on=['year'])

    # change all possible values to numeric form
    new_df7=new_df6.apply(pd.to_numeric, errors='ignore')

    # one hot encode day_segment and day_of_week for regession
    day_segment_number=['day_segment']
    day_of_week_number=['day_of_week']
    new_df8=pd.get_dummies(new_df7,columns=day_segment_number, drop_first=True)
    new_df9=pd.get_dummies(new_df8,columns=day_of_week_number)
    new_df9.dropna()
    new_df10=new_df9.copy()
    # isolate the one high property crime neighborhood
    temp_cbd_df=new_df10[new_df10.neighborhood == "Central Business District"]

    # eliminate neighborhood column for regression
    temp2_cbd_df=temp_cbd_df.drop(['neighborhood'],axis=1)
    temp3_cbd_df=temp2_cbd_df.dropna()
    cbd_df=temp3_cbd_df.copy()
    # group all other neighborhoods
    temp2_ab_cbd_df=new_df10[new_df10.neighborhood != "Central Business District"]
    temp3_ab_cbd_df=temp2_ab_cbd_df.dropna()

    # one hot encode neighborhood for regression
    neighborhood_number=['neighborhood']
    temp4_ab_cbd_df=pd.get_dummies(temp3_ab_cbd_df,columns=neighborhood_number, drop_first=False)
    ab_cbd_df=temp4_ab_cbd_df.copy()

    return cbd_df, ab_cbd_df


def create_cbd_input():
    '''
    create template on which to apply the cbd model
    '''

    # load basic template from data folder
    df=pd.read_csv('data/cbd_template.csv')
    d1=datetime.date.today() + datetime.timedelta(days=1)
    d2=datetime.date.today() + datetime.timedelta(days=2)
    d3=datetime.date.today() + datetime.timedelta(days=3)
    d4=datetime.date.today() + datetime.timedelta(days=4)
    d5=datetime.date.today() + datetime.timedelta(days=5)
    d6=datetime.date.today() + datetime.timedelta(days=6)
    d7=datetime.date.today() + datetime.timedelta(days=7)

    year_list=[d1.year,d1.year,d2.year,d2.year,d3.year,d3.year,d4.year,d4.year,d5.year,d5.year,d6.year,d6.year,d7.year,d7.year]

    month_list=[d1.month,d1.month,d2.month,d2.month,d3.month,d3.month,d4.month,d4.month,d5.month,d5.month,d6.month,d6.month,d7.month,d7.month]

    day_list=[d1.day,d1.day,d2.day,d2.day,d3.day,d3.day,d4.day,d4.day,d5.day,d5.day,d6.day,d6.day,d7.day,d7.day]

    day_of_week_list=[d1.weekday(),d1.weekday(),d2.weekday(),d2.weekday(),d3.weekday(),d3.weekday(),d4.weekday(),d4.weekday(),d5.weekday(),d5.weekday(),d6.weekday(),d6.weekday(),d7.weekday(),d7.weekday()]

    se1 = pd.Series(year_list)
    se2 = pd.Series(month_list)
    se3 = pd.Series(day_list)
    se4 = pd.Series(day_of_week_list)

    df['year'] = se1.values
    df['month'] = se2.values
    df['day'] = se3.values
    df['day_of_week']=se4.values

    days = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}

    df['day_of_week'] = df['day_of_week'].apply(lambda x: days[x])

    df2=df.copy()

    cbd_new_df1=pd.merge(df2,wdf_final, how='left', on=['year','month','day'])



    # merge exisitng dataframes
    cbd_new_df2=pd.merge(cbd_new_df1,cpi_df_final, how='left', on=['year','month'])



    # merge exisitng dataframes
    cbd_new_df3=pd.merge(cbd_new_df2,gdp_df_final, how='left', on=['year','month'])



    # merge exisitng dataframes
    cbd_new_df4=pd.merge(cbd_new_df3,emp_df_final, how='left', on=['year','month'])



    # merge exisitng dataframes
    cbd_new_df5=pd.merge(cbd_new_df4,drugs_df_final, how='left', on=['year'])



    # merge exisitng dataframes
    cbd_new_df6=pd.merge(cbd_new_df5,hp_df_final, how='left', on=['year'])

    # change all possible values to numeric form
    cbd_new_df7=cbd_new_df6.apply(pd.to_numeric, errors='ignore')

    # get dataframe for eventual output
    cbd_out=cbd_new_df7[['year','month','day','day_of_week','day_segment']]
    # one hot encode day_segment and day_of_week for regession
    day_segment_number=['day_segment']
    day_of_week_number=['day_of_week']
    cbd_new_df8=pd.get_dummies(cbd_new_df7,columns=day_segment_number, drop_first=True)
    cbd_new_df9=pd.get_dummies(cbd_new_df8,columns=day_of_week_number)
    cbd_input=cbd_new_df9.copy()

    return cbd_input,cbd_out



def create_ab_cbd_input():
    '''
    create template on which to apply the ab_cbd model
    '''
    # load basic template from data folder
    df=pd.read_csv('data/ab_cbd_template.csv')
    d1=datetime.date.today() + datetime.timedelta(days=1)
    d2=datetime.date.today() + datetime.timedelta(days=2)
    d3=datetime.date.today() + datetime.timedelta(days=3)
    d4=datetime.date.today() + datetime.timedelta(days=4)
    d5=datetime.date.today() + datetime.timedelta(days=5)
    d6=datetime.date.today() + datetime.timedelta(days=6)
    d7=datetime.date.today() + datetime.timedelta(days=7)

    year_list=[d1.year,d1.year,d2.year,d2.year,d3.year,d3.year,d4.year,d4.year,d5.year,d5.year,d6.year,d6.year,d7.year,d7.year]*23

    month_list=[d1.month,d1.month,d2.month,d2.month,d3.month,d3.month,d4.month,d4.month,d5.month,d5.month,d6.month,d6.month,d7.month,d7.month]*23

    day_list=[d1.day,d1.day,d2.day,d2.day,d3.day,d3.day,d4.day,d4.day,d5.day,d5.day,d6.day,d6.day,d7.day,d7.day]*23

    day_of_week_list=[d1.weekday(),d1.weekday(),d2.weekday(),d2.weekday(),d3.weekday(),d3.weekday(),d4.weekday(),d4.weekday(),d5.weekday(),d5.weekday(),d6.weekday(),d6.weekday(),d7.weekday(),d7.weekday()]*23

    se1 = pd.Series(year_list)
    se2 = pd.Series(month_list)
    se3 = pd.Series(day_list)
    se4 = pd.Series(day_of_week_list)

    df['year'] = se1.values
    df['month'] = se2.values
    df['day'] = se3.values
    df['day_of_week']=se4.values

    days = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}

    df['day_of_week'] = df['day_of_week'].apply(lambda x: days[x])

    df2=df.copy()

    ab_cbd_new_df1=pd.merge(df2,wdf_final, how='left', on=['year','month','day'])



    # merge exisitng dataframes
    ab_cbd_new_df2=pd.merge(ab_cbd_new_df1,cpi_df_final, how='left', on=['year','month'])



    # merge exisitng dataframes
    ab_cbd_new_df3=pd.merge(ab_cbd_new_df2,gdp_df_final, how='left', on=['year','month'])



    # merge exisitng dataframes
    ab_cbd_new_df4=pd.merge(ab_cbd_new_df3,emp_df_final, how='left', on=['year','month'])



    # merge exisitng dataframes
    ab_cbd_new_df5=pd.merge(ab_cbd_new_df4,drugs_df_final, how='left', on=['year'])



    # merge exisitng dataframes
    ab_cbd_new_df6=pd.merge(ab_cbd_new_df5,hp_df_final, how='left', on=['year'])

    # change all possible values to numeric form
    ab_cbd_new_df7=ab_cbd_new_df6.apply(pd.to_numeric, errors='ignore')

    # get dataframe for eventual output
    ab_cbd_out=ab_cbd_new_df7[['neighborhood','year','month','day','day_of_week','day_segment']]
    # one hot encode day_segment and day_of_week for regession
    day_segment_number=['day_segment']
    day_of_week_number=['day_of_week']
    ab_cbd_new_df8=pd.get_dummies(ab_cbd_new_df7,columns=day_segment_number, drop_first=True)
    ab_cbd_new_df9=pd.get_dummies(ab_cbd_new_df8,columns=day_of_week_number)

    # one hot encode neighborhood for regression
    neighborhood_number=['neighborhood']
    ab_cbd_new_df10=pd.get_dummies(ab_cbd_new_df9,columns=neighborhood_number)
    ab_cbd_input=ab_cbd_new_df10.copy()

    return ab_cbd_input, ab_cbd_out


def rearrange_input_cbd(cbd_input):

    cbd_input2=cbd_input.copy()
    cbd_input3=cbd_input2[['tmax', 'tmin', 'year', 'month', 'day',
       'consumer_price_index', 'gdp_millions_2007',
       'seasonally_adjusted_unemployment', 'unadjusted_unemployment',
       'Possession, cocaine ', 'Heroin, possession ', 'Heroin Price Canada',
       'day_segment_1200pm-1159pm', 'day_of_week_Monday',
       'day_of_week_Saturday', 'day_of_week_Sunday', 'day_of_week_Thursday',
       'day_of_week_Tuesday', 'day_of_week_Wednesday']]
    cbd_finalinput=cbd_input3.copy()

    return cbd_finalinput


def rearrange_input_ab_cbd(ab_cbd_input):
    ab_cbd_input2=ab_cbd_input.rename(columns={'neighborhood_Grandview Woodland':'neighborhood_Grandview-Woodland', 'neighborhood_Arbutus Ridge':'neighborhood_Arbutus Ridge'})
    ab_cbd_input3=ab_cbd_input2.copy()
    ab_cbd_input4=ab_cbd_input3[['tmax', 'tmin', 'year', 'month', 'day',
       'consumer_price_index', 'gdp_millions_2007',
       'seasonally_adjusted_unemployment', 'unadjusted_unemployment',
       'Possession, cocaine ', 'Heroin, possession ', 'Heroin Price Canada',
       'day_segment_1200pm-1159pm', 'day_of_week_Monday',
       'day_of_week_Saturday', 'day_of_week_Sunday', 'day_of_week_Thursday',
       'day_of_week_Tuesday', 'day_of_week_Wednesday',
       'neighborhood_Arbutus Ridge', 'neighborhood_Dunbar-Southlands',
       'neighborhood_Fairview', 'neighborhood_Grandview-Woodland',
       'neighborhood_Hastings-Sunrise',
       'neighborhood_Kensington-Cedar Cottage', 'neighborhood_Kerrisdale',
       'neighborhood_Killarney', 'neighborhood_Kitsilano',
       'neighborhood_Marpole', 'neighborhood_Mount Pleasant',
       'neighborhood_Musqueam', 'neighborhood_Oakridge',
       'neighborhood_Renfrew-Collingwood', 'neighborhood_Riley Park',
       'neighborhood_Shaughnessy', 'neighborhood_South Cambie',
       'neighborhood_Stanley Park', 'neighborhood_Strathcona',
       'neighborhood_Sunset', 'neighborhood_Victoria-Fraserview',
       'neighborhood_West End', 'neighborhood_West Point Grey']]
    ab_cbd_finalinput=ab_cbd_input4.copy()

    return ab_cbd_finalinput

def cbd_model(cbd_df,cbd_finalinput):
    '''
    function that creates model from the cbd dataframe and returns the predicted
    number of crimes for the next three days
    '''

    X_cbd=cbd_df[['year', 'month', 'day', 'tmax', 'tmin', 'consumer_price_index',
       'gdp_millions_2007', 'seasonally_adjusted_unemployment',
       'unadjusted_unemployment', 'Possession, cocaine ',
       'Heroin, possession ', 'Heroin Price Canada',
       'day_segment_1200pm-1159pm', 'day_of_week_Monday',
       'day_of_week_Saturday', 'day_of_week_Sunday', 'day_of_week_Thursday',
       'day_of_week_Tuesday', 'day_of_week_Wednesday']]
    y_cbd=cbd_df['number_of_crimes']


    scaler = StandardScaler()
    scaler.fit(X_cbd)  # Don't cheat - fit only on training data
    X_cbd = scaler.transform(X_cbd)
    cbd_input_scaled = scaler.transform(cbd_finalinput)
    xgb=XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=1, gamma=0, learning_rate=0.1, max_delta_step=0,
       max_depth=3, min_child_weight=1, missing=None, n_estimators=100,
       n_jobs=1, nthread=None, objective='reg:linear', random_state=0,
       reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
       silent=True, subsample=1)
    xgb.fit(X_cbd,y_cbd)
    predict_cbd=xgb.predict(cbd_input_scaled)

    return predict_cbd

def ab_cbd_model(ab_cbd_df,ab_cbd_finalinput):
    '''
    function that creates model from the all but cbd dataframe and returns the predicted
    number of crimes for the next three days
    '''
    ab_cbd_df2=ab_cbd_df.dropna()

    X_ab_cbd=ab_cbd_df2[['tmax', 'tmin', 'year', 'month', 'day',
       'consumer_price_index', 'gdp_millions_2007',
       'seasonally_adjusted_unemployment', 'unadjusted_unemployment',
       'Possession, cocaine ', 'Heroin, possession ', 'Heroin Price Canada',
       'day_segment_1200pm-1159pm', 'day_of_week_Monday',
       'day_of_week_Saturday', 'day_of_week_Sunday', 'day_of_week_Thursday',
       'day_of_week_Tuesday', 'day_of_week_Wednesday',
       'neighborhood_Arbutus Ridge', 'neighborhood_Dunbar-Southlands',
       'neighborhood_Fairview', 'neighborhood_Grandview-Woodland',
       'neighborhood_Hastings-Sunrise',
       'neighborhood_Kensington-Cedar Cottage', 'neighborhood_Kerrisdale',
       'neighborhood_Killarney', 'neighborhood_Kitsilano',
       'neighborhood_Marpole', 'neighborhood_Mount Pleasant',
       'neighborhood_Musqueam', 'neighborhood_Oakridge',
       'neighborhood_Renfrew-Collingwood', 'neighborhood_Riley Park',
       'neighborhood_Shaughnessy', 'neighborhood_South Cambie',
       'neighborhood_Stanley Park', 'neighborhood_Strathcona',
       'neighborhood_Sunset', 'neighborhood_Victoria-Fraserview',
       'neighborhood_West End', 'neighborhood_West Point Grey']]
    y_ab_cbd=ab_cbd_df2['number_of_crimes']


    scaler = StandardScaler()
    scaler.fit(X_ab_cbd)  # Don't cheat - fit only on training data
    X_ab_cbd = scaler.transform(X_ab_cbd)
    ab_cbd_input_scaled = scaler.transform(ab_cbd_finalinput)
    xgb=XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=1, gamma=0, learning_rate=0.1, max_delta_step=0,
       max_depth=3, min_child_weight=1, missing=None, n_estimators=100,
       n_jobs=1, nthread=-1, objective='reg:linear', random_state=0,
       reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
       silent=True, subsample=1)
    xgb.fit(X_ab_cbd,y_ab_cbd)
    predict_ab_cbd=xgb.predict(ab_cbd_input_scaled)

    return predict_ab_cbd


def cbd_output(cbd_out,predict_cbd):
    '''
    return dataframe for the central business district with predicted number
    of property crimes
    '''

    nbhdlst=['Central Business District']*14
    se1=pd.Series(nbhdlst)
    se2=pd.Series(predict_cbd)
    cbd_out['neighborhood']=se1.values
    cbd_out['number_of_crimes']=se2.values
    cbd_out2=cbd_out[['neighborhood','year', 'month', 'day', 'day_of_week', 'day_segment','number_of_crimes']]

    cbd_finalout=cbd_out2.copy()

    return cbd_finalout

def ab_cbd_output(ab_cbd_out,predict_ab_cbd):
    '''
    return dataframe for the central business district with predicted number
    of property crimes
    '''

    se2=pd.Series(predict_ab_cbd)
    ab_cbd_out['number_of_crimes']=se2.values
    ab_cbd_out2=ab_cbd_out[['neighborhood','year', 'month', 'day', 'day_of_week', 'day_segment','number_of_crimes']]

    ab_cbd_finalout=ab_cbd_out2.copy()

    return ab_cbd_finalout





def final_output(cbd_finalout, ab_cbd_finalout):
    '''
    function that gives a final dataframe as the output of the prediction
    process
    '''
    frames=[cbd_finalout, ab_cbd_finalout]
    result=pd.concat(frames)
    return result

def output_csv(result):
    out=result.to_csv('out.csv', sep=',')




if __name__ == "__main__":

    df_final=get_police_data()
    wdf_final=get_weather_data()
    cpi_df_final=get_cpi_data()
    gdp_df_final=get_gpd_data()
    emp_df_final=get_employment_data()
    drugs_df_final=get_drug_data()
    hp_df_final=get_heroin_price_data()

    cbd_df, ab_cbd_df=compile_data(df_final)

    cbd_input, cbd_out=create_cbd_input()

    cbd_finalinput=rearrange_input_cbd(cbd_input)


    predict_cbd=cbd_model(cbd_df,cbd_finalinput)

    cbd_finalout=cbd_output(cbd_out,predict_cbd)

    ab_cbd_input, ab_cbd_out=create_ab_cbd_input()

    ab_cbd_finalinput=rearrange_input_ab_cbd(ab_cbd_input)

    predict_ab_cbd=ab_cbd_model(ab_cbd_df,ab_cbd_finalinput)
    ab_cbd_finalout=ab_cbd_output(ab_cbd_out,predict_ab_cbd)

    result=final_output(cbd_finalout, ab_cbd_finalout)

    out=output_csv(result)

    print(out)
