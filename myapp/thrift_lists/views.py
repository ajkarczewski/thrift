from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db, thrift_lists 
from myapp.models import ThriftList
from myapp.thrift_lists.forms import ThriftListForm

thrift_lists = Blueprint('thrift_lists', __name__)

@thrift_lists.route('/create', methods=['GET', 'POST'])
@login_required
def create_list():
    form = ThriftListForm()
    if form.validate_on_submit():
        thrift_list = ThriftList(title=form.title.data, text=form.text.data, user_id=current_user.id)
        db.session.add(thrift_list)
        db.session.commit()
        flash('Thrift List Created')
        print('Thrift List was created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

@thrift_lists.route('/<int:thrift_list_id>')
def thrift_list(thrift_list_id):
    thrift_list = ThriftList.query.get_or_404(thrift_list_id) 
    return render_template('thrift_list.html', title=thrift_list.title, date=thrift_list.date, post=thrift_list)

@thrift_lists.route('/<int:thrift_list_id>/update',methods=['GET','POST'])
@login_required
def update(thrift_list_id):
    thrift_list = ThriftList.query.get_or_404(thrift_list_id)

    if thrift_list.author != current_user:
        abort(403)

    form = ThriftListForm()

    if form.validate_on_submit():
        thrift_list.title = form.title.data
        thrift_list.text = form.text.data
        db.session.commit()
        flash('Thrift List Updated')
        return redirect(url_for('thrift_lists.thrift_list',thrift_list_id=thrift_list.id))

    elif request.method == 'GET':
        form.title.data = thrift_list.title
        form.text.data = thrift_list.text

    return render_template('create_post.html',title='Updating',form=form)


@thrift_lists.route('/<int:thrift_list_id>/delete',methods=['GET','POST'])
@login_required
def delete_list(thrift_list_id):

    thrift_list = ThriftList.query.get_or_404(thrift_list_id)
    if thrift_list.author != current_user:
        abort(403)

    db.session.delete(thrift_list)
    db.session.commit()
    flash('Thrift List Deleted')
    return redirect(url_for('core.index'))