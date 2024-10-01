import subprocess , time , os
from flask import jsonify



class VBox:


    def __init__(self) -> None:
        self.__vboxmanage_path = os.getenv('VBOX_MANAGE')


    def start(self , vm_name):
        try:
            command = [self.__vboxmanage_path, 'startvm', vm_name]
            output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE )

            if (output.stdout.decode().lower()):
                state = self.check_vm_running(vm_name)
                return jsonify({"completed" : state, "message" : f"output : {output.stdout.decode().lower()}"})
                
            if (output.stderr.decode().lower()):
                return jsonify({"completed" : False, "message" : f"output : {output.stderr.decode().lower()}"})

        except subprocess.CalledProcessError as e:
            return  jsonify({"completed" : False, "message" : f"Error : {e}"})
        


    def check_vm_running(self , vm_name):
        command = [self.__vboxmanage_path, 'showvminfo', '--machinereadable', vm_name]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if 'VMState="running"' in result.stdout:  
            return True
        
        return False



    def check_vm_stopping(self , vm_name):
        command = [self.__vboxmanage_path, 'showvminfo', '--machinereadable', vm_name]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if 'VMState="poweroff"' in result.stdout:  
            return True
        
        return False



    def shutdown(self, vm_name):
        try:
            command = [self.__vboxmanage_path, 'controlvm', vm_name , "poweroff"]
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
            time.sleep(10)
            state = self.check_vm_stopping(vm_name)
            if state:
                return jsonify({"completed" : True, "message" : f"VM '{vm_name}' has been successfully powered off."})
            
            return jsonify({"completed" : False, "message" : f"Failed to power off VM '{vm_name}'."})
                
        except subprocess.CalledProcessError as e:
            return  jsonify({"completed" : False, "message" : f"Error : {e}"})
        
