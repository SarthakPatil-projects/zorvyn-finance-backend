from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.models.record import Record
from app.middleware.role_guard import role_required
from app.utils.errors import success_response
from sqlalchemy import func
from app import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
@role_required('viewer', 'analyst', 'admin')
def summary():
    total_income = db.session.query(func.sum(Record.amount)).filter_by(type='income', is_deleted=False).scalar() or 0
    total_expense = db.session.query(func.sum(Record.amount)).filter_by(type='expense', is_deleted=False).scalar() or 0
    net_balance = total_income - total_expense

    return success_response({
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance
    })

@dashboard_bp.route('/categories', methods=['GET'])
@jwt_required()
@role_required('viewer', 'analyst', 'admin')
def categories():
    results = db.session.query(
        Record.category,
        Record.type,
        func.sum(Record.amount)
    ).filter_by(is_deleted=False).group_by(Record.category, Record.type).all()

    data = [{'category': r[0], 'type': r[1], 'total': r[2]} for r in results]
    return success_response(data)

@dashboard_bp.route('/recent', methods=['GET'])
@jwt_required()
@role_required('viewer', 'analyst', 'admin')
def recent():
    records = Record.query.filter_by(is_deleted=False).order_by(Record.created_at.desc()).limit(5).all()
    return success_response([r.to_dict() for r in records])

@dashboard_bp.route('/trends', methods=['GET'])
@jwt_required()
@role_required('analyst', 'admin')
def trends():
    results = db.session.query(
        func.strftime('%Y-%m', Record.date),
        Record.type,
        func.sum(Record.amount)
    ).filter_by(is_deleted=False).group_by(
        func.strftime('%Y-%m', Record.date),
        Record.type
    ).all()

    data = [{'month': r[0], 'type': r[1], 'total': r[2]} for r in results]
    return success_response(data)