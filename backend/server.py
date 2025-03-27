from flask import Flask, request, jsonify
from flask_cors import CORS
import os 
import json
import requests
from urllib.parse import urlencode


app = Flask(__name__)
CORS(app)

def build_query(query_string,filters=None,sort=None,start=0,rows=10,fields=None,df=None):
    params = {
        'q': query_string,
        'start': start,
        'rows': rows,
        'fl': fields,
        'fq': filters,
        'df': df
    }

    if filters:
        for filter in filters:
            params["fq"] = filter
    if sort:
        params["sort"] = sort
    if fields:
        params["fl"] = ",".join(fields)
    if df:
        params["df"] = df

    query_string = urlencode(params)
    return f"{REQUEST_URL}{query_string}"

CONTAINER_NAME = 'news'
REQUEST_URL = 'http://solr:8983/solr/news/select?'


def make_request(query):
    response = requests.get(query)
    return response.json()

@app.route('/query', methods=['POST'])
def query():
    try:
        print("Incoming request data:", request.json)
        
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        text = data.get('query')
        if not text:
            return jsonify({"error": "No query provided"}), 400
        
        params = {
            'defType': "edismax",
            'fl': "title author url date",
            "indent": "true",
            'q': text,
            'q.op': "OR",
            'qf': "title^2 contents^1.1 tags^4 entities^3"
        }
        
        query_string = urlencode(params)
        encoded_url = f"{REQUEST_URL}{query_string}"
        
        print("Solr request URL:", encoded_url)
        
        response = requests.get(encoded_url)
        
        print("Solr response status:", response.status_code)
        print("Solr response content:", response.text)
        
        response_json = response.json()
        
        if len(response_json) > 0:
            return jsonify(response_json), 200
        else:
            return jsonify({"error": "No results found"}), 404
        
    except Exception as e:
        print("Error occurred:")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



    