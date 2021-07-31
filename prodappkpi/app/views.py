from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from io import StringIO
import pandas as pd
from .models import ProdAppKPiModel
import json
from random import randrange
import datetime

#For History Maintainces
hist_dict = {}
# Create your views here.
#Home page access, and default Running page
def index(request):
    #Getting Request time and updating to the Dictionary
    ctime = datetime.datetime.now()
    hist_dict.update({ctime:'Home Page'})
    return render(request,'index.html',{})
#Uploading the jtl file from Web browser and processing it
def JtlUploadAction(request):
    if request.method == 'POST':
        ctime = datetime.datetime.now()
        hist_dict.update({ctime: 'File Upload'})
        ProdAppKPiModel.objects.all().delete()
        jtl_file = request.FILES['file']
        data_set = jtl_file.read().decode('UTF-8')
        #print(type(data_set))
        TESTDATA = StringIO(data_set)
        df = pd.read_csv(TESTDATA, sep=",")
        for index, row in df.iterrows():
            ProdAppKPiModel.objects.create(
                timeStamp=row['timeStamp'], elapsed=row['elapsed'], label=row['label'], responseCode=row['responseCode'], responseMessage=row['responseMessage'], threadName=row['threadName'], dataType=row['dataType'], success=row['success'], failureMessage=row['failureMessage'],
                bytes=row['bytes'], sentBytes=row['sentBytes'], grpThreads=row['grpThreads'], allThreads=row['allThreads'], URL=row['URL'], Latency=row['Latency'], IdleTime=row['IdleTime'], Connect=row['Connect']
            )
        return render(request,'dashboard.html',{})
#Accessing the data for pivot element, for Graph Visulazation
def pivot_data(request):
    dataset = ProdAppKPiModel.objects.all()
    data = serializers.serialize('json', dataset)
    ctime = datetime.datetime.now()
    hist_dict.update({ctime: 'KPI Graphs'})
    #it sending the Json Response
    return JsonResponse(data, safe=False)
#view the data from web browser, the data will be displayed in the html tabular format
def dataView(request):
    ctime = datetime.datetime.now()
    hist_dict.update({ctime: 'Data View'})
    dataset = ProdAppKPiModel.objects.all()
    from django_pandas.io import read_frame
    df = read_frame(dataset)
    df = df.to_html
    return render(request, 'viewData.html', {'df':df})
#View the kpi graphs with flexmonster
def KPI(request):
    return render(request, 'dashboard.html', {})
#Generating user definded graphs
def graphs(request):
    """
        Function responsible for rendering the homepage
        """
    ctime = datetime.datetime.now()
    hist_dict.update({ctime: 'Chart generated'})
    # h_var : The title for horizontal axis
    h_var = 'Latency'

    # v_var : The title for horizontal axis
    v_var = 'elapsed'

    # data : A list of list which will ultimated be used
    # to populate the Google chart.
    data = [[h_var, v_var]]
    dataset = ProdAppKPiModel.objects.all()
    from django_pandas.io import read_frame
    df = read_frame(dataset)
    #labels = df['label'].value_counts()
    lbl = []
    for idx, name in enumerate(df['label'].value_counts().index.tolist()):
        lbl.append([name, df['label'].value_counts()[idx]])
    threadName = []
    for idx, name in enumerate(df['threadName'].value_counts().index.tolist()):
        threadName.append([name, df['threadName'].value_counts()[idx]])

    for index, row in df.iterrows():
        data.append([int(row['Latency']),int(row['elapsed'])])
    data.pop(0)
    elpgrpthread = []
    for index, row in df.iterrows():
        elpgrpthread.append([int(row['elapsed']),int(row['grpThreads'])])

    elapsCommit = []
    for index, row in df.iterrows():
        elapsCommit.append([int(row['elapsed']), int(row['Connect'])])
    elapsCommit.pop(0)

    latencyConnect= []
    for index, row in df.iterrows():
        latencyConnect.append([int(row['Latency']), int(row['Connect'])])
    latencyConnect.pop(0)
    # h_var_JSON : JSON string corresponding to  h_var
    # json.dumps converts Python objects to JSON strings
    h_var_JSON = json.dumps(h_var)
    # v_var_JSON : JSON string corresponding to  v_var
    v_var_JSON = json.dumps(v_var)
    modified_data = json.dumps(data)
    # dictiory shown below so that they can be displayed on the home screen
    return render(request, "gengraphs.html", {'lbl':lbl,'threadName':threadName,'values': modified_data, 'data':data, 'elpgrpthread':elpgrpthread,'elapsCommit':elapsCommit,'latencyConnect':latencyConnect,
                                           'h_title': h_var_JSON, 'v_title': v_var_JSON})
def historyView(request):
    return render(request,'historyview.html',{'hist':hist_dict})
