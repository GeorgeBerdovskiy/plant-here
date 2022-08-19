from flask import Flask, render_template, request
app = Flask(__name__)

from classes import RainBarrel

@app.route("/", methods=["POST"])
def home():
  if (request.method == "POST"):
    rainfall = 0.05
    return render_template('index.html', ranfall=rainfall)
  else:
    return render_template('index.html')
  

if __name__ == "__main__":
  app.run()