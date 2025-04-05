from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

arrayCompra = []
arrayVenta = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/registrarCompra', methods=['POST'])
def registrarCompra():
    data = request.get_json()

    required_fields = ['nombreproveedor', 'identificacion',
                       'numeroOrden', 'nombreProducto', 'cantidad', 'precio']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'El campo {field} es obligatorio.'}), 400

    arrayCompra.append({
        'nombreproveedor': data['nombreproveedor'],
        'identificacion': data['identificacion'],
        'numeroOrden': data['numeroOrden'],
        'nombreProducto': data['nombreProducto'],
        'cantidad': data['cantidad'],
        'precio': data['precio']
    })

    return jsonify({'message': 'Compra registrada con éxito.', 'data': arrayCompra}), 200


@app.route('/registrarVenta', methods=['POST'])
def registrarVenta():
    data = request.get_json()

    required_fields = ['nombreCliente', 'identificacion',
                       'numeroOrden', 'nombreProducto', 'cantidad', 'precio', 'total']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'El campo {field} es obligatorio.'}), 400

    arrayVenta.append({
        'nombreCliente': data['nombreCliente'],
        'identificacion': data['identificacion'],
        'numeroOrden': data['numeroOrden'],
        'nombreProducto': data['nombreProducto'],
        'cantidad': data['cantidad'],
        'precio': data['precio'],
        'total': data['total']
    })

    return jsonify({'message': 'Venta registrada con éxito.', 'data': arrayVenta}), 200


@app.route('/solicitarFactura', methods=['GET'])
def solicitarFactura():
    try:
        response = requests.get('http://192.168.1.22:5000')
        if response.status_code == 200:
            return jsonify({'message': 'Solicitud de factura recibida.', 'data': response.json()}), 200
        else:
            return jsonify({'message': 'Error al solicitar la factura.', 'status_code': response.status_code}), 500
    except Exception as e:
        return jsonify({'message': 'Error al conectar con el servicio externo.', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
