from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
import click 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:123456@localhost:3306/c_book?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app) 


# 页面的操作 views.py
@app.route('/')
def index():
  return render_template('index.html', name=name, movies=movies)
# 数据库的操作 module.py
  # 创建数据库操作
class User(db.Model): #表名将会是 user (自动生成，小写处理)
  id = db.Column(db.Integer, primary_key = True) # 主键
  name = db.Column(db.String(20)) # 名字
class Movie(db.Model): # 表名将会是 movies
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(60)) # 电影标题
  year = db.Column(db.String(4)) # 电影年份

# 自定义命令

@app.cli.command() # 注册为命令
@click.option('--drop',is_flag=True, help='Create after drop.') # 设置选项
def initdb(drop):
  """ Inittialize  the database. """
  if drop :  # 判断是否输入了选项
    db.drop_all()
  db.create_all()
  click.echo('Inittialized database.')

@app.cli.command()
def forge():
  """ Generate fake data. """
  db.create_all()

  # 全局的两个变量移动到这个函数内
  name = 'Grey Li'
  movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
  ]
  user = User(name=name)
  db.session.add(user)
  for m in movies:
    movie = Movie(title=m['title'],year = m['year'])
    db.session.add(movie)

  db.session.commit()
  click.echo('Done')
  