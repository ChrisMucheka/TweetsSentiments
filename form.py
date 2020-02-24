from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField
from wtforms.validators import DataRequired,length



class TweetForms(FlaskForm):
    wordTopic = StringField('Topic of sentiment:',validators=[DataRequired,length(min=2,max=100)])
    noOfTweet= IntegerField ( 'Number of tweets:', validators=[DataRequired] )
    noOfTopWords = IntegerField ( 'Number of top words used:', validators=[DataRequired] )
    noOfTopHash = IntegerField ( 'Number of top hashtag:', validators=[DataRequired] )
    noOfTopRetweets = IntegerField ( 'Number of top retweets:', validators=[DataRequired] )
    submit = SubmitField('Submit')
