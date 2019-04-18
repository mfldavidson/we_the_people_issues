from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col, DateCol, LinkCol, BoolCol
from flask_table.html import element

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
    signature_count = db.Column(db.Integer)
    signatures_needed = db.Column(db.Integer)
    url = db.Column(db.String(250))
    deadline_date = db.Column(db.DateTime)
    status = db.Column(db.String(25))
    response = db.Column(db.Text)
    created_date = db.Column(db.DateTime)
    is_signable = db.Column(db.Boolean)
    reached_public = db.Column(db.Boolean)
    type_rel = db.relationship('PetitionType',secondary='typepetitionassociation',back_populates='petition_rel',lazy='dynamic')
    issue_rel = db.relationship('Issue',secondary='issuepetitionassociation',back_populates='petition_rel',lazy='dynamic')

    def __repr__(self):
        return 'Petition: {}'.format(self.title)

class PetitionType(db.Model):
    __tablename__ = "types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    petition_rel = db.relationship('Petition',secondary='typepetitionassociation',back_populates='type_rel',lazy='dynamic')

    def __repr__(self):
        return "Type: {}".format(self.name)

class Issue(db.Model):
    __tablename__ = "issues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    petition_rel = db.relationship('Petition',secondary='issuepetitionassociation',back_populates='issue_rel',lazy='dynamic')

    def __repr__(self):
        return "Issue: {}".format(self.name)

class TypePetitionAssociation(db.Model):
    __tablename__ = 'typepetitionassociation'
    rel_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    petition_id = db.Column(db.Integer, db.ForeignKey('petitions.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    petition_assoc = db.relationship(Petition, backref=db.backref('type_assoc'))
    type_assoc = db.relationship(PetitionType, backref=db.backref('petition_assoc'))

class IssuePetitionAssociation(db.Model):
    __tablename__ = 'issuepetitionassociation'
    rel_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    petition_id = db.Column(db.Integer, db.ForeignKey('petitions.id'))
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'))
    petition_assoc = db.relationship(Petition, backref=db.backref('issue_assoc'))
    issue_assoc = db.relationship(Issue, backref=db.backref('petition_assoc'))

# ExternalURLCol code adapted from: https://github.com/plumdog/flask_table/blob/master/examples/external_url_col.py
class ExternalURLCol(Col):
    def __init__(self, name, url_attr):
        self.url_attr = url_attr
        super(ExternalURLCol, self).__init__(name)

    def td_contents(self, item, attr_list):
        text = 'Original We the People Petition'
        url = self.from_attr_list(item, [self.url_attr])
        return element('a', {'href': url}, content=text)

class PetitionTable(Table):
    html_attrs = {'table-layout':'fixed'}
    title = Col('Petition Title')
    url = ExternalURLCol('Link to Petition on We the People', url_attr='url')
    created_date = DateCol('Created')
    deadline_date = DateCol('Deadline')

    def get_td_attrs(self, item):
        return {'word-wrap':'break-word'}

class OpenPetitionTable(PetitionTable):
    signatures_needed = Col('Signatures Needed')

class ClosedPetitionTable(PetitionTable):
    status = Col('Status')
    reached_public = BoolCol('Reached Public?')

def getPetitionsByIssue(issue_id):
    rels = IssuePetitionAssociation.query.filter_by(issue_id=issue_id).all()
    petitions = []
    for rel in rels:
        petitions.append(Petition.query.filter_by(id=rel.petition_id).first())
    return petitions

def splitPetitionsBySignable(list_of_petitions):
    open_petitions = []
    closed_petitions = []
    for petition in list_of_petitions:
        if petition.is_signable:
            open_petitions.append(petition)
        else:
            closed_petitions.append(petition)
    return open_petitions, closed_petitions

def filterPetitions(list_of_petitions, status='All', is_signable='All', reached_public='All'):
    filtered_petitions = []
    for petition in list_of_petitions:
        meets_reqs = True
        if status != 'All':
            if status == 'All but Open':
                if petition.status == 'open':
                    meets_reqs = False
            elif petition.status != status:
                meets_reqs = False
        if is_signable != 'All' and petition.is_signable != is_signable:
            meets_reqs = False
        if reached_public != 'All' and petition.reached_public != reached_public:
            meets_reqs =  False
        if meets_reqs == True:
            filtered_petitions.append(petition)
    return filtered_petitions
