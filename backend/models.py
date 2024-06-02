from backend import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)

class Follow(db.Model):
    __tablename__ = 'follow'
    user_id = db.Column(db.String, db.ForeignKey('users.user_id'), primary_key=True)
    follower_id = db.Column(db.String, db.ForeignKey('users.user_id'), primary_key=True)

class Paper(db.Model):
    __tablename__ = 'paper'
    paper_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    reference = db.Column(db.Integer)
    venue = db.Column(db.String)
    year = db.Column(db.Integer)
    n_citation = db.Column(db.Integer)
    author = db.Column(db.String)

class Abstract(db.Model):
    __tablename__ = 'abstract'
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.paper_id'), primary_key=True)
    abstract = db.Column(db.Text)
    abstract_vector = db.Column(db.ARRAY(db.Float))

class UserKeyword(db.Model):
    __tablename__ = 'user_keyword'
    user_id = db.Column(db.String, db.ForeignKey('users.user_id'), primary_key=True)
    keyword = db.Column(db.String, primary_key=True)
    keyword_vector = db.Column(db.ARRAY(db.Float))
