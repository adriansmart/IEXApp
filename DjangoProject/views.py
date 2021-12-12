from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import pandas as pd
import requests as req
import json,urllib
from django.views.decorators.cache import never_cache
import sys
sys.path.append('/Users/adriansmart/DjangoEnv/mysite/mysite')
import ibkr

@never_cache
def index_entry(request):
    return render(request, 'chart.html')

def buy_stock(request):
    print("buy stock called")
    ticker = request.GET.get('ticker','')
    numShares = request.GET.get('shares','')
    ibkr.buy(ticker, numShares)   
    return HttpResponse("buy stock successful")

def get_news(request):
    ticker = request.GET.get('ticker','')
    url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/news/last/1?token="
    news = req.get(url).json()
    return HttpResponse(news)

def get_price(ticker):
    url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/price?token="
    price = req.get(url)
    return price

@never_cache
def get_company_stats(request):
    ticker = request.GET.get('ticker','')
    outDict = {}  
    # market cap
    url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/stats/marketcap?token="
    outDict['marketCap'] = req.get(url).text

    # employees
    url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/stats/employees?token="
    outDict['employees'] = req.get(url).text

    # next dividend date
    url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/stats/nextDividendDate?token="
    outDict['nextDivDate'] = req.get(url).text

    # ex-dividend date
    url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/stats/exDividendDate?token="
    outDict['exDivDate'] = req.get(url).text

    # 1 year change
    url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/stats/year1ChangePercent?token="
    outDict['yrChange'] = req.get(url).text

    # dividend yield
    url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/stats/dividendYield?token="
    outDict['divYield'] = req.get(url).text

    # convert Dictionary to json string
    str = json.dumps(outDict)
    return HttpResponse(str)

@never_cache
def update_price(request):
    ticker = request.GET.get('ticker','')
    price = get_price(ticker)
    return HttpResponse(price)
