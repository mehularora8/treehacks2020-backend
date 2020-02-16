from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trashcan.db'
db = SQLAlchemy(app)
db.create_all()

class trashcan(db.Model):
	dustbin_id = db.Column(db.Integer, primary_key = True, unique = True)
	trash = db.Column(db.Integer, nullable = True)
	compost = db.Column(db.Integer, nullable = True)
	recycling = db.Column(db.Integer, nullable = True)
	def __repr__(self):
		return str(self.__dict__)


@app.route('/', methods = ['POST', 'GET'])
def index():
	
	if request.method == 'GET':
		bins = trashcan.query.all()
		return render_template('index.html', bins = bins)

	elif request.method == "POST": 
		dustbin_id = request.form['id']
		argument_recycling = request.form["recycling"]
		argument_compost = request.form["compost"]
		argument_trash = request.form["trash"]

		if trashcan.query.filter_by(dustbin_id = dustbin_id).first() is None:
			new_dustbin = trashcan(dustbin_id = dustbin_id, trash = argument_trash, compost = argument_compost, recycling = argument_recycling)
			db.session.add(new_dustbin)
			db.session.commit()
			return "New record added"

		else:
			target_dustbin = trashcan.query.get(dustbin_id)
			
			target_dustbin.trash = argument_trash
			target_dustbin.compost = argument_compost
			target_dustbin.recycling = argument_recycling
			
			try:
				db.session.commit()
				return "200\n"

			except:
				return "Internal Failure"


if __name__ == "__main__":
	app.run(debug = True)
