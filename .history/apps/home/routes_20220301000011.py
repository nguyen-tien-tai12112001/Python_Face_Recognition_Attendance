# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from itertools import count
from sqlalchemy import func
from sched import scheduler
from unittest import result
from apps import db, login_manager
from apps.home import blueprint
from flask import render_template, redirect, request, url_for, Response
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.forms import CreateClass, CreateStudent,CreateSchedule, CreateSubject, CreateTeacher
from apps.authentication.models import  ClassMember, Schedule, Students, Subject, Teachers,Users,Class, Attendance
from apps.authentication.forms import EditAccountForm
import datetime
from sqlalchemy import cast, Date, extract, null
import hashlib
import binascii
import os

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')
@blueprint.route('/add-schedule.html', methods=['GET', 'POST'])
@login_required
def add_schedule():
    segment = get_segment(request)
    create_schedule_form = CreateSchedule(request.form)
    if'add_schedule' in request.form:
        mgv=request.form['info-gv']
        subjectId=request.form['info-subject']
        classId=request.form['info-class']
        c=int(classId.split('-')[0])
        s=int(subjectId.split('-')[0])
        g=mgv.split('-')[0]
        startDate=request.form['startDate']
        endDate=request.form['endDate']
        schedule = Schedule(mgv=g,subjectId=s,startDate=startDate,endDate=endDate,classId=c)
        db.session.add(schedule)
        db.session.commit()
        return redirect('/list-schedule.html')
    listGv=Teachers.query.all()
    listCl=Class.query.all()
    listSub=Subject.query.all()
    return render_template('home/schedule/add-schedule.html', segment=segment,listGv=listGv,listCl=listCl,listSub=listSub,form=create_schedule_form)

@blueprint.route('/add-student.html', methods=['GET', 'POST'])
@login_required
def add_student():
    create_student_form = CreateStudent(request.form)
    segment = get_segment(request)
    if 'add_student' in request.form:
        msv=request.form['msv']
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        DOBs=request.form['DOBs']
        classes=request.form['classes']
        img=request.form['img']
        
        # check msv
        student = Students.query.filter_by(msv=msv).first()
        if student:
            return render_template('home/add-student.html',
                                   msg='Mã sinh viên đã tồn tại',
                                   success=False,
                                   form=create_student_form, segment=segment)
        # Check email exists
        student = Students.query.filter_by(email=email).first()
        if student:
            return render_template('home/add-student.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_student_form, segment=segment)

        student = Students(**request.form)
        db.session.add(student)
        db.session.commit()
        return render_template('home/add-student.html',
                               msg='Thêm sinh viên thành công',
                               success=True,
                               form=create_student_form, segment=segment)
    else:
        return render_template('home/add-student.html', form=create_student_form, segment=segment)
@blueprint.route('/edit_student/<string:msv>', methods=['GET', 'POST'])
@login_required
def edit_student(msv):
    create_student_form = CreateStudent(request.form)
    segment = get_segment(request)
    student = Students.query.filter_by(msv=msv).first()
    if 'edit_student' in request.form:
        msv=request.form['msv']
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        DOBs=request.form['DOBs']
        classes=request.form['classes']
        img=request.form['img']
        
       

        x=db.session.query(Students).filter_by(msv=msv).first()
        x.msv=msv
        x.name=name
        x.phone=phone
        x.email=email
        x.DOBs=DOBs
        x.classes=classes
        x.img=img
        db.session.commit()
        return render_template('home/edit-student.html',
                               msg='Sửa thông tin sinh viên thành công',
                               success=True,
                               form=create_student_form, segment=segment,student=student)
    else:
        
        return render_template('home/edit-student.html', form=create_student_form, segment=segment,student=student)

@blueprint.route('/list-student.html', methods=['GET', 'POST'])
@login_required
def list_student():
    segment = get_segment(request)
    return render_template('home/list-student.html', rows=Students.query.all(), segment=segment)
#Class
@blueprint.route('/class/<int:id>/add-student', methods=['GET', 'POST'])
def add_student_to_class(id):
    segment = get_segment(request)
    if 'add_student' in request.form:
       msv=request.form['msv']
       item = ClassMember.query.filter_by(msv=msv,classId=id).first()
       print(item)
       print('haha')
       if item!=null:
        now=datetime.datetime.now()
        classmember= ClassMember(msv=msv,classId=id,joined_date=now.isoformat())
        db.session.add(classmember)
        db.session.commit()
        
    if 'find_student' in request.form:
        msv=request.form['msv']
        student=Students.query.filter_by(msv=msv).first()
        return render_template('home/class/add-student.html', idClass=id, segment=segment,student=student)
    return render_template('home/class/add-student.html', idClass=id, segment=segment,student=null)

@blueprint.route('/add-class.html', methods=['GET', 'POST'])
@login_required
def add_class():
    create_class_form = CreateClass(request.form)
    segment = get_segment(request)
    if 'add_class' in request.form:
        item = Class(**request.form)
        db.session.add(item)
        db.session.commit()
        return redirect('list-class.html')
    else:
        return render_template('home/class/add-class.html', form=create_class_form, segment=segment)


@blueprint.route('/list-class.html', methods=['GET', 'POST'])
@login_required
def list_class():
    segment = get_segment(request)
  
    return render_template('home/class/list-class.html', rows=Class.query.all(), segment=segment)
# Subject
@blueprint.route('/list-subject.html', methods=['GET', 'POST'])
@login_required
def list_subject():
    segment = get_segment(request)
    return render_template('home/subject/list-subject.html', rows=Subject.query.all(), segment=segment)
@blueprint.route('/add-subject.html', methods=['GET', 'POST'])
@login_required
def add_subject():
    create_class_form = CreateSubject(request.form)
    segment = get_segment(request)
    if 'add_subject' in request.form:
        item = Subject(**request.form)
        db.session.add(item)
        db.session.commit()
        return redirect('list-subject.html')
    else:
        return render_template('home/subject/add-subject.html', form=create_class_form, segment=segment)
# Teacher
@blueprint.route('/add-teacher.html', methods=['GET', 'POST'])
@login_required
def add_teacher():
    create_class_form = CreateTeacher(request.form)
    segment = get_segment(request)
    if 'add_teacher' in request.form:
        item = Teachers(**request.form)
        db.session.add(item)
        db.session.commit()
        return redirect('list-teacher.html')
    else:
        return render_template('home/teacher/add-teacher.html', form=create_class_form, segment=segment)
@blueprint.route('/list-teacher.html', methods=['GET', 'POST'])
@login_required
def list_teachers():
    segment = get_segment(request)
   
    return render_template('home/teacher/list-teacher.html', rows=Teachers.query.all(), segment=segment)

# Schedule
class ItemSchedule(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    classId= db.Column(db.Integer)
    className=db.Column(db.String(50))
    subjectName=db.Column(db.String(50))
    teacheName=db.Column(db.String(150))
    dateStart=db.Column(db.String(50))
    dateEnd=db.Column(db.String(50))
    def __init__(self,id,classId,className,subjectName,teacheName,dateStart,dateEnd):
        self.id=id
        self.classId=classId
        self.className=className
        self.subjectName=subjectName
        self.teacheName=teacheName
        self.dateStart=dateStart
        self.dateEnd=dateEnd

@blueprint.route('/list-schedule.html', methods=['GET', 'POST'])
@login_required
def list_schedule():
    segment = get_segment(request)
    schedules=Schedule.query.all()
    items=[]
    for event in schedules:
        itemClass= Class.query.filter_by(id=event.classId).first()
        itemSubject=Subject.query.filter_by(id=event.subjectId).first()
        itemTeacher=Teachers.query.filter_by(mgv=event.mgv).first()
        itemSchedule= ItemSchedule(id=event.id,classId=itemClass.id,className=itemClass.name,subjectName=itemSubject.name,teacheName=itemTeacher.fullname,dateStart=event.startDate,dateEnd=event.endDate)
        items.append(itemSchedule)
    return render_template('home/schedule/list-schedule.html', rows=items, segment=segment)



def DeleteStudent(msv):
    sv=Students.query.filter_by(msv=msv).first()
    db.session.delete(sv)
    db.session.commit()
@blueprint.route('/delete_student/<string:msv>')
@login_required
def delete_student(msv):
    DeleteStudent(msv)
    return redirect(url_for('home_blueprint.list_student'))

@blueprint.route('/info_class', methods=['GET', 'POST'])
@login_required
def info_class():
    return

@blueprint.route('/attendance_check', methods=['GET', 'POST'])
@login_required
def attendance_check():
    return
class Summary(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    countJoin=db.Column(db.String(50))
    className= db.Column(db.String(50))
    studentName=db.Column(db.String(50))
    isPast=db.Column(db.Boolean())
    def __init__(self,className,studentName,count,isPast):
        self.studentName=studentName
        self.className=className
        self.count=count
        self.isPast=isPast
@blueprint.route('/summary_study', methods=['GET', 'POST'])
@login_required
def summary_study():
    segment = get_segment(request)
    totals=db.session.query(Attendance.scheduleId,Attendance.msv,func.count(Attendance.scheduleId)).group_by(Attendance.scheduleId).all()
    for i in totals:
     for a in i:
         print(a)
    #print(totals.scheduleId)
    
    return render_template('home/summary/summary.html', rows=totals, segment=segment)



@blueprint.route('/list-user', methods=['GET', 'POST'])
@login_required
def list_user():
    segment = get_segment(request)
    return render_template('home/list-account.html', rows=Users.query.all(), segment=segment)
def DeleteUser(id):
    sv=Users.query.filter_by(id=id).first()
    db.session.delete(sv)
    db.session.commit()
@blueprint.route('/delete_user/<int:id>')
@login_required
def delete_user(id):
    DeleteUser(id)
    return redirect(url_for('home_blueprint.list_user'))
@blueprint.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    create_student_form = EditAccountForm(request.form)
    segment = get_segment(request)
    user = Users.query.filter_by(id=id).first()
    if 'edit_user' in request.form:
        username=request.form['username']
        email=request.form['email']
        a=request.form['password']
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', a.encode('utf-8'),
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        password=(salt + pwdhash)
        role=request.form['role']

        x=db.session.query(Users).filter_by(id=id).first()
        x.username=username
        x.email=email
        x.password=password
        x.role=role
        db.session.commit()
        return render_template('home/edit-user.html',
                               msg='Sửa thông tin thành công',
                               success=True,
                               form=create_student_form, segment=segment,user=user)
    else:
        return render_template('home/edit-user.html', form=create_student_form, segment=segment,user=user)

@blueprint.route('/chart_analysis')
@login_required
def chart_analysis():
    return
@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
