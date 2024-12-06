from flask import Blueprint, render_template, request, Response, stream_with_context
from app.models.zhipu_model import ZhipuModel, AIModelException
import json

bp = Blueprint('chat', __name__, url_prefix='')

@bp.route('/')
def index():
    return render_template('chat/index.html')

@bp.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        ai_model = ZhipuModel()
        
        def generate():
            try:
                for chunk in ai_model.chat_stream(message):
                    yield f"data: {json.dumps({'status': 'success', 'content': chunk})}\n\n"
            except AIModelException as e:
                yield f"data: {json.dumps({'status': 'error', 'content': str(e)})}\n\n"
        
        return Response(stream_with_context(generate()), mimetype='text/event-stream')
            
    except Exception as e:
        return {'status': 'error', 'content': str(e)}, 500 