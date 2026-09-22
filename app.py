from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="career_templates",
    static_folder="career_static"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student")
def student():
    return render_template("student.html")


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/roadmap")
def roadmap():
    return render_template("roadmap.html")


if __name__ == "__main__":
    app.run(debug=True)
