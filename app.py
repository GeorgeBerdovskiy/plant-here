from flask import Flask, render_template, request
app = Flask(__name__)

from barrel import Functions

@app.route("/", methods=["GET", "POST"])
def home():
  if (request.method == "POST"):
    rainfall = Functions.collect_from_bucket("2022", "08", "19", -5, -30)
    return render_template('index.html', rainfall=rainfall)
  else:
    return render_template('index.html')
  

if __name__ == "__main__":
  app.run()