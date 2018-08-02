#!/usr/bin/pyton
from __future__ import division

from datadog import initialize, api
import json
import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig()

class Org:
	name = ""
	hostCount = 0
	containerCount = 0
	apiKey = ""
	appKey = ""


def getHostData(aApiKey, aAppKey):
	dateS = datetime.now() - timedelta(hours = 36)
	startDate = str(dateS.strftime('%Y-%m-%dT%H'))
#	print(startDate)
	dateS = datetime.now() - timedelta(hours = 35)
	endDate = str(dateS.strftime('%Y-%m-%dT%H'))
#	print(endDate)

	r = requests.get("https://app.datadoghq.com/api/v1/usage/hosts?api_key="+aApiKey+"&application_key="+aAppKey+"&start_hr="+startDate+"&end_hr="+endDate)
	return r.json()


def storeHostDataInOrg(aOrg,aData):
	print(aData)
	if len(aData["usage"]) > 0:
#		print(aData["usage"][0]["host_count"])
		aOrg.hostCount = aData["usage"][0]["host_count"]
		aOrg.containerCount = aData["usage"][0]["container_count"]

def sendMetricToDD(aMainName,aApiKey, aAppKey, aMetricName, aNum):
	options = {
        'api_key': aApiKey,
        'app_key': aAppKey
        }

        initialize(**options)

	print("Sending to [" + aMainName + "], Metric ["+aMetricName+"] Value ["+str(aNum)+"]")

	api.Metric.send(metric=aMetricName, points=aNum)

orgs = []

with open("hostInfo.txt", "r") as filestream:
        for line in filestream:
            currentline = line.split(",")
	    org = Org()
	    org.name = currentline[0].rstrip()
	    org.apiKey = currentline[1].rstrip()
	    org.appKey = currentline[2].rstrip()
	    orgs.append(org)

mainOrgName = orgs[0].name
mainOrgApiKey = orgs[0].apiKey
mainOrgAppKey = orgs[0].appKey

totalHosts = 0
totalContainers = 0

i=0
while i < len(orgs):
	storeHostDataInOrg(orgs[i],dict(getHostData(orgs[i].apiKey, orgs[i].appKey)))
	totalHosts = totalHosts+ orgs[i].hostCount
	totalContainers = totalContainers+ orgs[i].containerCount
	i+=1

print("Total Hosts ["+str(totalHosts)+"]")

i=0
while i < len(orgs):
	print("**************************************")
	print(orgs[i].name + " Hosts ["+str(orgs[i].hostCount)+"] Containers ["+str(orgs[i].containerCount)+"]")
	sendMetricToDD(mainOrgName,mainOrgApiKey, mainOrgAppKey,orgs[i].name+".total.hosts",orgs[i].hostCount)
	sendMetricToDD(mainOrgName,mainOrgApiKey, mainOrgAppKey,orgs[i].name+".total.containers",orgs[i].containerCount)
	i+=1

sendMetricToDD(mainOrgName,mainOrgApiKey, mainOrgAppKey,"tc.all.hosts.active",totalHosts)
sendMetricToDD(mainOrgName,mainOrgApiKey, mainOrgAppKey,"tc.all.containers.active",totalContainers)


