from flask import Flask,url_for,redirect,flash,request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
import click
from werkzeug.utils import redirect 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:123456@localhost:3306/c_book?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app) 

# 页面的操作 views.py
@app.route('/',methods=['GET','POST'])
def index():
  if request.method == 'POST': # 判断是否是 POST 请求
    # 获取表单数据
    title = request.form.get('title') # 传入表单対应输入字段的 NAME 值
    year = request.form.get('year')
    # 验证数据
    if not title or not year or len(year) > 4 or len(title) > 60:
      flash('Invalid input.') # 显示错误提示
      return redirect(url_for('index'))  #重定向回主页
    # 保存表单数据到数据库
    movie = Movie(title=title, year=year) # 创建记录
    db.session.add(movie) # 添加到数据库会话
    db.session.commit() # 提交数据库会话
    flash('Item created.')
    return redirect(url_for('index')) # 重定向回主页
  movies =  Movie.query.all()  
  return render_template('index.html', movies=movies)
  # 删除电影条目
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
  # 404 错误处理函数
@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
  user = User.query.first()
  return render_template('404.html'), 404 # 返回模板和状态码
  # 模板上下文处理函数
@app.context_processor
def inject_user(): # 函数名可以随意修改
  user = User.query.first()
  return dict(user=user) # 需要返回字典， 等同于 return {'user': user}
  # 编辑电影条目
@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
  movie = Movie.query.get_or_404(movie_id)
  if request.method == 'POST':
    title = request.form['title']
    year = request.form['year']
    if not title or not year or len(year) > 4 or len(title) > 60:
      flash('Invalid input.')
      return redirect(url_for('edit',movie_id=movie_id)) # 重定向回対应的编辑页面
    movie.title = title # 更新标题
    movie.year = year # 更新年份
    db.session.commit() # 提交数据库会话
    flash("Item updated.")
    return redirect(url_for('index')) # 重定向回主页
  return render_template('edit.html',movie = movie)
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
  