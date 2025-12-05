# app/views.py
from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.forms import ContactForm
import logging

main_bp = Blueprint('main', __name__)

# Налаштування логування (можна залишити як було)
logging.basicConfig(filename='contact.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

@main_bp.route('/')
def resume(): 
    agent = request.user_agent 
    return render_template('resume.html', agent=agent)

@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts(): 
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        
        logging.info(f"New Contact: Name={name}, Email={email}, Subject={form.subject.data}")
        flash(f'Дякуємо, {name} ({email})! Ваше повідомлення надіслано.', 'success')
        
        return redirect(url_for('main.contacts')) 

    return render_template('contacts.html', form=form)