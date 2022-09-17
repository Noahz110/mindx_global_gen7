from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy.orm import sessionmaker
from models.model import Base, engine, User, Resume


app = Flask(__name__)


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    Session = sessionmaker(bind = engine)
    sess = Session()
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            return redirect(url_for('admin'))
            # error = 'Invalid Credentials. Please try again.'
        else:
            u = sess.query(User).filter(User.name == request.form['username']).first()
            if not request.form['username'] or not request.form['password']:
                error = 'username or password is invalid. Please try again.'
                return render_template('login.html', error=error)
            if not u:
                error = 'User are not exist. Please try again.'
                return render_template('login.html', error=error)
            elif u.password != request.form['password']:
                error = 'Password is incorrect. Please try again.'
                return render_template('login.html', error=error)
            else:
                return redirect("user/{}".format(u.id))

    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    Session = sessionmaker(bind = engine)
    sess = Session()
    error = None
    if request.method == 'POST':
        c = sess.query(User).filter(User.name == request.form['username']).count()
        if c:
            error = 'User already exist. Please try again.'
            return render_template('signup.html', error=error)
        if not request.form['username'] or not request.form['password']:
            error = 'username or password is invalid. Please try again.'
            return render_template('signup.html', error=error)
        else:
            user = User(name = request.form['username'], password = request.form['password'])
            sess.add(user)
            sess.commit()

            return redirect(url_for('login'))
    return render_template('signup.html', error=error)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    Session = sessionmaker(bind = engine)
    sess = Session()
    error = None
    users = sess.query(User).all()

    lines = []
    # result = "<h1>List Open Jobs</h1><ul>"
    result = "<ul>"
    order = 1
    for user in users:
        resumes = user.resumes
        u = '''{0}. User name: {1}'''.format(order, user.name)
        idx = 1
        user_res = []
        for res in resumes:
            r = '''<p><small><a href='/resume/{1}'>CV_{0}</a>
            </small>
            </p>'''.format(idx, res.id)
            idx += 1
            user_res.append(r)
        # resumes = sess.query(Resume).filter(User.id == user.id).all()
        lines.append(u + "<br>".join(user_res))
        order += 1
    result = result + "<br>" + "<br>".join(lines) + "</ul>"
    format_result = '''
                <html lang="en">
                <head>
                <title>resume</title>
                </head>
                <body>
                <h2 style="text-align: center;">Admin page resume website</h2>
                {}
                </body>
                </html>'''.format(result)
    return format_result
    # return render_template('admin.html', error=error)

@app.route("/user/<int:user_id>")
def user(user_id):
    Session = sessionmaker(bind = engine)
    sess = Session()
    user = sess.query(User).filter(User.id == int(user_id)).first()
    resumes = [r.id for r in user.resumes]
    return render_template(
        'user.html',
        user_name=user.name,
        resumes=resumes
    )

@app.route("/addcv")
def addcv():
    Session = sessionmaker(bind = engine)
    sess = Session()
    user = sess.query(User).filter(User.id == int(user_id)).first()
    resumes = [r.id for r in user.resumes]
    return render_template(
        'add.html',
        user_name=user.name,
        resumes=resumes
    )

@app.route("/save/<int:cv_id>")
def save(cv_id):
    Session = sessionmaker(bind = engine)
    sess = Session()
    data = sess.query(Resume).filter(Resume.id == int(cv_id)).first()
    import pdfkit
    pdfkit.from_url('http://127.0.0.1:5000//resume/{}'.format(cv_id),'my_cv.pdf')
    # return render_template(
    #     'resume.html',
    #     name=data.name,
    #     email=data.email,
    #     mobile=data.mobile,
    #     github=data.github,
    #     linkedin=data.linkedin,
    #     summary=data.summary,
    #     job=data.job,
    #     company=data.company,
    #     period=data.period,
    #     description=data.description,
    #     university=data.university,
    #     faculty=data.faculty,
    #     gpa=data.GPA,
    #     skills=data.skills,
    #     cv_id=data.id
    # )

@app.route("/resume/<int:resume_id>")
def resume(resume_id):
    Session = sessionmaker(bind = engine)
    sess = Session()
    data = sess.query(Resume).filter(Resume.id == int(resume_id)).first()

    return render_template(
        'resume.html',
        name=data.name,
        email=data.email,
        mobile=data.mobile,
        github=data.github,
        linkedin=data.linkedin,
        summary=data.summary,
        job=data.job,
        company=data.company,
        period=data.period,
        description=data.description,
        university=data.university,
        faculty=data.faculty,
        gpa=data.GPA,
        skills=data.skills,
        cv_id=data.id
    )

if __name__ == "__main__":
    app.run(debug=True)