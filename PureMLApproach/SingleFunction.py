from random import randrange
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from numpy import NaN
def Predictor(trainfile,testfile):
    data_test = pd.read_csv(testfile)
    data_train=pd.read_csv(trainfile)


    enc = OneHotEncoder(dtype = float)
    overs = [[i] for i in range(1, 21)]
    enc.fit(overs)

    def drop_feature(df):
        return df.drop(["batting_team", "ball", "bowler",
                        "batsman", "dismissal_kind", "fielder",
                        "bowling_team", "non_striker"
                        ], axis = 1)
    test = drop_feature(data_test)
    train=drop_feature(data_train)
    #For test data
    matchid=124
    cum_run=[]
    m=[]
    sum=0
    count1=1
    for i in range(len(test)):
        if test['match_id'][i]!=matchid:
            matchid=test['match_id'][i]
            try:
                sum=test['total_runs'][i]
                count1=1
            except:
                continue
            cum_run.append(sum)
            m.append(count1)
        else:
            sum+=test['total_runs'][i]
            count1+=1
            cum_run.append(sum)
            m.append(count1)
    test['cum_run']=cum_run
    test['balls']=m
    matchid=1
    cum_run=[]
    m=[]
    runrate=[]
    wickets=[]
    count2=[]
    sum=0
    count1=1
    op=0
    count6=0
    count5=0
    randomfactor=randrange(48,60)
    count8=0
    testes=[]
    for i in range(len(train)):
        if op<randomfactor and count8==0:
            op+=1
            count6+=train['total_runs'][i]
            if type(train['player_dismissed'][i])==str:
                count5+=1
        if op==randomfactor:
            op=0
            testes.append(randomfactor)
            randomfactor=randrange(48,60)
            wickets.append(count5)
            runrate.append(6*count6/count1)
            count5=0
            count6=0
            count8=1
        if train['match_id'][i]!=matchid:
            count8=0
            matchid=train['match_id'][i]
            count2.append(sum)
            try:
                sum=train['total_runs'][i]
                count1=1
            except:
                continue
            cum_run.append(sum)
            m.append(count1)
        else:
            sum+=train['total_runs'][i]
            count1+=1
            cum_run.append(sum)
            m.append(count1)
    count2.append(sum)
    train['cum_run']=cum_run
    train['balls']=m
    sampledf=pd.DataFrame()
    sampledf['Balls']=testes
    sampledf['wickets']=wickets
    sampledf['runrate']=runrate
    feature=sampledf.to_numpy()
    label=[]
    for i in range(len(count2)):
        label.append([count2[i]])
    model=DecisionTreeRegressor(max_depth=15)
    model.fit(feature,label)
    matchid=124
    count3=[]
    count4=[]
    count5=0
    m=[]
    id=[matchid]
    for i in range(len(test)):
        if type(test['player_dismissed'][i])==str:
            count5+=1
    if matchid!=test['match_id'][i]:
        count3.append(count5)
        count9=count5
        count5=0
        count4.append(test['balls'][i-1])
        matchid=test['match_id'][i]
        m.append(6*test['cum_run'][i-1]/test['balls'][i-1])
        id.append(matchid)
    count3.append(count9)
    count4.append(test['balls'][i])
    m.append(6*test['cum_run'][len(test)-2]/test['balls'][len(test)-2])
    sampledf2=pd.DataFrame()
    sampledf2['Balls']=count4
    sampledf2['wickets']=count3
    sampledf2['runrate']=m    
    feat=sampledf2.to_numpy()
    count10=model.predict(feat)
    sampledf3=pd.DataFrame()
    sampledf3['match_id']=id
    sampledf3['prediction']=count10
    sampledf3.to_csv('mnq.csv')
