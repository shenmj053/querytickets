##Installation
+ download the `/ticket` directory to your work directory
+ create a virtualenv in `/ticket`
+ activate the virtualenv
+ install dependencies to make the complete copy with following:

      pip install -r requirements.txt

+ run the development server:

      python tickets.py

##How to use API
1. API uri: http://localhost:5000?purpose_codes=ADULT

2. request url param: `Date`, `from` and `to` are required, while `change` is optional, with the formats `2016-08-20`, `北京`, `杭州`, `上海`

3. you can use the api as followed:

       import requests

       # 
       url = 'http://localhost:5000/zd?purpose_codes=ADULT&Date=2016-08-13&from=北京&to=杭州'
       # or url = 'http://localhost:5000/hc?purpose_codes=ADULT&Date=2016-08-15&from=北京&to=杭州&change=上海'
        
       req = request.get(url)
       contents = req.json()
       if contents:
            print(contents)
            
##Framework and Library
Flask and Request are used because of their simplity and easy using.