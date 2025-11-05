from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import ContactForm
import logging

@app.route('/')
def resume():
    return render_template('resume.html', title="My Resume")


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data


        logging.info(f"New contact form submission: Name={name}, Email={email}, Phone={phone}")


        flash(f'Thanks, {name}! Your message has been sent.', 'success')


        return redirect(url_for('contacts'))

    return render_template('contacts.html', title="Contacts", form=form)