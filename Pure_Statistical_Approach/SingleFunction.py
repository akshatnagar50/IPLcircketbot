import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
def Predict(trainfile,testfile):
  data_test = pd.read_csv(testfile)
  enc = OneHotEncoder(dtype = float)
  overs = [[i] for i in range(1, 21)]
  enc.fit(overs)
  def drop_feature(df):
      return df.drop(["batting_team", "ball", "bowler",
                      "batsman", "dismissal_kind", "player_dismissed", "fielder",
                      "bowling_team", "non_striker"
                      ], axis = 1)
  test = drop_feature(data_test)
  matchid=124
  cum_run=[]
  m=[]
  sum=0
  hehe=1
  for i in range(len(test)):
    if test['match_id'][i]!=matchid:
      matchid=test['match_id'][i]
      try:
        sum=test['total_runs'][i]
        hehe=1
      except:
        continue
      cum_run.append(sum)
      m.append(hehe)
    else:
      sum+=test['total_runs'][i]
      hehe+=1
      cum_run.append(sum)
      m.append(hehe)
  test['cum_run']=cum_run
  test['balls']=m
  matchid=124
  m=[]
  id=[matchid]
  for i in range(len(test)):
    if matchid!=test['match_id'][i]:
      matchid=test['match_id'][i]
      m.append(20*6.4*test['cum_run'][i-1]/test['balls'][i-1])
      id.append(matchid)
  m.append(20*6.4*test['cum_run'][len(test)-2]/test['balls'][len(test)-2])
  dafaq=pd.DataFrame()
  dafaq['match_id']=id
  dafaq['prediction']=m
  dafaq.to_csv('predicted.csv')
