from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rss_items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class RssItem(db.Model):
    __tablename__ = 'rss_items'
    
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(512))
    title = db.Column(db.String(512))
    link = db.Column(db.String(512))
    iso_date = db.Column(db.DateTime)
    categories = db.Column(db.JSON)
    image_url = db.Column(db.Text)
    rapidgator_url = db.Column(db.String(512))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    description = db.Column(db.Text)
    author = db.Column(db.String(255))
    series = db.Column(db.String(255))
    audiobook_id = db.Column(db.Integer)
    tags = db.Column(db.JSON)
    averagerating_amazon = db.Column(db.Float)
    numreviews_amazon = db.Column(db.Integer)
    averagerating_goodread = db.Column(db.Float)
    numreviews_goodread = db.Column(db.Integer)
    status = db.Column(db.String(50))
    genres_amazon = db.Column(db.JSON)
    positivereviews_amazon = db.Column(db.JSON)
    negativereviews_amazon = db.Column(db.JSON)
    genres_goodread = db.Column(db.JSON)
    positivereviews_goodread = db.Column(db.JSON)
    negativereviews_goodread = db.Column(db.JSON)
    empfehlung = db.Column(db.String(255))
    reason = db.Column(db.Text)
    over_all_score = db.Column(db.Float)

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/api/rss-items', methods=['GET'])
def get_rss_items():
    status = request.args.get('status', 'new')
    if status == 'all':
        items = RssItem.query.all()
    else:
        items = RssItem.query.filter_by(status=status).all()
    return jsonify([{
        'id': item.id,
        'guid': item.guid,
        'title': item.title,
        'link': item.link,
        'iso_date': item.iso_date.isoformat() if item.iso_date else None,
        'categories': item.categories,
        'image_url': item.image_url,
        'rapidgator_url': item.rapidgator_url,
        'created_at': item.created_at.isoformat() if item.created_at else None,
        'updated_at': item.updated_at.isoformat() if item.updated_at else None,
        'description': item.description,
        'author': item.author,
        'series': item.series,
        'audiobook_id': item.audiobook_id,
        'tags': item.tags,
        'averagerating_amazon': item.averagerating_amazon,
        'numreviews_amazon': item.numreviews_amazon,
        'averagerating_goodread': item.averagerating_goodread,
        'numreviews_goodread': item.numreviews_goodread,
        'status': item.status,
        'genres_amazon': item.genres_amazon,
        'positivereviews_amazon': item.positivereviews_amazon,
        'negativereviews_amazon': item.negativereviews_amazon,
        'genres_goodread': item.genres_goodread,
        'positivereviews_goodread': item.positivereviews_goodread,
        'negativereviews_goodread': item.negativereviews_goodread,
        'empfehlung': item.empfehlung,
        'reason': item.reason,
        'over_all_score': item.over_all_score
    } for item in items])

@app.route('/api/rss-items/<int:id>', methods=['GET'])
def get_rss_item(id):
    item = RssItem.query.get_or_404(id)
    return jsonify({
        'id': item.id,
        'guid': item.guid,
        'title': item.title,
        'link': item.link,
        'iso_date': item.iso_date.isoformat() if item.iso_date else None,
        'categories': item.categories,
        'image_url': item.image_url,
        'rapidgator_url': item.rapidgator_url,
        'created_at': item.created_at.isoformat() if item.created_at else None,
        'updated_at': item.updated_at.isoformat() if item.updated_at else None,
        'description': item.description,
        'author': item.author,
        'series': item.series,
        'audiobook_id': item.audiobook_id,
        'tags': item.tags,
        'averagerating_amazon': item.averagerating_amazon,
        'numreviews_amazon': item.numreviews_amazon,
        'averagerating_goodread': item.averagerating_goodread,
        'numreviews_goodread': item.numreviews_goodread,
        'status': item.status,
        'genres_amazon': item.genres_amazon,
        'positivereviews_amazon': item.positivereviews_amazon,
        'negativereviews_amazon': item.negativereviews_amazon,
        'genres_goodread': item.genres_goodread,
        'positivereviews_goodread': item.positivereviews_goodread,
        'negativereviews_goodread': item.negativereviews_goodread,
        'empfehlung': item.empfehlung,
        'reason': item.reason,
        'over_all_score': item.over_all_score
    })

@app.route('/api/rss-items/<int:id>', methods=['PUT'])
def update_rss_item(id):
    item = RssItem.query.get_or_404(id)
    data = request.json
    
    # Liste der editierbaren Felder
    editable_fields = [
        'title', 'description', 'status', 'empfehlung', 'reason',
        'tags', 'genres_amazon', 'genres_goodread'
    ]
    
    for field in editable_fields:
        if field in data:
            setattr(item, field, data[field])
    
    item.updated_at = db.func.now()
    db.session.commit()
    return jsonify({'message': 'Updated successfully'})

@app.route('/api/rss-items/<int:id>', methods=['DELETE'])
def delete_rss_item(id):
    item = RssItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'})

def init_db():
    with app.app_context():
        db.create_all()
        # Add some sample data if the table is empty
        if not RssItem.query.first():
            sample_items = [
                RssItem(
                    title='Beispiel RSS Item 1',
                    link='https://example.com/1',
                    description='Dies ist ein Beispiel-RSS-Item.',
                    pub_date=db.func.now()
                ),
                RssItem(
                    title='Beispiel RSS Item 2',
                    link='https://example.com/2',
                    description='Dies ist ein weiteres Beispiel-RSS-Item.',
                    pub_date=db.func.now()
                )
            ]
            db.session.add_all(sample_items)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=53509)