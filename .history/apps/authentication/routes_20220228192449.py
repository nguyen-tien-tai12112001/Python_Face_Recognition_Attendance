# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sqlalchemy import null
import schedule
import time
import io
import face_recognition
from PIL import Image, ImageDraw
from turtle import circle
import pandas as pd
import numpy as np
import datetime
import urllib.request
import cv2
from flask import render_template, redirect, request, url_for, Response, session
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from models.detector import face_detector
from models.verifier.face_verifier import FaceVerifier
from apps import db, login_manager
from apps.authentication import blueprint

from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import ClassMember, Users,Students,Class
from apps.authentication.util import verify_pass
from run import app
import tensorflow as tf
from keras.models import Sequential
from multiprocessing import Pool
import os
width, height = 220, 220
fontface=os.getcwd()+"/apps/authentication/haarcascade_frontalface_default.xml"
detector_faceTest = cv2.CascadeClassifier(fontface)
@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.attendance'))

#-------------------------------------------------------------------------------------
global fd
fd = face_detector.FaceAlignmentDetector(
    lmd_weights_path="./models/detector/FAN/2DFAN-4_keras.h5"# 2DFAN-4_keras.h5, 2DFAN-1_keras.h5
)
global fv
fv = FaceVerifier(classes=512, extractor = "facenet")
fv.set_detector(fd)
global students
students=Students.query.all()
global img_crop
global graph
graph = tf.compat.v1.get_default_graph()


def resize_image(im, max_size=768):
    if np.max(im.shape) > max_size:
        ratio = max_size / np.max(im.shape)
        print(f"Resize image to ({str(int(im.shape[1]*ratio))}, {str(int(im.shape[0]*ratio))}).")
        return cv2.resize(im, (0,0), fx=ratio, fy=ratio)
    return im
def addInfo_In(msv):
    return
    # with app.app_context():
    #     if (db.session.query(InfoClass).filter(InfoClass.msv==msv).count()%2==0):
    #         x = datetime.datetime.now()
    #         id=db.session.query(InfoClass).count()
    #         student = InfoClass(id+1,msv,x,'In')
    #         db.session.add(student)
    #         db.session.commit()
def addInfo_Out(msv):
    return
    # with app.app_context():
    #     if (db.session.query(InfoClass).filter(InfoClass.msv==msv).count()%2==1):
    #         x = datetime.datetime.now()
    #         id=db.session.query(InfoClass).count()
    #         student = InfoClass(id+1,msv,x,'Out')
    #         db.session.add(student)
    #         db.session.commit()
def Verifiert(im1,im2):
    global fv  
    with graph.as_default():
        result, distance = fv.verify(im1, im2, threshold=0.5, with_detection=False, with_alignment=False, return_distance=True)
    return result,distance
def VerifierStudent(student): 
    global fv  
    # print('1')
    url=student.img
    response = urllib.request.urlopen(url)
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    im_known = cv2.imdecode(image, cv2.IMREAD_COLOR)
    im_known = resize_image(im_known)
    kq=[]
    # result, distance=Verifiert(im_known,img_crop)
    # print('2')
    return kq
listStudents=[]
def getListStudentByClassId(classId):
    #members= Students
    #global listStudents
    members=ClassMember.query.all()
    #print(students)
    print(members.count(2))
    print('concac')
    students=Students.query.all()
    for member in members:
        print(member.msv)
    #print(members)
    return students

def gen_frames():
    global students
    global img_crop
    camera = cv2.VideoCapture(0)
    #camera.set(cv2.CAP_PROP_FPS, 5)
    num_people=1000
    
    stu_new=[]
    stu_old=[]
    stu_msv=['']
    while camera.isOpened():
        ret,img=camera.read()
        if ret:
            #imgS=cv2.resize(frame,(0,0),None,0.25,0.25)
            image_grey=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            # with graph.as_default():
            detected_faces = detector_faceTest.detectMultiScale(image_grey, scaleFactor=1.5, minSize=(30, 30))
            for (x, y, l, a) in detected_faces:
                image_face= cv2.resize(image_grey[y:y + a, x:x + l], (width, height))
                cv2.rectangle(img, (x, y), (x + l, y + a), (0, 0, 255), 2)
                cv2.cvtColor(image_face,cv2.COLOR_BGR2RGB)
                distance_test=10000
                name="Unknown"
                
                for student in listStudents:
                    url=student.img
                    print(url)
                    print('hahahahahhahahahaha')
                    response = urllib.request.urlopen(url)
                    image = np.asarray(bytearray(response.read()), dtype="uint8")
                    im_known = cv2.imdecode(image, cv2.IMREAD_COLOR)
                    im_known = resize_image(im_known)
                    result, distance=fv.verify(im_known, image_face, threshold=0.5, with_detection=False, with_alignment=False, return_distance=True)
                    if distance<1.0 :
                        name=student.msv
                        stu_msv.append(name)
                        distance_test=distance
                        if  (student.msv not in stu_msv):
                            addInfo_In(name)
                        break
                    name="Unknown"
                stu_new.append(name)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, name , (y + 6, x +25), font, 1.0, (5, 5, 255), 1)
                cv2.putText(img, str(round(distance_test,4)) , (y + 6, x -10), font, 1.0, (5, 5, 255), 1)
            for i in stu_old:
                if i not in stu_new:
                    addInfo_Out(i)
            stu_old=stu_new
            stu_new=[]
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
          
@blueprint.route('/end')
def end():
    for student in students:
        addInfo_Out(student.msv)
    return redirect(url_for('authentication_blueprint.login'))


#Time
schedule.every(5).seconds.do(redirect('/attendance'))
schedule.every(10).seconds.do(redirect('/index'))
schedule.every().day.at("07:30").do(redirect('/attendance'))

# while True:
#     schedule.run_pending()
#     time.sleep(1)

@blueprint.route('/attendance/class/<int:id>')
def attendance(id):
    global listStudents
    listStudents=getListStudentByClassId(id)
    print(listStudents.count(2))
    print('haha')
       #return redirect('/index')
    return render_template('/face_recognition/face.html',classId=id)
@blueprint.route('/video_feed/<int:id>')
def video_feed(id):
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


RED = (255, 0, 0)
GREEN = (0, 255, 0)
SIZE = 500
HALF_SIZE = 250

#-------------------------------------------------------------------------------------

# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('home_blueprint.index'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register.html', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        photo = request.form['photo']
        
        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/profile')
def profile():
    return render_template('accounts/profile.html',user=current_user)
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))




@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
