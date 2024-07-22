from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, ValidationError
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


def time_validation(form, field):
    time_data = field.data.lower()
    if "am" not in time_data and "pm" not in time_data:
        raise ValidationError("Field must contain 'am' or 'pm'")


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField("Cafe location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open_time = StringField("Opening Time e.g. 8AM", validators=[DataRequired(), time_validation])
    closing_time = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired(), time_validation])
    coffee_rating = SelectField("Coffee Rating", validators=[DataRequired()], choices=[
        (1, "☕️"),
        (2, "☕️☕️"),
        (3, "☕️☕️☕️"),
        (4, "☕️☕️☕️☕️"),
        (5, "☕️☕️☕️☕️☕️")
    ])
    wifi_rating = SelectField("Wifi Strength Rating", validators=[DataRequired()],  choices=[
        (1, "💪"),
        (2, "💪💪"),
        (3, "💪💪💪"),
        (4, "💪💪💪💪"),
        (5, "💪💪💪💪💪")
    ])
    power_rating = SelectField("Power Socket Availability", validators=[DataRequired()],  choices=[
        (1, "🔌"),
        (2, "🔌🔌"),
        (3, "🔌🔌🔌"),
        (4, "🔌🔌🔌🔌"),
        (5, "🔌🔌🔌🔌🔌")
    ])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_row = [
            form.cafe.data,
            form.location_url.data,
            form.open_time.data,
            form.closing_time.data,
            int(form.coffee_rating.data) * "☕️",
            int(form.wifi_rating.data) * "💪",
            int(form.power_rating.data) * "🔌"
        ]
        with open('cafe-data.csv', newline='', encoding='utf-8', mode='a') as csv_file:
            csv_writter = csv.writer(csv_file)
            csv_writter.writerow(new_row)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
