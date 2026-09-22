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

# ==============================
# FIREBASE CONNECTION
# ==============================

firebase_credentials = json.loads(
    os.environ["FIREBASE_CREDENTIALS"]
)

cred = credentials.Certificate(firebase_credentials)

firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://career-advancement-system-default-rtdb.asia-southeast1.firebasedatabase.app"
    }
)


# ==============================
# PAGES
# ==============================

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


# ==============================
# SAVE TEST RESULT
# ==============================

@app.route("/save_result", methods=["POST"])
def save_result():

    try:

        data = request.get_json()

        print("SAVE RESULT DATA:", repr(data))

        # Check data
        if not isinstance(data, dict):

            return jsonify({
                "success": False,
                "error": "Invalid result data"
            }), 400


        # Convert to clean JSON
        clean_result = json.loads(
            json.dumps(
                data,
                allow_nan=False
            )
        )


        print("CLEAN RESULT:", repr(clean_result))


        # Firebase reference
        ref = db.reference("student_results")


        # Create new Firebase entry
        new_result = ref.push()


        # Save data
        new_result.set(clean_result)


        print(
            "FIREBASE SAVED:",
            new_result.key
        )


        return jsonify({
            "success": True,
            "id": new_result.key
        })


    except Exception as e:

        print(
            "FIREBASE ERROR:",
            repr(e)
        )

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":

    app.run(
        debug=True
    )
