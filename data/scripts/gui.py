import bge
from bge.types import *
import aud

from pathlib import Path
from bge.logic import globalDict, expandPath

LUZ_ALPHA = 0.055
FOTON_TEMPO_VIDA = 360
INTERVALO_EMISSAO_UV = 5


def widget(cont):
	# type: (SCA_PythonController) -> None
	
	own = cont.owner
	camera = own.scene.active_camera
	
	over = cont.sensors["Over"] # type: KX_MouseFocusSensor
	lmb = cont.sensors["LMB"] # type: SCA_MouseSensor
	
	if not over.positive:
		own.color[3] = 1.0
		
	elif over.positive:
		
		if not lmb.positive:
			own.color[3] = 0.6
			
			if over.status == 1:
				playSound(cont, "hover.wav")
			
		elif lmb.positive and lmb.status == 1:
			own.color[3] = 0.4
			playSound(cont, "click.wav")
			
			if "Cor" in own and camera["Iniciado"]:
				fotonEmitir(cont)
				
			elif "Iniciar" in own:
				iniciarParar(cont)
				
			elif "TipoEmissao" in own and not camera["Iniciado"]:
				tipoEmissao(cont)
				
			elif "Cena" in own:
				own.scene.replace(own["Cena"])
				
			elif "Sair" in own:
				bge.logic.endGame()
	

def fotonEmitir(cont):
	# type: (SCA_PythonController) -> None
	
	own = cont.owner
	camera = own.scene.active_camera
	objLanterna = own.scene.objects["lampada"] # type: KX_GameObject
	objLuz = own.scene.objects["lampada luz"] # type: KX_GameObject
	objFotonSeta = own.scene.objects["foton seta"] # type: KX_GameObject
	objFotonColisao = own.scene.addObject("foton colisao", "foton spawner", FOTON_TEMPO_VIDA)
	objFotonLampada = objFotonColisao.childrenRecursive["foton lampada"] # type: KX_GameObject
	objFoton = objFotonColisao.childrenRecursive["foton"] # type: KX_GameObject
	
	objLanterna.color = list(own.color)[0:3] + [1.0]
	objFoton.color = list(own.color)[0:3] + [1.0]
	objFotonLampada.color = list(own.color)[0:3]
	objLuz.color = list(own.color)[0:3] + [LUZ_ALPHA]
	
	frameFotonSeta = 0.0
	
	if "IV" in own:
		frameFotonSeta = 1.0
		objLanterna.color = (0.25, 0.0, 0.0, 1.0)
		objFoton.color = (0.25, 0.0, 0.0, 1.0)
		objLuz.color = (0.25, 0.0, 0.0, LUZ_ALPHA)
		
	elif "UV" in own:
		frameFotonSeta = 2.0
		objLanterna.color = (0.0, 0.25, 0.25, 1.0)
		objFoton.color = (0.0, 0.25, 0.25, 1.0)
		objLuz.color = (0.0, 0.25, 0.25, LUZ_ALPHA)
		objFotonColisao["UV"] = True
		own.scene["CorFotonUV"] = list(objFoton.color)
		
		if camera["UVCooldown"] >= 0:
			camera["UVCooldown"] = -INTERVALO_EMISSAO_UV
			
		elif camera["UVCooldown"] < 0:
			objFotonColisao.endObject()
		
	objFotonSeta.playAction("FotonSeta", frameFotonSeta, frameFotonSeta)


def iniciarParar(cont):
	# type: (SCA_PythonController) -> None
	
	own = cont.owner
	camera = own.scene.active_camera
	btnIniciar = own.scene.objects["botão iniciar"] # type: KX_GameObject
	txtIniciar = own.scene.objects["texto iniciar"] # type: KX_FontObject
	lmpIniciar = own.scene.objects["lampada iniciar"] # type: KX_LightObject
	lmpLuz = own.scene.objects["lampada luz"] # type: KX_LightObject
	
	# Iniciar
	if not camera["Iniciado"]:
		camera["Iniciado"] = True
		lmpLuz.visible = True
		btnIniciar.color = (1, 0, 0, 1)
		lmpIniciar.color = (1, 0, 0)
		txtIniciar.color = (1, 0, 0, 1)
		txtIniciar.text = "Parar"
		own.sendMessage("Iniciar")
		
	# Parar
	else:
		camera["Iniciado"] = False
		camera["UVCooldown"] = 0
		lmpLuz.visible = False
		btnIniciar.color = (0, 1, 0, 1)
		lmpIniciar.color = (0, 1, 0)
		txtIniciar.color = (0, 1, 0, 1)
		txtIniciar.text = "Iniciar"
		own.sendMessage("Parar")


def tipoEmissao(cont):
	# type: (SCA_PythonController) -> None
	
	own = cont.owner
	camera = own.scene.active_camera
	txtTipoEmissao = own.scene.objects["texto tipo emissao"] # type: KX_FontObject
	
	if camera["TipoEmissao"] == "Espontânea":
		camera["TipoEmissao"] = "Estimulada"
	
	elif camera["TipoEmissao"] == "Estimulada":
		camera["TipoEmissao"] = "Espontânea"
		
	txtTipoEmissao.text = camera["TipoEmissao"]


def playSound(cont, soundFile):
	# type: (SCA_PythonController, str) -> None
	
	own = cont.owner
	scene = own.scene
	
	if not "Sounds" in scene:
		scene["Sounds"] = {}
	
	soundPath = Path(expandPath("//sounds/") + soundFile)
	
	if soundPath.exists():
		
		if not soundFile in scene["Sounds"].keys():
			scene["Sounds"][soundFile] = aud.Factory(soundPath.as_posix())
			
		aud.device().volume = 0.1
		aud.device().play(scene["Sounds"][soundFile])
		
