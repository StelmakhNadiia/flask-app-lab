from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from . import disciplines_bp
from .models import Discipline, DisciplineCategory
from .forms import DisciplineForm

@disciplines_bp.route('/', methods=['GET'])
def list_disciplines():
    
    search_query = request.args.get('q', '')
    
    query = Discipline.query

   
    if search_query:
        query = query.filter(Discipline.name.ilike(f'%{search_query}%'))
    
  
    disciplines = query.order_by(Discipline.id.desc()).all()

    return render_template('disciplines/list.html', disciplines=disciplines, search_query=search_query)


@disciplines_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_discipline():
    form = DisciplineForm()
    
   
    categories = DisciplineCategory.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        discipline = Discipline(
            name=form.name.data,
            description=form.description.data,
            hours=form.hours.data,
            category_id=form.category_id.data,
            user=current_user 
        )
        db.session.add(discipline)
        db.session.commit()
        flash('Дисципліну успішно додано!', 'success')
        return redirect(url_for('disciplines_bp.list_disciplines'))

    return render_template('disciplines/create.html', form=form, title="Нова дисципліна")


@disciplines_bp.route('/<int:id>')
def detail_discipline(id):
    discipline = db.session.get(Discipline, id)
    if not discipline:
        abort(404)
    return render_template('disciplines/detail.html', discipline=discipline)


@disciplines_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_discipline(id):
    discipline = db.session.get(Discipline, id)
    if not discipline:
        abort(404)

  
    if discipline.user != current_user:
        flash('Ви не маєте прав редагувати цей запис!', 'danger')
        return redirect(url_for('disciplines_bp.detail_discipline', id=id))

    form = DisciplineForm()
   
    categories = DisciplineCategory.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        discipline.name = form.name.data
        discipline.description = form.description.data
        discipline.hours = form.hours.data
        discipline.category_id = form.category_id.data
        
        db.session.commit()
        flash('Дисципліну оновлено!', 'success')
        return redirect(url_for('disciplines_bp.detail_discipline', id=id))
    
    
    elif request.method == 'GET':
        form.name.data = discipline.name
        form.description.data = discipline.description
        form.hours.data = discipline.hours
        form.category_id.data = discipline.category_id

    return render_template('disciplines/create.html', form=form, title="Редагування")


@disciplines_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_discipline(id):
    discipline = db.session.get(Discipline, id)
    if not discipline:
        abort(404)
        
   
    if discipline.user != current_user:
        flash('Ви не маєте прав видаляти цей запис!', 'danger')
        return redirect(url_for('disciplines_bp.list_disciplines'))

    db.session.delete(discipline)
    db.session.commit()
    flash('Дисципліну видалено.', 'info')
    return redirect(url_for('disciplines_bp.list_disciplines'))