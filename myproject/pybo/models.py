from pybo import db

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))


class L4_wideip(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    wideip = db.Column(db.String(100),  unique=True, nullable=False)
    wideip_record = db.Column(db.String(20), nullable=False)
    wideip_status = db.Column(db.String(20), nullable=False)
    wideip_en = db.Column(db.String(20), nullable=False)
    wideip_lbmod = db.Column(db.String(20), nullable=False)
    wideip_rcof = db.Column(db.String(20), nullable=False)


class L4_pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    wideip = db.Column(db.String(200),  nullable=False)
    pool = db.Column(db.String(200),  nullable=False)
    ratio = db.Column(db.Integer)
    order = db.Column(db.Integer)


class L4_pool_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pool = db.Column(db.String(200), unique=True, nullable=False)
    pool_ttl = db.Column(db.Integer)
    pool_status = db.Column(db.String(20), nullable=False)
    pool_en = db.Column(db.String(20), nullable=False)
    pool_lbmod = db.Column(db.String(20), nullable=False)
    pool_alter = db.Column(db.String(20), nullable=False)
    pool_fallback = db.Column(db.String(20), nullable=False)
    pool_avail = db.Column(db.String(20), nullable=False)

class L4_poolmbr(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pool = db.Column(db.String(200),  nullable=False)
    poolmbr = db.Column(db.String(200),  nullable=False)
    poolmbr_status = db.Column(db.String(20))
    ratio = db.Column(db.Integer)
    order = db.Column(db.Integer)

class L4_poolmbr_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    poolmbr = db.Column(db.String(200),  nullable=False)
    poolmbr_status = db.Column(db.String(20), nullable=False)
