import bge
from bge.types import *

from math import radians
from random import randrange
from bge.logic import globalDict
from .gui import FOTON_TEMPO_VIDA

ELETRON_VELOCIDADE = 0.03
DISTANCIA_NIVEL_ELETRON = 3.0


def main(cont):
	# type: (SCA_PythonController) -> None
	
	own = cont.owner
	camera = own.scene.active_camera
	eletronAux = own.childrenRecursive["eletron aux"] # type: KX_GameObject
	textoUV = own.scene.objects["texto UV"] # type: KX_FontObject
	
	always = cont.sensors["Always"] # type: SCA_AlwaysSensor
	message = cont.sensors["Message"] # type: KX_NetworkMessageSensor
	
	if always.positive:
		
		if camera["UVCooldown"] >= 0.0:
			textoUV.color = (1, 1, 1, 1)
		
		elif camera["UVCooldown"] < 0.0:
			textoUV.color = (1, 0, 0, 1)
		
		if camera["Iniciado"]:
			own.applyRotation((0, 0, -ELETRON_VELOCIDADE), True)
		
			if message.positive:
				for msg in message.subjects:
					
					if msg == "MoverE1" and camera["NivelEletron"] == 2:
						camera["NivelEletron"] = 1
						eletronAux.localPosition.y -= DISTANCIA_NIVEL_ELETRON
						camera["UVCooldown"] = 0.0
						
					if msg == "MoverE2" and camera["NivelEletron"] == 1:
						camera["NivelEletron"] = 2
						eletronAux.localPosition.y += DISTANCIA_NIVEL_ELETRON
						
					if msg == "EmitirFotonsEstimulada":
						emitirFotonsEstimulada(cont, eletronAux)
						own.sendMessage("MoverE1")
			
			if camera["UVCooldown"] >= 0 and camera["NivelEletron"] == 2 and camera["TipoEmissao"] == "Espontânea":
				emitirFotonEspontanea(cont, eletronAux)
				own.sendMessage("MoverE1")
			
		if not camera["Iniciado"]:
			own.localOrientation = [0, 0, 0]


def emitirFotonEspontanea(cont, ref):
	# type: (SCA_PythonController, KX_GameObject) -> None
	
	objFoton = cont.owner.scene.addObject("foton colisao", ref, FOTON_TEMPO_VIDA) # type: KX_GameObject
	objFoton["Seguir"] = False
	objFoton["Velocidade"] = 0.15
	objFoton.applyRotation((0, 0, radians(randrange(0, 360))), True)
	
	for obj in objFoton.childrenRecursive:
		try:
			obj.color = cont.owner.scene["CorFotonUV"]
		except:
			obj.color = cont.owner.scene["CorFotonUV"][0:3]


def emitirFotonsEstimulada(cont, ref):
	# type: (SCA_PythonController, KX_GameObject) -> None
	
	objFoton1 = cont.owner.scene.addObject("foton colisao", ref, FOTON_TEMPO_VIDA) # type: KX_GameObject
	objFoton2 = cont.owner.scene.addObject("foton colisao", ref, FOTON_TEMPO_VIDA) # type: KX_GameObject
	objsFotons = [objFoton1, objFoton2] # type: list[KX_GameObject]
	rotacaoFotons = radians(randrange(0, 360))
	
	objFoton2.localPosition.x += 1.0
	
	for fotCol in objsFotons:
		fotCol["Seguir"] = False
		fotCol["Velocidade"] = 0.15
		fotCol.applyRotation((0, 0, rotacaoFotons), True)
		
		for obj in fotCol.childrenRecursive:
			try:
				obj.color = cont.owner.scene["CorFotonUV"]
			except:
				obj.color = cont.owner.scene["CorFotonUV"][0:3]
