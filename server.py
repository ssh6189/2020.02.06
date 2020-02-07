#얘는 계속 실행이 되어야 해서, jupyter notebook에서는 안된다.
#이걸 하는 목적 : dialog flow로부터 데이터를 받아, 여기서 처리한 후 다시 dialog flow로 반환
#그걸 위해서는 json으로 리턴해야 한다.

import requests
import urllib
import IPython.display as ipd
import json
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import pickle

def getWeather(city) :    
    url = "https://search.naver.com/search.naver?query="
    url = url + urllib.parse.quote_plus(city + "날씨")
    print(url)
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    temp = bs.select('span.todaytemp')    
    desc = bs.select('p.cast_txt')    
    #dictionery가 좋은 리턴방식이다.
    return {"temp":temp[0].text, "desc":desc[0].text} #temp가 온도, desc가 어제보다 4도 낮아요.
    #return {"temp":temp[4+7].text, "desc":desc[0].text} #dctionery방식으로 하면, 이런식으로, 수정할때 용이하다.

    #return temp[0].text + "/" + desc[0].text #리턴 값을 문자열로 준다.

def getQuery(word):
    url = "https://search.naver.com/search.naver?where=kdic&query="
    url = url + urllib.parse.quote_plus(word)
    print(url)
    
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    output = bs.select('p.txt_box')
    
    return [node.text for node in output]
    #return output[0].text

def processDialog(req) :
    
    answer = req['queryResult']['fulfillmentText']
    intentName = req['queryResult']['intent']['displayName'] 
    
    if intentName == 'query' :
        word = req["queryResult"]['parameters']['any'] 
        text = getQuery(word)[0]                
        res = {'fulfillmentText': text}   
    else :
        res = {'fulfillmentText': answer}           
        
    return res

#Flask 객체 생성
app = Flask(__name__)

@app.route('/') #'데코레이터'라고 한다. 특정 함수가 호출할때, 앞뒤로 감싸는것, 클래스에 선언된 route다. 브라우저에 입력한것을 home에 넣어준다.
#잘 몰라도, 웹어플리케이션을 쉽게 만들도록 해준다.
def home():
    
    name = request.args.get("name")
    item = request.args.get("item")
    return "hello"#호출할때, 반드시 name이라는 파라미터를 호출해야한다.

@app.route('/abc')#데코레이터'라고 한다. 특정 함수가 호출할때, 앞뒤로 감싸는것, 클래스에 선언된 route다. 브라우저에 입력한것을 home에 넣어준다.
#잘 몰라도, 웹어플리케이션을 쉽게 만들도록 해준다.
def abc():
    return "test"

@app.route('/weather')#데코레이터'라고 한다. 특정 함수가 호출할때, 앞뒤로 감싸는것, 클래스에 선언된 route다. 브라우저에 입력한것을 home에 넣어준다.
#잘 몰라도, 웹어플리케이션을 쉽게 만들도록 해준다.

def weather():
    city = request.args.get("city")
    info = getWeather(city)
    
   #return "<font color=red>" + info["temp"] + "도 " + info["desc"] + "</font>"
   #return info #웹표준방식이 아니어서, 안된다.
   #return json.dumps(info)
    return jsonify(info)

#어떤 요청이 들어와도, 무조건, Hello만 리턴하는 서버
#GET방식으로도, POST방식으로도 호출 가능하게 한것, 서비스 할때는, GET방식을 빼준다.
#GET방식은 디버깅할때 사용, 공인 서버가 아니다 보니까, dialog가 우리서버를 호출할 수 없다.

#단어검색기능
@app.route('/dialogflow', methods=['GET', 'POST'])
def dialogflow():
    req = request.get_json(force=True) #강제로, json파일로 변환
    print(json.dumps(req, indent=4, ensure_ascii=False))
    
    answer = req['queryResult']['fulfillmentText']
    intentName = req['queryResult']['intent']['displayName']
    
    if intentName == 'query':
        word = req["queryResult"]['parameters']['any']
        text = getQuery(word)[0]
        res = {"fulfillmentText":text}
    else:
        res = {"fulfillmentText":answer}
    
   # res = {'fulfillmentText':'Hello~~~'}   
    return jsonify(res)
    
    #dialogflow에서 만든 규약을 지켜서 return을 해야한다. json파일로 해야한다.

@app.route('/dialogflowp', methods=['POST', 'GET'])
def dialogflowp():
    
    if request.method == 'GET' :
        file = request.args.get("file")        
        with open(file, encoding='UTF8') as json_file:
            req = json.load(json_file)    
            print(json.dumps(req, indent=4, ensure_ascii=False))            
    else :
        req = request.get_json(force=True)    
        print(json.dumps(req, indent=4, ensure_ascii=False))    
    
    
    return  jsonify(processDialog(req))
    

#날씨검색기능
@app.route('/dialogflowweather', methods=['GET', 'POST'])
def dialogflowweather():
    req = request.get_json(force=True) #강제로, json파일로 변환
    print(json.dumps(req, indent=4, ensure_ascii=False))
    
    answer = req['queryResult']['fulfillmentText']
    intentName = req['queryResult']['intent']['displayName']
    
    if intentName == 'query':
        word = req["queryResult"]['parameters']['any']
        text = getWehather(word)[0]
        res = {"fulfillmentText":text}
    else:
        res = {"fulfillmentText":answer}
    
   # res = {'fulfillmentText':'Hello~~~'}   
    return jsonify(res)
    
    #dialogflow에서 만든 규약을 지켜서 return을 해야한다. json파일로 해야한다.
    
    
    
if __name__ == '__main__':
    #host = 0.0.0.0에는 실제 ip를 넣어주면 된다. 0.0.0.0은 ip를 모르더라도 접속할 수 있다. 원래는 자기 ip를 써야 한다.
    #그럴때, 쓸 수 있는게 0.0.0.0, 127.0.0.1 두가지를 사용할 수 있다.
    app.run(host='0.0.0.0', port = 3000, debug=True)