from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///employees.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# schema of app db
class Employee(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(500), nullable=False)
    manager = db.Column(db.String(500), nullable=False)
    office = db.Column(db.String(500), nullable=False)
    joining_date = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} , {self.name}, {self.role}, {self.mobile}, {self.manager}, {self.office}, {self.joining_date}"

# home page
@app.route('/')
@app.route('/home')
def home():
    result = []
    for row in Employee.query.all():
        emplyee_data_row = (row.sno, row.name, row.role, row.mobile, row.manager, row.office, row.joining_date)
        result.append(emplyee_data_row)

    current_date = datetime.now().date()
    dict_by_date = {}
    for emplyee_data_row in result:
        join_date = emplyee_data_row[6].split('-')
        
        # get name of the month by number
        month_num = join_date[1]
        datetime_object = datetime.strptime(month_num, "%m")
        full_month_name = datetime_object.strftime("%B")
        
        # get number of months from current month
        join_date_to_int = [int(i) for i in join_date]
        start_date = datetime(join_date_to_int[0], join_date_to_int[1], join_date_to_int[2])
        num_months = (current_date.year - start_date.year) * 12 + (current_date.month - start_date.month)
        
        # key -> num_months, value -> employee data row 
        if num_months in dict_by_date.keys():
            dict_by_date[num_months].append((emplyee_data_row[1], emplyee_data_row[2], emplyee_data_row[3],
            emplyee_data_row[4], emplyee_data_row[5],
            join_date[2]+' '+full_month_name+' '+join_date[0][2:]+' ('+str(num_months)+' months ago)'))
        else:
            dict_by_date[num_months] = [(emplyee_data_row[1], emplyee_data_row[2], emplyee_data_row[3],
            emplyee_data_row[4], emplyee_data_row[5],
            join_date[2]+' '+full_month_name+' '+join_date[0][2:]+' ('+str(num_months)+' months ago)')]
    
    # sorting data by dict keys
    result.clear()
    for key in sorted(dict_by_date.keys()):
        if len(dict_by_date[key]) == 1:
            result.append(dict_by_date[key][0])
        else:
            for tuple in dict_by_date[key]:
                result.append(tuple)
    
    return render_template("home.html", allTodo= result)

# add page
@app.route('/add')
def add():
    return render_template("add.html")

# get request form data and insert into app employee db
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        name = request.form['inputName']
        role = request.form['inputRole']
        mobile = request.form['inputMobile']
        manager = request.form['inputManager']
        office = request.form['inputOffice']
        jd = request.form['inputJD']
        employee = Employee(name=name, role=role, mobile=mobile, manager=manager, office=office, joining_date=jd)
        db.session.add(employee)
        db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
