from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from generator import Crossword
import random
import string

app = Flask(__name__)
app.secret_key = "srydtufyguhlk"


class CrosswordForm(FlaskForm):
    size = IntegerField("Size", default=15)
    submit = SubmitField("Generate")


@app.route('/', methods=['GET', 'POST'])
def home():
    form = CrosswordForm()
    if form.validate_on_submit():
        crossword = Crossword(form.size.data)
        result = crossword.solve()
        if result:
            filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            crossword.save(f"./static/crosswords/{filename}.png")
            crossword.save(f"./static/crosswords/{filename}-hidden.png", True)

            return render_template("result.html", path1=f"./static/crosswords/{filename}.png",
                                   path2=f"./static/crosswords/{filename}-hidden.png", sentences=crossword.sentences)
        return redirect(url_for("home"))
    return render_template("home.html", form=form)


if __name__ == "__main__":
    print("Running flask app!")
    app.run(debug=True)
