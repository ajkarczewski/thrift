# core/views.py 
from flask import render_template, request, Blueprint
from myapp.models import ThriftList

core = Blueprint('core', __name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    thrift_lists = ThriftList.query.order_by(ThriftList.date.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', thrift_lists=thrift_lists)

@core.route('/info')
def info():
    return render_template('info.html')
