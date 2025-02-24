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
    title = db.Column(db.String(255))
    link = db.Column(db.String(512))
    description = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/api/rss-items', methods=['GET'])
def get_rss_items():
    items = RssItem.query.all()
    return jsonify([{
        'id': item.id,
        'title': item.title,
        'link': item.link,
        'description': item.description,
        'pub_date': item.pub_date.isoformat() if item.pub_date else None
    } for item in items])

@app.route('/api/rss-items/<int:id>', methods=['GET'])
def get_rss_item(id):
    item = RssItem.query.get_or_404(id)
    return jsonify({
        'id': item.id,
        'title': item.title,
        'link': item.link,
        'description': item.description,
        'pub_date': item.pub_date.isoformat() if item.pub_date else None
    })

@app.route('/api/rss-items/<int:id>', methods=['PUT'])
def update_rss_item(id):
    item = RssItem.query.get_or_404(id)
    data = request.json
    
    if 'title' in data:
        item.title = data['title']
    if 'link' in data:
        item.link = data['link']
    if 'description' in data:
        item.description = data['description']
    
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