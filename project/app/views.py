from flask import Flask, jsonify,request
import json

from datetime import datetime,timedelta
from datetime import date
from app import app
from app import scheduler
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4


def generate_pdf(user_id,json_obj):
    json_obj=json.loads(json_obj)
    c=canvas.Canvas("../question_"+str(user_id)+"_suggestion.pdf",pagesize=letter)
    y=750
    i=1
    c.setTitle("Similar questions")
    for value in json_obj.values():
        c.drawString(100,y,"Q."+str(i)+" "+value)
        y=y-20
        i=i+1
    #c.showPage()
    c.save()
    #scheduler.remove_job(str(user_id))
    
def job(user_id,json_obj):    
    generate_pdf(user_id,json_obj)
   

@app.route("/api/<user_id>",methods=['POST'])
def suggested_question_pdf(user_id):
    data=request.data
    
    data = data.decode('utf8').replace("'", '"')
    run_time = datetime.now() + timedelta(0,5)
    if data is None or data=='':
        return jsonify({'code':400,"message":"data is unavailable","status":'failed'})
    try:
        json_obj=json.loads(data)
    except Exception as e:
        print(e)
        return jsonify({'code':400,"message":"Invalid data only json data accepted","status":'failed'})    
    job_exist=scheduler.get_job(user_id)
    if job_exist is None:
       scheduler.add_job(job, 'date', run_date=run_time, id=str(user_id),kwargs={'user_id':user_id,'json_obj':data})
    else:
       scheduler.remove_job(str(user_id))
       scheduler.add_job(job, 'date', run_date=run_time, id=str(user_id),kwargs={'user_id':user_id,'json_obj':data})   
    return jsonify({'code':200,"result":[],"status":'success'})

    
