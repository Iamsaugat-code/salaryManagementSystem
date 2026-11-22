
from flask import flash,Flask,jsonify,render_template,redirect,request,session,url_for,Response
import mysql.connector
import math
import re

app = Flask(__name__)
app.secret_key = "iamsalarymanagementmember"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home",methods=["GET"])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    con = mysql.connector.connect(
                host ='localhost',
                user ='root',
                password ='password',
                database ='salarymanagement'
            )
    cursor = con.cursor()
    try:
        cursor.execute("select count(*) from salarytype")
        total_st = cursor.fetchone()[0]
        cursor.execute("select count(*) from employees")
        total_em = cursor.fetchone()[0]
    finally:
        cursor.close()
        con.close()
    return render_template("home.html",total_st=total_st,total_em=total_em)

@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] ='no-store'
    return response

@app.context_processor
def user_found():
    username = session.get("username")
    return {"current_user":username}

@app.route("/logined",methods=["GET","POST"])
def checklogin():
    con = mysql.connector.connect(
        host ='localhost',
        user ='root',
        password ='password',
        database ='salarymanagement'
    )
    cursor = con.cursor()
    try:
        if request.method =='POST': 
            username = request.form.get("named","").strip()    
            password = request.form.get("password","").strip()        
            if not all([username,password]):        
                flash("please fill the field first !","error")        
                return redirect(url_for("checklogin"))        
            cursor.execute("select count(*) from useraccounts where username =%s and password =%s",(username,password))    
            result = cursor.fetchone()[0]    
            if result==0:        
                flash("Try again !","error")        
                return redirect(url_for("checklogin"))    
            session["username"] = username    
            return redirect(url_for('home'))
    except mysql.connector.Error as e:
        flash(" Mysql Connection error ","error")
        return redirect(url_for("checklogin")) 
    finally:
        cursor.close()
        con.close()   
    
    return render_template("login.html")


# add salary types
@app.route("/salarytypes",methods=["GET"])
def salary_types():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("salarytypes.html")

@app.route("/addsalary",methods =["GET","POST"])
def add_salary():
    con = mysql.connector.connect(
            host ='localhost',
            user ='root',
            password ='password',
            database ='salarymanagement'
        )
    cursor = con.cursor()
    try:
        if request.method =='POST':
            salary = request.form.get("salary","").strip()
            amount = float(request.form.get("amount","").strip())
            username = session.get("username")
            
            if not all([salary,amount]):
                flash("please fill the feild","error")
                return redirect(url_for('addsalary'))
            
            cursor.execute("select count(*) from salarytype where typesname =%s",(salary,))
            data = cursor.fetchone()[0]
            if data >=1:
                flash("already added salary types","error")
                return render_template("salarytypes.html")
               
            cursor.execute("insert into salarytype (typesname,salary,username) values (%s,%s,%s)",(salary,amount,username))
            con.commit()
            flash(f"salarytypes added suceesfully ! ","success")
            return redirect(url_for('add_salary'))
            
    finally:
        cursor.close()
        con.close()
    return render_template("salarytypes.html")


# relate to employee view type 
@app.route("/showemp",methods =["GET","POST"])
def show_emp():
    if 'username' not in session:
        return redirect(url_for('login'))
    con = mysql.connector.connect(
                    host ='localhost',
                    user ='root',
                    password ='password',
                    database ='salarymanagement'
                )
    cursor = con.cursor()
    try:
        page = request.args.get("page",1,type=int)
        per_page = 7
        if page <1:
            page=1
        offset = (page-1)*per_page
        cursor.execute("select count(*) from employees")
        total_em = cursor.fetchone()[0]
        total_page = max(1,math.ceil(total_em/per_page))
        cursor.execute("select * from employees limit %s offset %s",(per_page,offset))
        data = cursor.fetchall()
    except mysql.connector.Error as e:
        print("database connection error ")
        return redirect(url_for('show_emp'))
    finally:
        cursor.close()
        con.close()
    return render_template("showemp.html",results = data,page=page,total_page=total_page,offset=offset)

# edit employees data
@app.route("/showeditEmp/<int:emp_id>")
def edit_emp(emp_id):
    if 'username' not in session:
        return redirect(url_for('login'))
        
    con = mysql.connector.connect(
                    host ='localhost',
                    user ='root',
                    password ='password',
                    database ='salarymanagement'
                )
    cursor = con.cursor()
    try:
        cursor.execute("select fullname,phone,gmail,gender,salaryt from employees where emp_id = %s",(emp_id,))
        data = cursor.fetchone()
        cursor.execute("select typesname  from salarytype")
        results = cursor.fetchall()
    except mysql.connector.Error as e:
            print("database connection error ")
            return redirect(url_for('emp_id'))
    finally:
        cursor.close()
        con.close()
        
    return render_template("editemp.html",data = data,emp_id=emp_id,results=results)  

# update the employee
@app.route("/updateEmp",methods =["GET","POST"])
def update_emp():
    con = mysql.connector.connect(
                    host ='localhost',
                    user ='root',
                    password ='password',
                    database ='salarymanagement'
                )
    cursor = con.cursor()
    try:
        if request.method =="POST":
            emp_id = request.form.get("emp_id","").strip()
            emp_name = request.form.get("named","").strip()
            email = request.form.get("email","").strip()
            phone = request.form.get("phone","").strip()
            gender = request.form.get("gender","").strip()
            salaryt = request.form.get("salarytypes","").strip()
            username = session.get("username")
            
            cursor.execute("select fullname,phone,gmail,gender,salaryt from employees where emp_id = %s",(emp_id,))
            data = cursor.fetchone()
            cursor.execute("select typesname  from salarytype")
            results = cursor.fetchall()
            
            if not all([emp_id,emp_name,email,phone,gender,salaryt,username]):
                flash("please the fill the all fields ! ","error")
                return render_template("editemp.html",results=results,data=data,emp_id=emp_id)
    
            if len(phone) <10:
                flash("enter valid 10 digit number !") 
                return render_template("editemp.html",results=results,data=data,emp_id=emp_id)
 
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                flash("Enter a valid email address", "error")
                return render_template("editemp.html",results=results,data=data,emp_id=emp_id)

            
            cursor.execute("update employees set fullname =%s,phone =%s,gmail=%s,gender =%s,salaryt=%s,addby =%s where emp_id =%s",(emp_name,phone,email,gender,salaryt,username,emp_id))
            con.commit()
            return redirect(url_for('show_emp'))
            
    except mysql.connector.Error as e:
        flash("database connection error ","error")
        return redirect(url_for('update_emp'))
    finally:
        cursor.close()
        con.close()
    return render_template("editemp.html")


# delete the employees 

@app.route("/deletemp/<int:emp_id>")
def delete_emp(emp_id):
    con = mysql.connector.connect(
                    host ='localhost',
                    user ='root',
                    password ='password',
                    database ='salarymanagement'
                )
    cursor = con.cursor()
    try:
        cursor.execute("delete from employees where emp_id=%s",(emp_id,))
        con.commit()
    except mysql.connector.Error as e:
        flash("database connection error ","error")
        return redirect(url_for('emp_id',emp_id=emp_id))
    finally:
        cursor.close()
        con.close()
    
    return redirect(url_for('show_emp'))
    
#  relate to salary type view
@app.route("/showstypes",methods=["GET","POST"])
def show_stypes():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    con = mysql.connector.connect(
                host ='localhost',
                user ='root',
                password ='password',
                database ='salarymanagement'
            )
    cursor = con.cursor()
    try:
        page = request.args.get("page",1,type=int)
        if page <1:
            page=1
        per_page =7
        offset = (page - 1)*per_page
        cursor.execute("select count(*) from salarytype")
        total_data = cursor.fetchone()[0]
        total_page = max(1,math.ceil(total_data/per_page))
        cursor.execute("select * from salarytype order by salary desc limit %s offset %s",(per_page,offset))
        data = cursor.fetchall()
    except mysql.connector.Error as e:
        print("database connection error ")
        return redirect(url_for('show_stypes'))
    finally:
        cursor.close()
        con.close()
    return render_template("showsalarytypes.html",results = data,total_page=total_page,offset=offset,page=page)

# delete the salary types
@app.route("/deleteStypes/<int:st_id>")
def d_salarytypes(st_id):
    if 'username' not in session:
            return redirect(url_for('login'))
        
    con = mysql.connector.connect(
                    host ='localhost',
                    user ='root',
                    password ='password',
                    database ='salarymanagement'
                )
    cursor = con.cursor()
    try:
        cursor.execute("delete from salarytype where st_id = %s",(st_id,))
        con.commit()
    except mysql.connector.Error as E:
        print("mysql connection error ")
        return redirect(url_for('d_salarytypes',st_id = st_id))
    finally:
        cursor.close()
        con.close()
    return redirect(url_for('show_stypes'))

# edit the salary types
@app.route("/editstypes/<int:st_id>")
def e_salarytypes(st_id):
    if 'username' not in session:
            return redirect(url_for('login'))
        
    con = mysql.connector.connect(
                    host ='localhost',
                    user ='root',
                    password ='password',
                    database ='salarymanagement'
                )
    cursor = con.cursor()
    try:
        cursor.execute("select typesname,salary from salarytype where st_id =%s",(st_id,))
        data = cursor.fetchone()
        s_type = data[0]
        s_amt =data[1]
        
        if not data:
            flash("id is not available")
            return redirect(url_for('e_salarytypes',st_id=st_id))
            
    except Exception as e:
        flash("something is wrong !","error")
        return redirect(url_for('e_salarytypes',st_id=st_id))             
        
    finally:
        cursor.close()
        con.close()
    
    return render_template("editstypes.html",s_type=s_type,s_amt=s_amt,st_id=st_id)
    
# update the salary types
@app.route("/updatest",methods =["GET","POST"])
def update_st():
    con = mysql.connector.connect(
                        host ='localhost',
                        user ='root',
                        password ='password',
                        database ='salarymanagement'
                    )
    cursor = con.cursor()
    try:
        if request.method =='POST':
            salary = request.form.get("salary","").strip()
            amount = float(request.form.get("amount","").strip())
            st_id = int(request.form.get("st_id","").strip())
            username = session.get("username")
            
            print(salary,amount,username,st_id)
            if not all([salary,amount,st_id]):
                flash("please fill all feild or no value is available","error")
                return redirect(url_for('update_st'))             

                        
            cursor.execute("update salarytype set typesname =%s,salary =%s,username=%s where st_id =%s",(salary,amount,username,st_id))
            con.commit()
                        
            return redirect(url_for('show_stypes'))
    except Exception as e:
        flash("something is wrong !","error")
        return redirect(url_for('update_st'))             
                    
    finally:
        cursor.close()
        con.close()
    return render_template("editstypes.html")


# paid salary 
@app.route("/paidsalary")
def paid_salary():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    con = mysql.connector.connect(
                                    host ='localhost',
                                    user ='root',
                                    password ='password',
                                    database ='salarymanagement'
                                )
    cursor = con.cursor()
    try:
        cursor.execute("select fullname from employees")
        data = cursor.fetchall()
    finally:
        cursor.close()
        con.close()
    
    return render_template("pay.html",results =data)
    

# select btn of paid employee

@app.route("/listemp",methods =["GET","POST"])
def employe_list():
    con = mysql.connector.connect(
                                        host ='localhost',
                                        user ='root',
                                        password ='password',
                                        database ='salarymanagement'
                                    )
    cursor = con.cursor()
    try:
        cursor.execute("select fullname from employees")
        data = cursor.fetchall()
        if request.method=='POST':
            emp_name = request.form.get("employee","").strip()
            if not emp_name:
                return render_template("pay.html",results = data)
            cursor.execute("select salaryt from employees where fullname = %s",(emp_name,))
            emp_type = cursor.fetchone()[0]
            cursor.execute("select salary from salarytype where typesname =%s",(emp_type,))
            emp_salary = cursor.fetchone()[0]              
            return render_template("pay.html",results = data,emp_type=emp_type,emp_salary=emp_salary,emp_name=emp_name)
    finally:
        cursor.close()
        con.close()
    return render_template("pay.html")
    

# paid employee
@app.route("/paidemps",methods =["GET","POST"])
def paid_emps():
    con = mysql.connector.connect(
                                            host ='localhost',
                                            user ='root',
                                            password ='password',
                                            database ='salarymanagement'
                                        )
    cursor = con.cursor()
    try:
        if request.method =="POST":
            emp_name = request.form.get("emp_name","").strip()
            emp_type = request.form.get("salaryt","").strip()
            months = request.form.get("month","")
            from_date = request.form.get("from_date","")
            to_date = request.form.get("to_date","")
            tax_amt = request.form.get("pay_tax","")
            save_amt = request.form.get("save_amt","")
            a_salary = request.form.get("actual_salary","")
            
            if not all([emp_name,emp_type,months,from_date,to_date,tax_amt,save_amt,a_salary]):
                flash(" please filled the field ","error")
                return redirect(url_for('paid_salary'))

            
            cursor.execute("insert into payments (employee,salaryt,months,from_date,to_date,tax_amt,save_amt,paid_amt)values (%s,%s,%s,%s,%s,%s,%s,%s)",(emp_name,emp_type,months,from_date,to_date,tax_amt,save_amt,a_salary))
            con.commit()
            flash(f"Salary is successfully paid to {emp_name} ","success")
            return redirect(url_for('paid_salary'))
    
    finally:
        cursor.close()
        con.close()
    
    return render_template("pay.html")

# view salary payment 

@app.route("/viewpaid")
def view_paid():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    con = mysql.connector.connect(
                                    host ='localhost',
                                    user ='root',
                                    password ='password',
                                    database ='salarymanagement'
                                )
    cursor = con.cursor()
    try:
        page = request.args.get("page",1,type=int)
        if page <1:
            page=1
        per_page = 7
        offset = (page-1)*per_page
        cursor.execute("select count(*) from payments")
        tatal_data = cursor.fetchone()[0]
        total_page = max(1,math.ceil(tatal_data/per_page))
        
        cursor.execute("select * from payments limit %s offset %s",(per_page,offset))
        data = cursor.fetchall()
    finally:
        cursor.close()
        con.close()    
    
    return render_template("viewpaid.html",results = data,page=page,offset=offset,total_page=total_page)            
    
    
# add employee to in the system
    
@app.route("/addemp")
def add_employe():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    con = mysql.connector.connect(
                                host ='localhost',
                                user ='root',
                                password ='password',
                                database ='salarymanagement'
                            )
    cursor = con.cursor()
    try:
        cursor.execute("select typesname  from salarytype")
        data = cursor.fetchall()
    finally:
        cursor.close()
        con.close()
    return render_template("addemp.html",results = data)

@app.route("/addemptodb",methods =["GET","POST"])
def addingemp():
    con = mysql.connector.connect(
                                    host ='localhost',
                                    user ='root',
                                    password ='password',
                                    database ='salarymanagement'
                                )
    cursor = con.cursor()
    cursor.execute("select typesname  from salarytype")
    data = cursor.fetchall()
    try:
        if request.method =="POST":
            fullname = request.form.get("named","").strip()
            email = request.form.get("email","").strip()
            phone = str(request.form.get("phone","").strip())
            gender = request.form.get("gender","").strip()
            salary_types = request.form.get("salarytypes","").strip()
            f = request.files['image']
            image = f.read()
            username = session.get('username')
            
            
            if not all([fullname,email,phone,gender,salary_types,image,username]):
                flash("fill field first !","error")
                return render_template("addemp.html",results = data)
            
            if len(phone) <10:
                flash("enter valid 10 digit number !") 
                return render_template("addemp.html",results = data)

            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                flash("Enter a valid email address", "error")
                return render_template("addemp.html",results = data)
            
            cursor.execute("insert into employees (fullname,phone,gmail,gender,salaryt,img,addby) values(%s,%s,%s,%s,%s,%s,%s)",(fullname,phone,email,gender,salary_types,image,username))
            con.commit()
            
            flash(f"employee {fullname} added successfully !","success")
            return redirect(url_for('add_employe'))
    except mysql.connector.Error as e:
        flash("database connection error","error")
        return render_template("addemp.html",results = data)

    finally:
        cursor.close()
        con.close()
    
    return render_template("addemp.html",results = data)
        
   
    
if __name__ =='__main__':
    app.run(debug=True)