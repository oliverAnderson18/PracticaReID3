from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
import schemas
import db
import uuid
import google.generativeai as genai

gemini_bp = Blueprint("gemini", __name__)

@gemini_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate_gemini():
    data = request.json
    schema = schemas.SendMessageSchema()
    try:
        schema.load(data)
        if get_jwt_identity():
            genai.configure(api_key="AIzaSyC2GM-noH3Y4oGgqtKr3trZnWMEoYdafWQ")
            model = genai.GenerativeModel("gemini-1.5-flash")
            result = model.generate_content(data["content"])
            uid = uuid.uuid4().hex
            db.messages[uid] = {"content": data["content"], "ToGemini": True, "Response": result.text}
            return jsonify({uid: {"ToGemini": True, "Response": result.text}}), 200
        else:
            return jsonify({"Error": "unauthorized token"}), 401
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400