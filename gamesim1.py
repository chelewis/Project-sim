# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 15:20:40 2020

@author: lewis
"""
import pandas as pd
import random as rand




"""Read Player dataset"""
players = pd.read_csv("Players.csv")
champions = pd.read_csv("Champions.csv")
playerChampionPools = pd.read_csv("PlayerChampionPools.csv")
teams = pd.read_csv("Teams.csv")
teamRosters = pd.read_csv("TeamRosters.csv")
tplayers = len(players.index)

"""Globals"""
LaneName = ["Top Lane","Jungle","Mid Lane","Bot Lane","Support"]


"""Classes"""
class MyPlayer:
    laneScore = 0
    ChampionPickID = -1
    
    def __init__(self,Id):
        
        self.comfortBuff = 0
        self.laneScore = 0
        self.ChampionPickID = -1
        self.ID = Id
        rec = players.loc[players['ID']==Id]
        self.name = rec.iloc[0].loc["Name"]
        self.role = rec.iloc[0].loc["Role"]
        self.age = rec.iloc[0].loc["Age"]
        self.aggr = rec.iloc[0].loc["aggr"]
        self.aware = rec.iloc[0].loc["aware"]
        self.pos = rec.iloc[0].loc["pos"]
        self.dmg = rec.iloc[0].loc["dmg"]
        self.cs = rec.iloc[0].loc["cs"]
        self.pool = playerChampionPools.loc[playerChampionPools['PlayerId']==Id]
        
        
    def SetComfort(self):
        pool = self.pool.iloc[0]
        if self.ChampionPickID == pool.loc["ChampionId1"]:
            self.comfortBuff = 50
            return
        
        if self.ChampionPickID == pool.loc["ChampionId2"] or pool.loc["ChampionId3"]:
            self.comfortBuff = 25
            return
        
        if self.ChampionPickID == pool.loc["ChampionId4"] or pool.loc["ChampionId5"]:
            self.comfortBuff = 10
            return
        
        self.comfortBuff = -10
        return
    
    
    def CheckComfort(self):
        pool = self.pool.iloc[0]
        if self.ChampionPickID == pool.loc["ChampionId1"]:
            print("On BEST(tier 1) pick")
            return
        
        if self.ChampionPickID == pool.loc["ChampionId2"] or pool.loc["ChampionId3"]:
            print("On COMFORT(tier 2) pick")
            return
        
        if self.ChampionPickID == pool.loc["ChampionId4"] or pool.loc["ChampionId5"]:
            print("On FAMILIAR(tier 3) pick")
            return
        
        print("Vunerable Pick")
        return
        
    
    def PrintStats(self):
        print("Name:",self.name)
        print("Age:",self.age)
        print("Champion Pool",self.pool)
        
    """Add CalculateLaneScore as a method within class instead"""
    
    """Lane diff can be implemented in here as a method that takes in another player object and subtracting lane scores"""


    
class MyTeam:
    
    
    def __init__(self,teamid,*Id):
        self.id = teamid
        self.name = (teams.loc[teams['ID']==teamid]).iloc[0].loc["Name"]
        self.roster = []
        self.teamComp = []
        self.bans = []
        self.towersTaken = 0
        self.dragsTaken = 0
        self.baronsTaken = 0
        self.rHeraldsTaken = 0
        self.totalTeamLaneScore = 0
        self.totalTeamGold = 2500
        self.golddiff = 0
        self.mvp = -1
        self.mvpId = -1
        self.mvpScore = 0
        
        for p in Id:
            """print("[DEBUG]p=",p)"""
            self.roster.append(MyPlayer(p))
            
    def printRoster(self):
        for p in self.roster:
            print(p.PrintStats())
    
    def SetChampionPicks(self,*champIds):
        i=0
        for c in champIds:
            self.roster[i].ChampionPickID = c
            self.roster[i].SetComfort()
            i+=1
    
    def CalculateTeamLaneScores(self):
        for p in self.roster:
            p.laneScore = CalculateLaneScore2(p)
            self.totalTeamLaneScore += p.laneScore
            if p.laneScore >self.mvpScore:
                self.mvpScore = p.laneScore
                self.mvp = p.name
                self.mvpId = p.ID
    
    def GetPLayer(self,Id):
        for x in self.roster:
            if x.ID == Id:
                return x
        
        return -1
    

class MyChampion:
    def __init__(self,Id):
        rec = champions.loc[champions['Id']==Id]
        self.ID = Id
        self.Name = (champions.loc[champions['Id']==Id]).iloc[0].loc["Name"]
        self.Class = rec.iloc[0].loc["Class"]
        self.Difficulty = rec.iloc[0].loc["Difficulty"]
        self.DamageType = rec.iloc[0].loc["DamageType"]
        self.Damage = rec.iloc[0].loc["Damage"]
        self.Sturdiness = rec.iloc[0].loc["Sturdiness"]
        self.CC = rec.iloc[0].loc["Crowd-Control"]
        self.Mobility = rec.iloc[0].loc["Mobility"]
        self.Utility = rec.iloc[0].loc["Utility"]



"""********FUNCTION DEFINITIONS********"""
def CalculateLaneScore(*player):
    resultset = []
    for p in player:
        """roll player lane score(random number * stat factor)"""
        """p1LaneScore = (rand.randint(1,10)*players.loc[p,'aggr']) + (rand.randint(1,10) * players.loc[p,'aware']) + (rand.randint(1,10)*players.loc[p,'pos']) + (rand.randint(1,10)*players.loc[p,'dmg'])"""
        p1LaneScore = (rand.randint(1,10)*p.aggr) + (rand.randint(1,10) * p.aware) + (rand.randint(1,10)*p.pos) + (rand.randint(1,10)*p.dmg)
        resultset.append(p1LaneScore)

    return resultset


def CalculateLaneScore2(p):
    """roll player lane score(random number * stat factor)"""
    """p1LaneScore = (rand.randint(1,10)*players.loc[p,'aggr']) + (rand.randint(1,10) * players.loc[p,'aware']) + (rand.randint(1,10)*players.loc[p,'pos']) + (rand.randint(1,10)*players.loc[p,'dmg'])"""
    return (rand.randint(1,10)*p.aggr) + (rand.randint(1,10) * p.aware) + (rand.randint(1,10)*p.pos) + (rand.randint(1,10)*p.dmg) + p.comfortBuff
        
def CalculateLaneScoreTest(p):
    champ = MyChampion(p.ChampionPickID)
    champAggrSyn = (champ.Damage*30 + champ.Sturdiness*30 + champ.CC*10 + champ.Mobility*10 + champ.Utility*20)/200
    champAwrSyn = (champ.Damage*10 + champ.Sturdiness*30 + champ.CC*20 + champ.Mobility*10 + champ.Utility*30)/200
    champPosSyn = (champ.Damage*30 + champ.Sturdiness*20 + champ.CC*10 + champ.Mobility*30 + champ.Utility*10)/200
    champDmgSyn = (champ.Damage*40 + champ.Sturdiness*10 + champ.CC*10 + champ.Mobility*40 + champ.Utility*20)/200
    
    aggr = rand.randint(1,10) * p.aggr
    aware = rand.randint(1,10) * p.aware
    pos = rand.randint(1,10) * p.pos
    dmg = rand.randint(1,10)*p.dmg
    
    score = (aggr*champAggrSyn + aware*champAwrSyn + pos*champPosSyn + dmg*champDmgSyn)
    print('DEBUG',score)
    return  score + (score * p.comfortBuff)



"""DO NOT USE. OUTDATED METHOD FOR FUTURE REFERENCE ONLY"""
def CalculateLaneCSDiffs(laneScores,p1,p2):
    p1gold = (laneScores[0]*10) + p1.cs*10
    p2gold = (laneScores[1]*10) + p2.cs*10
    
    """part of original calculation in case absolute value returned is an issue"""
    """p1gdiff = p1gold - p2gold
    p2gdiff = p2gold - p1gold"""
    
    """gold differencial @ 15 minutes"""
    gdiff = abs(p1gold - p2gold)
    return gdiff

"""Takes lane scores and opposing lane players"""
def CalculateLaneCSDiffsAll(t1,t2):
    gdiffs = []
    for i in range(0,len(t1.roster)):
        p1 = t1.roster[i]
        p2 = t2.roster[i]
        p1gold = (p1.laneScore*10) + p1.cs*10
        p2gold = (p2.laneScore*10) + p2.cs*10
        gdiff = abs(p1gold - p2gold)
        gdiffs.append(gdiff)
    """part of original calculation in case absolute value returned is an issue"""

    
    """list of gold differencials @ 15 minutes"""    
    return gdiffs



def PrintMatchup(p1,p2):
    p1ChampName = (champions.loc[champions['Id']==p1.ChampionPickID]).iloc[0].loc["Name"]
    p2ChampName = (champions.loc[champions['Id']==p2.ChampionPickID]).iloc[0].loc["Name"]
    print("Lane Matchup:",p1.name,"as",p1ChampName,"VS",p2.name,"as",p2ChampName)
    
    
"""DO NOT USE. OUTDATED METHOD FOR FUTURE REFERENCE ONLY"""
def OutputResults(ls,p1,p2,diff):
    print(p1.name," got a lane score of ",p1.laneScore)
    print(p2.name," got a lane score of ",p2.laneScore)
    if p1.laneScore > p2.laneScore:
        print(p1.name," Has won the lane with a gold lead of ",diff)
    elif p2.laneScore > p1.laneScore:
        print(p2.name," Has won the lane with a gold lead of ",diff)
    else:
        print("The lane phase has ended even")
        


def OutputLaneResults(t1,t2,diff):
    
    for lane in range(0,len(t1.roster)):
        p1 = t1.roster[lane]
        p2 = t2.roster[lane]
        
        print(LaneName[lane],"==============================================")
        PrintMatchup(p1,p2)
        print(p1.name," got a lane score of ",p1.laneScore)
        print(p2.name," got a lane score of ",p2.laneScore)
        
        if p1.laneScore > p2.laneScore:
            print(p1.name," Has won the lane with a gold lead of ",diff[lane],"\n")
        elif p2.laneScore > p1.laneScore:
            print(p2.name," Has won the lane with a gold lead of ",diff[lane],"\n")
        else:
            print("The lane phase has ended even\n")
            

def PrintTeamStats(t1,t2):
    print(t1.name,"\t\t\t",t2.name)
    print(t1.teamComp,"\t\t\t",t2.teamComp)
    print(t1.towersTaken,"\t\t\t",t2.towersTaken)
    print(t1.dragsTaken,"\t\t\t",t2.dragsTaken)
    print(t1.baronsTaken,"\t\t\t",t2.baronsTaken)
    print(t1.totalTeamLaneScore,"\t\t\t",t2.totalTeamLaneScore)
    

def GetMVP(t1,t2):
    if t1.mvpScore > t2.mvpScore:
        return t1.mvp
    elif t2.mvpScore > t1.mvpScore:
        return t2.mvp
    else:
        return (t1.mvp," and",t2.mvp)

def PrintMVP(t1,t2):
    if t1.mvpScore > t2.mvpScore:
        plyr = t1.GetPLayer(t1.mvpId)
        print("Player of the Game:",t1.name,t1.mvp,"On",(champions.loc[champions['Id']==plyr.ChampionPickID]).iloc[0].loc["Name"])
    elif t2.mvpScore > t1.mvpScore:
        plyr = t2.GetPLayer(t2.mvpId)
        print("Player of the Game:",t2.name,t2.mvp,"On",(champions.loc[champions['Id']==plyr.ChampionPickID]).iloc[0].loc["Name"])
    else:
        print("No") 


def GetWinner(t1,t2):
    if t1.totalTeamLaneScore > t2.totalTeamLaneScore:
        return t1
    if t1.totalTeamLaneScore < t2.totalTeamLaneScore:
        return t2
    return t1

def PrintWinner(t1,t2):
    victor = GetWinner(t1,t2)
    print(victor.name,"Has Won the Match")
"""*************************************"""



"""**********MAIN RUN**********"""



"""Initialize teams and players"""
team1 = MyTeam(1,1,2,3,4,5)
team2 = MyTeam(2,6,7,8,9,10)

"""Set team champion picks"""
team1.SetChampionPicks(119,132,67,125,143)
team2.SetChampionPicks(110,113,69,8,16)

"""PrintMatchup(team1.roster[0],team2.roster[0])"""


"""Calculate all lane scores for team 1 and team 2"""
team1.CalculateTeamLaneScores()
team2.CalculateTeamLaneScores()


"""Calculate Lane Scores"""
goldDiffList = CalculateLaneCSDiffsAll(team1,team2)

"""Output lane phase results"""
OutputLaneResults(team1,team2,goldDiffList)

PrintTeamStats(team1,team2)
PrintWinner(team1,team2)
PrintMVP(team1,team2)

"""END"""