from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db
from myapp.models import ThriftItem
from myapp.thrift_items.forms import ThriftItemForm

thrift_items = Blueprint('thrift_items', __name__)

@thrift_items.route('/create', methods=['GET', 'POST'])
@login_required
def create_item():
    form = ThriftItemForm()
    if form.validate_on_submit():
        thrift_item = ThriftItem(name=form.name.data, item_details=form.item_details.data,
        user_id=current_user.id)
        db.session.add(thrift_item)
        db.session.commit()
        flash('Thrift Item Created')
        print('Thrift Item was created')
        return redirect(url_for('core.index'))
    return render_template('create_item.html', form=form)

@thrift_items.route('/<int:thrift_item_id>')
def thrift_item(thrift_item_id):
    thrift_item = ThriftItem.query.get_or_404(thrift_item_id) 
    return render_template('thrift_item.html', name=thrift_item.name, date=thrift_item.date, item=thrift_item)

@thrift_items.route('/<int:thrift_item_id>/update',methods=['GET','POST'])
@login_required
def update(thrift_item_id):
    thrift_item = ThriftItem.query.get_or_404(thrift_item_id)

    if thrift_item.author != current_user:
        abort(403)

    form = ThriftItemForm()

    if form.validate_on_submit():
        thrift_item.name = form.name.data
        thrift_item.item_details = form.item_details.data
        db.session.commit()
        flash('Thrift Item Updated')
        return redirect(url_for('thrift_items.thrift_item',thrift_item_id=thrift_item.id))

    elif request.method == 'GET':
        form.name.data = thrift_item.name
        form.item_details.data = thrift_item.item_details

    return render_template('create_item.html',title='Updating',form=form)


@thrift_items.route('/<int:thrift_item_id>/delete',methods=['GET','POST'])
@login_required
def delete_item(thrift_item_id):
    thrift_item = ThriftItem.query.get_or_404(thrift_item_id)
    if thrift_item.author != current_user:
        abort(403)

    db.session.delete(thrift_item)
    db.session.commit()
    flash('Thrift Item Deleted')
    return redirect(url_for('core.index'))