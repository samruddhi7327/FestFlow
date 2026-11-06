from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector, os
app=Flask(__name__); app.secret_key=os.getenv("SECRET_KEY","festflow-demo")
def db():
 return mysql.connector.connect(host=os.getenv("DB_HOST","localhost"),user=os.getenv("DB_USER","root"),password=os.getenv("DB_PASSWORD","YOUR_MYSQL_PASSWORD"),database=os.getenv("DB_NAME","fest_db"))
def allrows(q,p=()):
 c=db(); k=c.cursor(dictionary=True); k.execute(q,p); r=k.fetchall(); k.close(); c.close(); return r
@app.route("/")
def home():
 try:
  stats={x:allrows(q)[0]["n"] for x,q in {"students":"SELECT COUNT(*) n FROM STUDENT","events":"SELECT COUNT(*) n FROM FEST_EVENT","registrations":"SELECT COUNT(*) n FROM REGISTRATION","pending":"SELECT COUNT(*) n FROM PAYMENT WHERE payment_status='Pending'"}.items()}
  recent=allrows("SELECT e.event_name,e.event_date,COUNT(r.registration_id) registrations FROM FEST_EVENT e LEFT JOIN REGISTRATION r ON e.event_id=r.event_id GROUP BY e.event_id,e.event_name,e.event_date ORDER BY e.event_date LIMIT 5")
  return render_template("home.html",stats=stats,recent=recent)
 except Exception as e: return render_template("error.html",message=str(e))
@app.route("/events")
def events():
    try:
        query = """
        SELECT
            e.event_id,
            e.event_name,
            e.event_date,
            e.event_time,
            e.registration_fee,
            e.max_participants,
            v.venue_name,
            COUNT(r.registration_id) AS registered_count,
            GREATEST(
                e.max_participants - COUNT(r.registration_id), 0
            ) AS available_seats
        FROM FEST_EVENT e
        JOIN VENUE v ON e.venue_id = v.venue_id
        LEFT JOIN REGISTRATION r
            ON e.event_id = r.event_id
            AND r.registration_status = 'Registered'
        GROUP BY
            e.event_id,
            e.event_name,
            e.event_date,
            e.event_time,
            e.registration_fee,
            e.max_participants,
            v.venue_name
        ORDER BY e.event_date
        """

        event_list = allrows(query)

        return render_template(
            "events.html",
            events=event_list
        )

    except Exception as e:
        return render_template("error.html", message=str(e))
@app.route("/students")
def students():
 try: return render_template("students.html",students=allrows("SELECT student_id,student_name,email,department,year_of_study FROM STUDENT ORDER BY student_id"))
 except Exception as e: return render_template("error.html",message=str(e))
@app.route("/register",methods=["GET","POST"])
def register():
 if request.method=="POST":
  c=None; k=None
  try:
   c=db(); k=c.cursor(); k.execute("INSERT INTO REGISTRATION (student_id,event_id,registration_date,registration_status) VALUES (%s,%s,CURDATE(),'Registered')",(request.form["student_id"],request.form["event_id"])); c.commit(); flash("Registration saved successfully.","success")
  except Exception as e: flash(str(e),"danger")
  finally:
   if k: k.close()
   if c: c.close()
 try:
  return render_template("register.html",students=allrows("SELECT student_id,student_name FROM STUDENT ORDER BY student_name"),events=allrows("SELECT event_id,event_name FROM FEST_EVENT ORDER BY event_date"),registrations=allrows("SELECT r.registration_id,s.student_name,e.event_name,r.registration_date,r.registration_status FROM REGISTRATION r JOIN STUDENT s ON r.student_id=s.student_id JOIN FEST_EVENT e ON r.event_id=e.event_id ORDER BY r.registration_id DESC"))
 except Exception as e: return render_template("error.html",message=str(e))
@app.route("/payments")
def payments():
 try: return render_template("payments.html",payments=allrows("SELECT p.payment_id,s.student_name,e.event_name,p.amount,p.payment_method,p.payment_status FROM PAYMENT p JOIN REGISTRATION r ON p.registration_id=r.registration_id JOIN STUDENT s ON r.student_id=s.student_id JOIN FEST_EVENT e ON r.event_id=e.event_id ORDER BY p.payment_id DESC"))
 except Exception as e: return render_template("error.html",message=str(e))
if __name__=="__main__": app.run(debug=True)
