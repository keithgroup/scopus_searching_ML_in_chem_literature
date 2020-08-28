import requests
import json
import urllib
import pandas as pd


def make_df(request):
    
    df = pd.DataFrame(columns=['title'])
    
    for r in request['search-results']['entry']:
        
        df = df.append({'title': r['prism:publicationName']},
                      ignore_index=True)
        
    return df


def make_request(query, apiKey, start=0, view='STANDARD'):
    
    query_str = urllib.parse.urlencode({"query": query, "apiKey": apiKey,
                                        "start": start, "view": view})
    url_str = "https://api.elsevier.com/content/search/scopus?{0}".format(query_str)
    #print(requests.get(url_str))
    request = requests.get(url_str).json()
    
    return request


def get_all_results(query, apiKey, start=0, results_per_page=25):
    
    results_found = results_per_page
    df = pd.DataFrame()
    
    while results_found == results_per_page:
        
        request = make_request(query, apiKey, start)
        df2 = make_df(request)
        df = pd.concat([df, df2])
        
        results_found = len(request['search-results']['entry'])
        start += results_per_page
        print(start)
        
    return df