import random
import webbrowser
from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy

# config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)

# database model
class ShortUrl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	uuid = db.Column(db.String(15), unique=True, nullable=False)
	link = db.Column(db.String(300), nullable=False)

	def __repr__(self):
		return f"{self.id} | {self.uuid} | {self.link}"

# routing
@app.route('/', methods=['POST', 'GET'])
def index():
	characters = "0123456789-abcdefghijklmnopqrstuvwxyz"
	uuid = ''
	shorted = ''
	
	if request.method == 'POST':
		url = request.form.get('url')

		for i in range(15):
			uuid += random.choice(characters)

		new_link = ShortUrl(uuid=uuid, link=url)
		shorted = f'localhost:5000/{uuid}'

		db.session.add(new_link)
		db.session.commit()
			
		print(url)


	return render_template('index.html', shorted=shorted)

@app.route('/<id>')
def link_to_redirect(id):
	exists = ShortUrl.query.filter_by(uuid=str(id)).first()

	try:
		return redirect(str(exists.link), code=302)
	except AttributeError:
		pass

#another
if __name__ == '__main__':
	app.run(debug=False)