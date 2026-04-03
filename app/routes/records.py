from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app import db
from app.models.record import Record
from app.middleware.role_guard import role_required
from app.utils.errors import error_response, success_response
from datetime import datetime

records_bp = Blueprint('records', __name__)

@records_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_record():
    data = request.get_json()

    if not data or not data.get('amount') or not data.get('type') or not data.get('category') or not data.get('date'):
        return error_response("Amount, type, category and date are required", 400)

    if data['type'] not in ['income', 'expense']:
        return error_response("Type must be income or expense", 400)

    try:
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return error_response("Date format must be YYYY-MM-DD", 400)

    record = Record(
        amount=data['amount'],
        type=data['type'],
        category=data['category'],
        date=date,
        notes=data.get('notes', '')
    )
    db.session.add(record)
    db.session.commit()
    return success_response(record.to_dict(), "Record created successfully", 201)

@records_bp.route('/', methods=['GET'])
@jwt_required()
@role_required('viewer', 'analyst', 'admin')
def get_records():
    query = Record.query.filter_by(is_deleted=False)

    category = request.args.get('category')
    type_ = request.args.get('type')
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    if category:
        query = query.filter_by(category=category)
    if type_:
        query = query.filter_by(type=type_)
    if from_date:
        query = query.filter(Record.date >= datetime.strptime(from_date, '%Y-%m-%d').date())
    if to_date:
        query = query.filter(Record.date <= datetime.strptime(to_date, '%Y-%m-%d').date())

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return success_response({
        'records': [r.to_dict() for r in paginated.items],
        'total': paginated.total,
        'page': page,
        'pages': paginated.pages
    })

@records_bp.route('/<int:record_id>', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def update_record(record_id):
    record = Record.query.filter_by(id=record_id, is_deleted=False).first()
    if not record:
        return error_response("Record not found", 404)

    data = request.get_json()
    if data.get('amount'):
        record.amount = data['amount']
    if data.get('type') and data['type'] in ['income', 'expense']:
        record.type = data['type']
    if data.get('category'):
        record.category = data['category']
    if data.get('notes'):
        record.notes = data['notes']
    if data.get('date'):
        record.date = datetime.strptime(data['date'], '%Y-%m-%d').date()

    db.session.commit()
    return success_response(record.to_dict(), "Record updated successfully")

@records_bp.route('/<int:record_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_record(record_id):
    record = Record.query.filter_by(id=record_id, is_deleted=False).first()
    if not record:
        return error_response("Record not found", 404)

    record.is_deleted = True
    db.session.commit()
    return success_response(None, "Record deleted successfully")