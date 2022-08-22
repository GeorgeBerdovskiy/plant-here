from flask import Flask, render_template, request
app = Flask(__name__)

from barrel import Functions

@app.route("/", methods=["GET", "POST"])
def home():
  if (request.method == "POST"):
    rainfall = Functions.determine_rainfall(-5, 30)
    return render_template('index.html', rainfall=rainfall)
  else:
    return render_template('index.html')
  

if __name__ == "__main__":
  app.run()