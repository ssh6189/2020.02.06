#얘는 계속 실행이 되어야 해서, jupyter notebook에서는 안된다.
#이걸 하는 목적 : dialog flow로부터 데이터를 받아, 여기서 처리한 후 다시 dialog flow로 반환
#그걸 위해서는 json으로 리턴해야 한다.

import requests
import urllib
import IPython.display as ipd
import json
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify


#Flask 객체 생성
app = Flask(__name__)

#가상폴더 개념
#'데코레이터'라고 한다. 특정 함수가 호출할때, 앞뒤로 감싸는것, 클래스에 선언된 route다. 브라우저에 입력한것을 home에 넣어준다.
#잘 몰라도, 웹어플리케이션을 쉽게 만들도록 해준다.

#챗봇적용
cnt = 0 #전역변수로 해야 누적이 된다.

@app.route('/')

def home():
    html = """
    <h1>Hello</h1>
    <img src = /static/image.jpg>
    <br>
    <iframe
    allow="microphone;"
    width="350"
    height="430"
    src="https://console.dialogflow.com/api-client/demo/embedded/ssh_chatbot">
</iframe>
    """
    return html

#수를 이미지로 표시   
    
@app.route('/counter')

def counter():
    global cnt
    cnt = cnt + 1
    
    ###""" """ 부분은 없어도 된다.
    """
    html = ""
    for i in str(cnt):
            html = html + f"<img src = /static/{i}.png width=32>"
    html =  html + "명이 방문했습니다."
        
    """
    html = "".join([f"<img src=/static/{i}.png width=32>" for i in str(cnt)])
    html = html + "명이 방문했습니다."
                    
    return html
    #cnt를 이미지로 출력


@app.route('/weather')

def weather():
    city = request.args.get("city")
    return f"{city} 날씨 좋아요."


#def home():
    #return "hello----<img src = image.jpg />" #이것만 치면, 문자만 호출된다.
    #이건, 우리가 동적으로 html을 생성한것이다.
#    return "hello----<img src = /static/image.jpg />" #반드시 폴더명을  static이라고 해야한다.



if __name__ == '__main__':
    #host = 0.0.0.0에는 실제 ip를 넣어주면 된다. 0.0.0.0은 ip를 모르더라도 접속할 수 있다. 원래는 자기 ip를 써야 한다.
    #그럴때, 쓸 수 있는게 0.0.0.0, 127.0.0.1 두가지를 사용할 수 있다.
    app.run(host='0.0.0.0', port = 3000, debug=True)
   