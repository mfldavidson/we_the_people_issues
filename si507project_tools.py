from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'gordonbdnumber1cat'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./petitions.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = db.session

# models
class Petition(db.Model):
    __tablename__ = "petitions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    body = db.Column(db.Text)
    type = db.Column(db.Integer, db.ForeignKey('types.id'))
    issue = db.Column(db.Integer, db.ForeignKey('issues.id'))
    signature_threshold = db.Column(db.Integer)
    signature_count = db.Column(db.Integer)
    signatures_needed = db.Column(db.Integer)
    url = db.Column(db.String(250))
    deadline_date = db.Column(db.DateTime)
    status = db.Column(db.String(25))
    response = db.Column(db.Text)
    created_date = db.Column(db.DateTime)
    is_signable = db.Column(db.Boolean)
    is_public = db.Column(db.Boolean)
    reached_public = db.Column(db.Boolean)
    type_rel = relationship('Type',secondary='type-petition-association',back_populates='petition_rel',lazy='dynamic')
    issue_rel = relationship('Issue',secondary='issue-petition-association',back_populates='petition_rel',lazy='dynamic')

    def __repr__(self):
        return 'Petition: {}'.format(self.title)

class Type(db.Model):
    __tablename__ = "types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    petition_rel = relationship('Petition',secondary='type-petition-association',back_populates='type_rel',lazy='dynamic')

    def __repr__(self):
        return "Type: {}".format(self.name)

class Issue(db.Model):
    __tablename__ = "issues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    petition_rel = relationship('Petition',secondary='issue-petition-association',back_populates='issue_rel',lazy='dynamic')

    def __repr__(self):
        return "Issue: {}".format(self.name)

class TypePetitionAssociation(Base):
    __tablename__ = 'type-petition-association'
    petition_id = Column(Integer, ForeignKey('petitions.id'),primary_key=True)
    type_id = Column(Integer, ForeignKey('types.id'),primary_key=True)
    petition_assoc = relationship(Petition, backref=backref('type_assoc'))
    type_assoc = relationship(Type, backref=backref('petition_assoc'))

class IssuePetitionAssociation(Base):
    __tablename__ = 'issue-petition-association'
    petition_id = Column(Integer, ForeignKey('petitions.id'),primary_key=True)
    issue_id = Column(Integer, ForeignKey('issues.id'),primary_key=True)
    petition_assoc = relationship(Petition, backref=backref('issue_assoc'))
    issue_assoc = relationship(Issue, backref=backref('petition_assoc'))

# functions to get or create new values
# def get_rating(rating_text,rating_num=None):
#     rating = Rating.query.filter_by(text=rating_text).first()
#     if rating:
#         return rating
#     else:
#         return 'This is not a valid MPAA rating. Please use one of the following: G, PG, PG-13, R, or NC-17'
#
# def get_or_create_distributor(distributor_name):
#     distributor = Distributor.query.filter_by(name=distributor_name).first()
#     if distributor:
#         return distributor
#     else:
#         distributor = Distributor(name=distributor_name)
#         session.add(distributor)
#         session.commit()
#         return distributor
#
# def get_or_create_director(first,last):
#     director = Director.query.filter_by(fname=first,lname=last).first()
#     if director:
#         return director
#     else:
#         director = Director(fname=first,lname=last)
#         session.add(director)
#         session.commit()
#         return director
