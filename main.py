from flask import Flask, render_template, redirect
from flask.helpers import url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import URL, DataRequired, InputRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class AddCoffeeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[InputRequired()])
    location = StringField('Cafe Location on Google Map(URL)', validators=[InputRequired(), URL()])
    open_time = StringField('Opening Time e.g 8AM', validators=[InputRequired()])
    closing_time = StringField('Closing Time e.g 8:30PM', validators=[InputRequired()])
    coffee_rating = SelectField('Coffee Rating', validators=[InputRequired()], choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"])
    wifi_rating = SelectField('Wifi Strength Rating', validators=[InputRequired()], choices=['💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    power_outlet = SelectField('Power Socket Available', validators=[InputRequired()], choices=['🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = AddCoffeeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', encoding="utf8") as csv_file:
            csv_file.write(
                f"\n{form.cafe_name.data},"
                f"{form.location.data},"
                f"{form.open_time.data},"
                f"{form.closing_time.data},"
                f"{form.coffee_rating.data},"
                f"{form.wifi_rating.data},"
                f"{form.power_outlet.data},"
            )
            return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
