# api_gateway.py
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

#with open("log.txt", 'a') as f:
#    f.write("1\n")

class APIGateway:
    # Define service locations
    SERVICES = {
        'book_service': 'http://book-service:5001/api/books', 
        'order_service': 'http://review-service:5002/api/reviews',
        'web_service': 'http://localhost:3000'
    }

    @staticmethod
    def forward_request(service_name, path):
        services = APIGateway.SERVICES

        # Simple request forwarding to services
        if service_name not in services:
            return {'error': f'Service name {service_name} not recognized'}
        url = f"{services[service_name]}{path}"
        try:
            response = requests.get(url)
            try:
                return response.json()
            except Exception as e:
                #return {'error': f'failed to convert to json: {response} {dir(e)}'}
                return {}
        except Exception as e:
            return {'error': f'Service unavailable: {e}'}

@app.route('/api/books/<int:book_id>')
def get_book(book_id):
    return jsonify(APIGateway.forward_request(
        service_name = 'book_service', 
        path = f'/books/{book_id}'
    ))

@app.route('/api/reviews/<book_id>')
def get_book_reviews(book_id):
    # get book details
    book = APIGateway.forward_request(
        service_name = 'review_service', 
        path = f'/books/{book_id}'
    )

    # get book reviews
    reviews = APIGateway.forward_request(
        service_name = 'review_service', 
        path = '/reviews/book/{book_id}'
    )

    # combine the responses
    return jsonify({
        'book': book, 
        'reviews': reviews
    })

@app.route('/')
def get_web_interface():
    return jsonify(APIGateway.forward_request(
        service_name = 'web_service', 
        path = '/'
    ))


if __name__ == "__main__":
    app.run(port=8000)






    


