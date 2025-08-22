from flask import Flask, request, jsonify
from ports.entrypoints import ReconciliationEntrypoint
from core.domain.services import ReconciliationService
from adapters.repositories.csv_repository import CsvRepository
import os

def create_app():
    app = Flask(__name__)
    repository = CsvRepository('data/literary_works.csv')
    service = ReconciliationService(repository)
    entrypoint = ReconciliationEntrypoint(service)

    @app.route('/reconcile', methods=['GET'])
    def reconcile_get():
        query = request.args.get('query', '')
        limit = int(request.args.get('limit', 3))
        result = entrypoint.reconcile({'query': query, 'limit': limit})
        return jsonify({'result': result})

    @app.route('/reconcile', methods=['POST'])
    def reconcile_post():
        data = request.get_json()
        if not data or 'queries' not in data:
            return jsonify({'error': 'Invalid request'}), 400
        results = {}
        for query_id, query_data in data['queries'].items():
            results[query_id] = {'result': entrypoint.reconcile(query_data)}
        return jsonify(results)

    @app.route('/')
    def index():
        return jsonify({'message': 'Publication Reconciliation Service'})

    return app
