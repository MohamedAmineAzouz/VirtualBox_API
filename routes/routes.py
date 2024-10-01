from flask import Flask , request , Response
from decorators.decorators import access_required
from modules.virtualbox.vbox import VBox

app = Flask(__name__)


@app.route('/api/v1/startVM', methods=[ "GET" ])
@access_required
def startVirtualMachine():
    vm_name = request.args.get('vm_name')
    response = VBox().start(vm_name)

    return response



@app.route('/api/v1/shutdownVM', methods=[ "GET" ])
@access_required
def shutdownVirtualMachine():
    vm_name = request.args.get('vm_name')
    response = VBox().shutdown( vm_name )

    return response