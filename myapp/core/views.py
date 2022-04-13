# core/views.py 
from flask import render_template, request, Blueprint
from myapp.models import ThriftItem

core = Blueprint('core', __name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    thrift_items = ThriftItem.query.order_by(ThriftItem.date.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', thrift_items=thrift_items)

@core.route('/info')
def info():
    return render_template('info.html')
