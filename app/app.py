from flask import Flask, render_template, request, send_from_directory
import requests
import json 

app = Flask(__name__)

@app.route('/')

def test(productName=None):
    return render_template('index.html', productName=productName)

@app.route('/basic',methods=['POST'])
def basic(productName=None):
###################폼을 받아보자
    #return render_template('index.html', productName=productName)

    productName = request.form['productName']
    #추천컨셉은 여러개 입력가능
    productConcept = request.form.getlist('productConcept[]')
    productTopN = request.form['productTopN']
    print("productName : ",productName)
    print("productConcept : ",productConcept)
    print("productTopN : ",productTopN)
   # return productName 

#################### 연관식품추천API 연동테스트
    headers = {'Content-Type': 'application/json; chearset=utf-8'}
    url = 'https://dtresearch.cj.net/api/recom/food'  
    jsonInput = {
        #"product": "쁘띠첼 워터젤리사과",
        "product": productName,
        "userContext": 
          #  {"concept": ["다이어트"]},
            {"concept": productConcept },
        #"topn": "3"
        "topn": productTopN
        }

    response = requests.post(url, json=jsonInput, headers=headers) 

   #json.dumps() : python data (dict) -> json data (str)
    json_string = json.dumps(response.json(), ensure_ascii=False)

    #결과값 파싱
    #json.loads() : json data (str) -> python data (dict)
    jsonObject = json.loads(json_string)
    jsonArray = jsonObject.get("resultData")
    #resultlen = len(resultData)
    
    #print("len : ",len(jsonArray))
    if jsonArray is not None:
        for resultData in jsonArray :
            #product = resultData.get("product")
            print("resultData : ",resultData)
            #product = resultData["product"]
            #imgurl = 'http://'+ resultData.get("imgurl")

    return render_template("index.html", content=json_string, productName = productName, productConcept = productConcept, productTopN = productTopN, jsonArray= jsonArray) 



#######################################################################################################################3


@app.route('/recipe')
def tab(productName=None):
    return render_template('recipe.html')

@app.route('/recipe',methods=['POST'])
def recipe(productName=None):
    productName = request.form['productName']
    #식재료, 추천컨셉은 여러개 입력가능
    ingredientName = request.form.getlist('ingredientName[]')
    productConcept = request.form.getlist('productConcept[]')
    productTopN = request.form['productTopN']
    print("productName : ",productName)
    print("productConcept : ",productConcept)
    print("productTopN : ",productTopN)
   # return productName 

#################### 연관레시피추천API 연동테스트
    headers = {'Content-Type': 'application/json; chearset=utf-8'}
    url = 'https://dtresearch.cj.net/api/recom/recipe'  
    jsonInput = {
        #"product": "백설 안달루시아산 올리브유",
        "product": productName,
        "userContext": 
          {
            "ingredient": ingredientName,
            "concept": productConcept
            },
        "topn": productTopN,
        "option": {
            "ingredient_ratio": "0.2"
            }
        }

    response = requests.post(url, json=jsonInput, headers=headers) 

   #json.dumps() : python data (dict) -> json data (str)
    json_string = json.dumps(response.json(), ensure_ascii=False)

    #결과값 파싱
    #json.loads() : json data (str) -> python data (dict)
    jsonObject = json.loads(json_string)
    jsonArray = jsonObject.get("resultData")
    #resultlen = len(resultData)
    
    #print("len : ",len(jsonArray))
    if jsonArray is not None:
        for resultData in jsonArray :
            #product = resultData.get("product")
            #print("resultData : ",resultData)
            print(productName)
            #print(resultData.get("relatedProduct"))
    return render_template("recipe.html", content=json_string, productName = productName, productConcept = productConcept, productTopN = productTopN, ingredientName = ingredientName, jsonArray= jsonArray) 


@app.route('/img/<path:file>', methods=['GET', 'POST'])
def image(file):
   return send_from_directory(directory='img',filename=file)


if __name__ == '__main__':
    app.run(debug=True)
