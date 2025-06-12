from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models import URL, db
import random
import string

dashboard = Blueprint('dashboard', __name__)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@dashboard.route('/')
@login_required
def dashboard_view():
    urls = URL.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', urls=urls)

@dashboard.route('/shorten', methods=['POST'])
@login_required
def shorten():
    original = request.form['original']
    custom_code = request.form.get('custom_code', '').strip()

    if custom_code:
        if URL.query.filter_by(short_code=custom_code).first():
            return "Mã rút gọn này đã tồn tại. Hãy chọn mã khác.", 400
        code = custom_code
    else:
        code = generate_short_code()
        while URL.query.filter_by(short_code=code).first():
            code = generate_short_code()

    new_url = URL(original=original, short_code=code, user_id=current_user.id)
    db.session.add(new_url)
    db.session.commit()
    return redirect(url_for('dashboard.dashboard_view'))
@dashboard.route('/<code>')
def redirect_url(code):
    url = URL.query.filter_by(short_code=code).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original)