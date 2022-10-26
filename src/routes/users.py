@app.route("/users", methods=['GET'])
def display_all():
    return jsonify(User.query.all())

# @app.route('/new', methods = ['GET', 'POST'])
# def new():
#     if request.method == 'POST':
#         if not request.form['username'] or not request.form['screenname'] or not request.form['password']:
#             flash('Please enter all the required fields.', 'error')
#         else:
#             user = user(request.form['username'], request.form['screnname'], request.form['password'])

#             db.session.add(user)
#             db.session.commit()
#             flash('User added succesfully')
#             return redirect(url_for('display_all'))
#         return render_template('new.html')