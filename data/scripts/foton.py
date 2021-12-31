import bge

from bge.logic import globalDict
from bge.types import *


def main(cont):
	# type: (SCA_PythonController) -> None
	
	own = cont.owner
	camera = own.scene.active_camera
	eletron = own.scene.objects["eletron"] # type: KX_GameObject
	
	always = cont.sensors["Always"] # type: SCA_AlwaysSensor
	message = cont.sensors["Message"] # type: KX_NetworkMessageSensor
	collisionEletron = cont.sensors["CollisionEletron"] # type: KX_TouchSensor
	
	if always.positive:
		
		if message.positive:
			for msg in message.subjects:
				if msg == "Parar":
					own.endObject()
					return
		
		if own["Seguir"]:
			own.alignAxisToVect(eletron.worldPosition - own.worldPosition, 0)
			own.alignAxisToVect((0, 0, 1), 2)
		
		if own["Mover"]:
			own.applyMovement((own["Velocidade"], 0, 0), True)
			
		if collisionEletron.positive:
			own["Seguir"] = False
			
			if own["UV"]:
				if camera["NivelEletron"] == 1:
					own.sendMessage("MoverE2")
					
				elif camera["NivelEletron"] == 2:
					own.sendMessage("EmitirFotonsEstimulada")
					
				own.endObject()
				return
