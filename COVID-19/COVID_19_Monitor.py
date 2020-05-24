from flask import Flask, render_template,request
import requests
import pylab
import json
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.rc('figure', max_open_warning = 0)


app = Flask(__name__)
@app.route('/data', methods=['POST', 'GET'])
def data():
    country = request.form.get("country")
    Type= request.form.get("Type")
    Visual=request.form.get("Show Data")
    payload = {'country': country}
    URL = 'https://api.statworx.com/covid'
    response = requests.request("POST", url=URL, data=json.dumps(payload))
    df = pd.DataFrame.from_dict(json.loads(response.text))
    if Visual == "Show Data":
        return render_template('result.html', data = {str(country): df[str(Type)].values} )
    elif Visual == "Plot Data":
        fig = plt.figure(figsize=(6, 4))
        plt.plot(df[str(Type)], 'mo')
        fig.suptitle(str(country))
        plt.xlabel("Number of days since 1/1/2020")
        plt.ylabel(str(Type))
        URl='static/imgs/'+str(country)+str(Type)+'.png'
        img = plt.savefig(URl)
        return render_template('result_plot.html', url = URl)
    elif Visual == "Find R0":
        #for the plotting
        x=[]
        for i in range (len(df['cases'])):
            x.append(i)   
        x = pylab.array(x)
        yV=np.log(df['cases'])
        Y=[]
        for y in yV:
            if y==np.NINF:
                y=0
                Y.append(y)
            else:
                y=y
                Y.append(y)
        Y = pylab.array(Y)
        #for the calculation
        xVals=[]
        fig = pylab.figure(figsize=(6, 4))
        yVals=[]
        for i in df["cases"]:
            if i != 0 :
                yVals.append(i)
        yVals = pylab.array(yVals)
        yVals = np.log10(yVals)
        xVals = np.arange(len(yVals))
        A=np.vstack([xVals,np.ones(len(xVals))]).T
        m,c=np.linalg.lstsq(A,yVals,rcond=None)[0]
        R0=10**(m*6)
        model = pylab.polyfit(x, Y, 1)
        pylab.plot(np.log(df['cases']),  'mo', label = 'log Daily Cases')
        pylab.plot(x, pylab.polyval(model, x), 'r--', label = 'Linear Model')
#        estYVals = pylab.polyval(model, xVals)
#        dx=np.diff(xVals)
#        dy=np.diff(estYVals)
#        slope=dy/dx
#        R0=10**(slope[0]*6)
        fig.suptitle(str(country)+',R0='+str(R0))
        plt.xlabel("Number of days since 1/1/2020")
        plt.ylabel("log[n(t)]")
        pylab.legend(loc = 'best')
        Url='static/imgs/'+str(country)+'R0.png'
        img = pylab.savefig(Url)
        return render_template('R0.html', url = Url)
        

@app.route('/', methods=['GET'])
def Home_Page():
    return render_template('Home Page.html')



if __name__ == '__main__':
    app.run()