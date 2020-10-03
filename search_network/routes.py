import os , json
import functools
import secrets
from PIL import Image
from search_network.form import SearchForm, NewProjectForm, NewIdeaForm
from flask import Flask,  render_template , url_for , redirect , flash, request, abort , jsonify
from search_network.models import Person, Project, Idea, Department
from search_network import app, db, socketio, mail, bcrypt, mobility
from flask_socketio import send , disconnect
from flask_mail import Message
from flask_mobility.decorators import mobile_template
from sqlalchemy import or_ ,and_
from validate_email import validate_email

from pony.orm import *




@app.route("/")
def home():
 #if current_user.is_authenticated:  
 #   page = request.args.get('page' , 1 , type=int )
 #   stories = Story.query.join(followers, (followers.c.followed_id == Story.user_id)).filter(followers.c.follower_id == current_user.id)
 #   posts = Post.query.join(followers, (followers.c.followed_id == Post.user_id )).filter(followers.c.follower_id == current_user.id).order_by(Post.date_posted.desc()).paginate(page=page , per_page=7) 
 #   #posts2 = Post.query.filter_by(author=current_user).all()
 #else:  
    projects = []
    persons = []
    ideas = []
    departments = []
    #return redirect(url_for('login')) 
 #posts_liked = Post.query.join(liking , (liking.c.post_liked_id == Post.id )).filter(liking.c.liker_id == current_user.id).all()
    return render_template('home.html') #, posts=posts , liked=posts_liked , stories=stories) 


@app.route("/about")
def about():
    return "<h1>about page</h1>"

# @app.route("/register" , methods=[ 'GET' , 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#          hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#          user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#          db.session.add(user)
#          db.session.commit()
#          flash('Welcome to Lamma !', 'success')
#          login_user(user)
#          return redirect(url_for('home'))
#     return render_template('register.html', title='Register', form=form)


# @app.route("/login" , methods=[ 'GET' , 'POST'])
# def login():
#     if current_user.is_authenticated:
#         current_user.online = True
#         return redirect(url_for('home'))
#     else: 
#         current_user.is_online = False   
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user and bcrypt.check_password_hash(user.password , form.password.data):
#           login_user(user, remember=form.remember.data)
#           user.online = True
#           db.session.commit()
#           next_page = request.args.get('next')
#           return redirect(next_page) if next_page else redirect(url_for('home'))     
#         else:
#          flash('Login Unsuccessful. Please check email and password', 'danger') 
#     return render_template('login.html', title='login', form=form)
    

# @app.route("/logout")
# def logout():
#     current_user.online = False
#     db.session.commit()
#     logout_user()
#     return redirect(url_for('home'))


# """@app.route("/is_online/<int:uid>")
# def is_online(uid):
#     user = User.query.filter_by(id=uid).first_or_404()
#     if user.online:
#         return '1' 
#     else:
#         return '0'   """ 


def save_picture(form_picture,x,y,folder):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/'+ folder, picture_fn)
    
    output_size = (x, y)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


# @app.route("/account" , methods=[ 'POST' , 'GET'])
# @login_required
# def account():
#     page = request.args.get('page' , 1 , type=int )
#     posts = Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).paginate(page=page , per_page=5)    
#     form = UpdateForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#            picture_file = save_picture(form.picture.data, 150 , 150 , 'profile_pics')
#            current_user.image_file = picture_file
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         return redirect(url_for('account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email    
#     image_file = url_for('static' , filename='profile_pics/' + current_user.image_file)
#     if current_user.private:
#         private = 'Make your account public'
#     else:
#         private = 'Make your account private' 
#     followingn = db.session.query(followers).filter_by(follower_id=current_user.id).count() 
#     followersn = db.session.query(followers).filter_by(followed_id=current_user.id).count()     
#     return render_template('account.html' , title='account' , image_file=image_file , form=form , posts=posts , 
#         user=current_user , private_or_not = private , nbrfollowers = followersn,
#         nbrfollowing = followingn ) 


@app.route("/projects")
@app.route("/projects/new" , methods=[ 'POST' , 'GET'])
#@login_required
def new_project():
    form = NewProjectForm()
    if form.validate_on_submit():
        if form.image.data:
           projectimage_file = save_picture(form.image.data, 500 , 500 , 'project_pictures')
        else:
            projectimage_file = None
        project = Project(title=form.title.data, content=form.content.data, author=current_user, image=postimage_file )
        db.session.add(project)
        db.session.commit()
        flash('Your project has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('New_project.html' , title='New project' , form=form , legend='Create project')


@app.route("/projects")
@app.route("/ideas/new" , methods=[ 'POST' , 'GET'])
#@login_required
def new_idea():
    form = NewIdeaForm()
    if form.validate_on_submit():
        if form.image.data:
           ideaimage_file = save_picture(form.image.data, 500 , 500 , 'idea_pictures')
        else:
            ideaimage_file = None
        idea = Idea(title=form.title.data, content=form.content.data, author=current_user, image=postimage_file )
        db.session.add(idea)
        db.session.commit()
        flash('Your idea has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('New_idea.html' , title='New idea' , form=form , legend='Create idea')


@app.route("/projects/<int:project_id>")
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template( 'project.html' , name=project.name , project=project)


@app.route("/persons/<int:person_id>")
def person(person_id):
    person = Person.query.get_or_404(person_id)
    return render_template( 'person.html' , name=person.name , person=person)


@app.route("/ideas/<int:idea_id>")
def idea(person_id):
    idea = Idea.query.get_or_404(idea_id)
    return render_template( 'idea.html' , name=idea.name , idea=idea)



# @app.route("/posts/<int:post_id>/update" , methods=[ 'POST' , 'GET'])
# @login_required
# def post_update(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#        abort(403)
#     form = NewPostForm()
#     if form.validate_on_submit():
#        if form.image.data:
#            postimage1_file = save_picture(form.image.data, 500 , 500 , 'post_pictures')
#            post.image = postimage1_file 
#        else: 
#             post.image = 'jjjjjjjjj.ll'   
#        post.title = form.title.data
#        post.content = form.content.data
#        db.session.commit() 
#        return redirect(url_for('post' , post_id=post_id))   
#     elif request.method == 'GET': 
#        form.title.data = post.title
#        form.content.data = post.content
#     return render_template( 'New_post.html' , title='Update post' , form=form , legend='Update post')


# @app.route("/posts/<int:post_id>/delete", methods=['POST'])
# @login_required
# def post_delete(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#        abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted!', 'success')
#     return redirect(url_for('home')) 


# @app.route("/user/<string:username>")
# def user_account(username):
#     page = request.args.get('page' , 1 , type=int )
#     user = User.query.filter_by(username=username).first_or_404()  
#     if user == current_user:
#        return redirect(url_for('account') ) 
#     posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page , per_page=5) 
#     form = UpdateForm()
#     form.username.data = user.username
#     form.email.data = user.email
#     image_file = url_for('static' , filename='profile_pics/' + user.image_file)
#     if current_user.is_following(user):
#         fon = 'unfollow'
#         postsview = True
#     else:
#         if current_user.is_requesting(user): 
#             fon = 'requested'
#         else: 
#             fon = 'follow'
#         if user.private == True:
#             postsview = False 
#         else:
#             postsview = True            
#     followingn = db.session.query(followers).filter_by(follower_id=user.id).count() 
#     followersn = db.session.query(followers).filter_by(followed_id=user.id).count()        
#     return render_template('account.html' , title=username + ' -profile' , 
#         image_file=image_file , 
#         form=form , 
#         posts=posts, 
#         user=user,
#         followed_or_not = fon,
#         nbrfollowers = followersn,
#         nbrfollowing = followingn,
#         postsview=postsview)  


@app.route("/search")
#@login_required
def search(): 
    query = request.args.get('search', '')
    query = query.split(',') #Example:  Peter, persons True, projects False, ideas False, skills python linux
    name = query[0]
    features = [x.split() for x in query[1:]]
    features_ = {}
    for list_ in features:
        k = list_[0]
        features_[k] = list_[1:]

    skills = features_['skills'] if 'skills' in features_.keys() else []
    areas = features_['areas'] if 'areas' in features_.keys() else []
    department = features_['department'] if 'department' in features_.keys() else None
    print(name, skills, areas, department)

    full_select = []
    if 'persons' not in features_.keys() or features_['persons']:
        persons = select(p for p in Person if (name == 'none' or name == p.name) and
                         ((not skills) or (p.skills.select(lambda x: x.name in skills).count() > 0)) and
                         ((not areas) or (p.areas.select(lambda x: x.name in areas).count() > 0)) and
                         ((department is None) or department == p.department.name)
                         )[:]
        full_select.extend(persons)
        print(full_select)
    if 'projects' not in features_.keys() or features_['projects']:
        projects = select(p for p in Project if (name == 'none' or name == p.name) and
                          ((not skills) or (p.skills.select(lambda x: x.name in skills).count() > 0)) and
                          ((not areas) or (p.areas.select(lambda x: x.name in areas).count() > 0)) and
                          ((department is None) or department == p.department.name)
                          )[:]
        full_select.extend(projects)
    if 'ideas' not in features_.keys() or features_['ideas']:
        ideas = select(p for p in Idea if (name == 'none' or name == p.name) and
                       ((not skills) or (p.skills.select(lambda x: x.name in skills).count() > 0)) and
                       ((not areas) or (p.areas.select(lambda x: x.name in areas).count() > 0)) and
                       ((department is None) or department == p.department.name)
                       )[:]
        full_select.extend(ideas)
    print(full_select)
    return render_template('search.html', full_select=full_select)


# @app.route("/chats")
# @login_required
# def chats():
#     messages = Chats.query.filter((Chats.sender_id == current_user.id)).all()
#     others_ids = []
#     for message in messages:
#         others_ids.append(message.reciever_id) 
#     return     


# @app.route("/chatting/<int:user_id>" , methods=['GET' , 'POST'])
# @login_required
# def chat(user_id):
#     user = User.query.filter_by(id=user_id).first_or_404()
#     messages = Chats.query.filter(or_(and_(Chats.sender_id == user_id , 
#         Chats.reciever_id == current_user.id) , and_(Chats.sender_id == current_user.id,
#       Chats.reciever_id == user_id) )).all()
#     return render_template('chat.html' , messages=messages ,
#      user=current_user, friend=user )


# @app.route("/chatting/message/<string:message>/<int:user_id>" , methods=['POST' , 'GET'])
# @login_required
# def send_message(message , user_id):
#     if message != 'voidmessagevoidmessagevoidmessage':
#         chat = Chats(message=message , sender_id=current_user.id , reciever_id=user_id)
#         db.session.add(chat)
#         db.session.commit()
#     messages = Chats.query.filter(or_(and_(Chats.sender_id == user_id , 
#         Chats.reciever_id == current_user.id) , and_(Chats.sender_id == current_user.id,
#       Chats.reciever_id == user_id) )).all()
#     messages_data = []
#     for message in messages:
#         message_data = {
#             'message' : message.message,
#             'sender' : message.sender_id}
#         messages_data.append(message_data)         
#     return json.dumps(messages_data)   


# """@app.route("/chatting/message/<string:message><int:user_id>" , methods=['POST'])
# @login_required
# def chats():
#     conversations = Chats.query.filter(Chats.sender_id)"""


# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message('Password Reset Request',
#                   sender='noreply@demo.com',
#                   recipients=[user.email])
#     msg.body = ' To reset your password, visit the following link:\n%s\nIf you did not make this request then simply ignore this email and no changes will be made.' % {url_for("reset_token", token=token, _external=True)}
#     mail.send(msg)


# @app.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)


# @app.route("/reset_password/<token>", methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = form.password.data
#         user.password = hashed_password
#         db.session.commit()
#         flash('Your password has been updated! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html', title='Reset Password', form=form)    


# @app.route("/following/<int:followed_id>")
# @login_required
# def following(followed_id):
#     user = current_user  
#     followed = User.query.filter_by(id=followed_id).first_or_404()  
#     if not user.is_following(followed):
#       if not followed.private:  
#         event = user.follow(followed)
#         db.session.add(event)
#         db.session.commit()
#       else:
#        if not user.is_requesting(followed) and not user.is_following(followed): 
#         event = user.request(followed)
#         db.session.add(event)
#         db.session.commit()  
#        else:
#         event = user.unrequest(followed)
#         db.session.add(event)
#         db.session.commit() 
#     else:
#         event = user.unfollow(followed)
#         db.session.add(event)
#         db.session.commit()    
#     return redirect(url_for('user_account' , username=followed.username))


# @app.route("/private/<int:private_id>")
# def private(private_id):
#     user = current_user
#     if not user.private:
#         user.private = True 
#         db.session.commit()
#     else:
#         user.private = False 
#         db.session.commit() 
#     return redirect(url_for('user_account' , username=current_user.username))


# @app.route("/requests")
# @login_required
# def handle_request():
#     users_requesting = User.query.join(requests , (requests.c.follower_id == User.id )).filter(requests.c.followed_id == current_user.id).all()
#     return render_template('requests.html' , users_requesting=users_requesting)


# def delete_request(follower):
#         event = follower.unrequest(current_user)
#         db.session.add(event)
#         db.session.commit()


# @app.route("/requests/accept_or_delete/<int:follower_id><string:user_choice>", methods=['GET', 'POST'])
# @login_required
# def accept_or_delete(user_choice , follower_id):
#     follower = User.query.filter_by(id=follower_id).first_or_404()
#     if user_choice == 'accept':
#         event = follower.follow(current_user)
#         db.session.add(event)
#         db.session.commit()
#     delete_request(follower)
#     return redirect(url_for('handle_request'))


# @app.route("/like/handle/<int:liker_id><int:post_liked_id><int:rate>" , methods=['GET' , 'POST'])
# def like_post(liker_id , post_liked_id, rate):
#     post = Post.query.filter_by(id=post_liked_id).first_or_404()
#     user = User.query.filter_by(id=liker_id).first_or_404()
#     if not post.is_liked_by(user):
#         e = post.liked_by(user)
#         db.session.add(e)
#         post.number_of_reactions = post.number_of_reactions + 1
#         db.session.commit()             
#     """ if rate == 1:
#         r = 25 
#     elif rate == 2:
#         r = 50
#     elif rate == 3:
#         r = 75 
#     elif rate == 4: 
#         r = 100 
#     else:
#         r = rate                
#     old_number = post.number_of_reactions
#     new_number = post.number_of_reactions + 1 
#     old = post.like_percentage
#     post.like_percentage = (((old * old_number) + r) / new_number)
#     post.number_of_reactions = new_number 
#     db.session.commit()"""
#     return render_template('likes.html' , likes=post.number_of_reactions)
