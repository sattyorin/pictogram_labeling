from flask import Flask, jsonify, request
from flask_cors import CORS

from text_embedding import TextEmbedding

app = Flask(__name__)
CORS(app, origins=["http://localhost:8081"])


@app.route("/search", methods=["POST"])
def search_picto():
    query = request.json.get("query")
    print(f"query: {query}")

    text_embedding = TextEmbedding()
    text_vec = text_embedding.do_embedding(query)
    if text_vec is None:
        return jsonify(
            {"success": False, "message": "query is empty.", "pictId": "9999"}
        )

    return (
        jsonify(
            {
                "success": True,
                "message": "Search pictogram successfully",
                "pictoId": 9999,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
