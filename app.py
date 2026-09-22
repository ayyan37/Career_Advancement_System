from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
import json

app = Flask(
    __name__,
    template_folder="career_templates",
    static_folder="career_static"
)

# Firebase connection
firebase_credentials = json.loads(
    os.environ["FIREBASE_CREDENTIALS"]
)

cred = credentials.Certificate(firebase_credentials)

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://career-advancement-system-default-rtdb.asia-southeast1.firebasedatabase.app"
})


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- STUDENT DETAILS ----------------

@app.route("/student")
def student():
    return render_template("student.html")


# ---------------- TEST ----------------

@app.route("/test")
def test():
    return render_template("test.html")


# ---------------- RESULT ----------------

@app.route("/result")
def result():
    return render_template("result.html")


# ---------------- ROADMAP ----------------

@app.route("/roadmap")
def roadmap():
    return render_template("roadmap.html")


# ---------------- SAVE RESULT ----------------

@app.route("/save_result", methods=["POST"])
def save_result():

    try:

        data = request.get_json()

        print("SAVE RESULT DATA:", repr(data))

        # Check received data
        if not isinstance(data, dict):

            return jsonify({
                "success": False,
                "error": "Invalid result data"
            }), 400


        # Clean data before sending to Firebase
        def clean_data(value):

            if isinstance(value, dict):

                return {
                    str(k): clean_data(v)
                    for k, v in value.items()
                }


            if isinstance(value, list):

                return [
                    clean_data(v)
                    for v in value
                ]


            if value is None:

                return ""


            if isinstance(value, (str, int, float, bool)):

                return value


            return str(value)


        clean_result = clean_data(data)


        # Save result in Firebase
        ref = db.reference("student_results")

        new_result = ref.push(clean_result)


        print("FIREBASE SAVED:", new_result.key)


        return jsonify({
            "success": True,
            "id": new_result.key
        })


    except Exception as e:

        print("FIREBASE ERROR:", repr(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ---------------- RUN APP ----------------

if __name__ == "__main__":

    app.run(debug=True)
