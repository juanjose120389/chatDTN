#Autor Juan José Sáenz
#API dropbox v2
#version chat 1.1

import dropbox#libreria de dropbox(debe ser instalada)
import os #libreria de funciones dle sistema
import sys #libreria para tomar los parametros de entrada
APP_KEY = 'yvfnfb3rgh8oz5t' #cambiar con la generada en su aplicacion
APP_SECRET = 'ri1cfy8zluzn6lf' #cambiar con la generada en su aplicacion
pathactual=os.getcwd()


#transferencia
#clase con las funciones de manejo del chat
class TransferData:
    def __init__(self, dbx, access_token):#funcion de inicializacion
        self.access_token = access_token
    def existe (self, usuario):#funcion para saber si el usuario existe en el archivo de usuarios
        var=False#auxilar de inicializacion
        token=""
        with open("input.dat", 'r') as input_file:#abrir archivo de usuarios
        	for line in input_file:
				
        		u,t = line.split(" ")#separa nombre de usuario y token
        		t = t.strip()#quitar el \n del final
        		if u==usuario: #si el usuario existe
        			var=True
        			token=t
					
        if var==True:
        	return token#si el usuario existe devolver el token
        else:
        	return "fail"
    def upload_file(self, dbx, file_from, file_to):#funcion para subir archivo cuando sea reemplazado

        
        with open(file_from, 'rb') as f: 
            dbx.files_upload(f.read(), file_to,  mode=dropbox.files.WriteMode.overwrite)

    def descargar(self,dbx,archivo):#funcion para descargar el archivo de chat cuando se abre

    	dbx.files_download_to_file(pathactual+'/chat.txt', '/ChatDTN/chat.txt')#origen y destino del archivo que sera descargado( se trabajara en una copia local)
    	print("\nBienvenido al ChatDTN, a continuación se presentarán los mensajes almacenados")
    	f = open ('chat.txt','r')#apertura de archivo en modo lectura
    	mensaje = f.read()#mostrar todos los mensajes
    	print(mensaje)
    	f.close()
       # dbx.files_download('/chat4.txt')

    def grabarMensaje(self, dbx, usuario, mensaje):#funcion para subir mensajes al archivo
        f = open('chat.txt','a')#apertura archivo lectura escritura
        f.write('\n' + usuario+': '+mensaje)#escribir mensaje en archivo
        f.close()

    def email(self,dbx ):#regresar mensaje con el mail del usuario conectado
       #dbx = dropbox.Dropbox(self.access_token)
        try:
            dbx.users_get_current_account()#mostrar la cuenta adjunta a la conexion
            #print(dbx.users_get_current_account().email)
            return dbx.users_get_current_account().email
        except dropbox.exceptions.AuthError as err:
            raise StandardError('error')
            return ""

    def escribirMensaje(self, dbx, usuario):#escribir mensaje en pantalla
        mensaje=''
        print ("\nEnviar los mensajes que desee, para cerrar escriba salirchat")
        while (mensaje!='salirchat'):#escribir mientras no se salga del chat con salirchat
	        print("Mensaje: ")
	        mensaje = input() #lectura de linea
	        if mensaje!='salirchat':

	        	self.grabarMensaje(dbx, usuario, mensaje)#cuando se sale se graba en el archivo
        print('\nTodos los mensajes fueron enviados, adios!!!')

    def borrarChat(self, dbx):#borrar todo archivo de chat
        f = open('chat.txt','w')#se crea un archivo en blanco
        #f.write('\n' + usuario+': '+mensaje)
        f.close()

    def registrarUsuario(self):#cuando hay un nuevo usuario se debe registrar con su token
        auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)#crear un flujo de aplicacion con el app key y secret
        authorize_url = auth_flow.start()#generar una url de registro para permitir aplicacion
        print("Para registrar a un usuario nuevo permitido, realice los siguientes pasos: ")
        print ("1. Ingrese en su navegador al siguiente enlace (debe tener una sesión dropbox abierta en el navegador) : " + authorize_url)
        print ("2. Clic en Permitir( \"Allow\" )")
        print ("3. Copiar el código de autorización de la aplicación( authorization code).")
        auth_code = input("Pegar aquí el código de autorización y dar enter: ").strip()#copiar el auth para generar un token
        try:
            oauth_result = auth_flow.finish(auth_code)#la api de dropbox genera el token con el auth
            print("Código ingresado correctamente, el usuario tiene el siguiente token(envíelo al administrador para que le ingrese en el archivo input.dat de usuarios y le de su nombre de usuario):")#token que genera mendiante la misma api
            print(oauth_result.access_token)
        except Exception as e:
            print('Error el código ingresado no es correcto vuelva a realizar el proceso')
            sys.exit(1)

def main():#funcion principal

    if len(sys.argv)==1 or len(sys.argv)>3:#numero de parametros minimo 2 y máximo 3 caso contrario error
    	print("Ayuda ChatDTN\nComandos disponibles: \nPara registrar un nuevo usuario use: python3 chatdtn.py registrar\nPara ver y enviar mensajes(debe tener ya un token de activación) use: python3 chatdtn.py iniciar <usuario>\nPara borrar todo el historial de chat use: python3 chatdtn.py borrar <usuario> ")
   

    elif sys.argv[1] == 'registrar':
    	#dbx = dropbox.Dropbox(auth_code)
    	transferData = TransferData("", '')
    	transferData.registrarUsuario()#llamar  a registro de usuario
    elif sys.argv[1]== 'iniciar':
    	#auth_code= sys.argv[2]
    	transferData = TransferData("", "")
    	token=transferData.existe(sys.argv[2])#recupera token del archivo
    	#print(str(existe),":")
    	try:

    		dbx = dropbox.Dropbox(token)#generar conexion de dropbox con la api
    		transferData = TransferData(dbx, token)#inicializacion de clase de transferencia
    		print("Usuario asociado a la cuenta: ",transferData.email(dbx))
    		file_from = 'chat.txt'#archivo local
    		file_to = '/ChatDTN/chat.txt'#destino en el dropbox
    		transferData.descargar(dbx, file_to)#descarga el archivo del chat
    		transferData.escribirMensaje(dbx,sys.argv[2]+ " (" +transferData.email(dbx)+")")#graba en el archivo
	    
	    # API v2
    		transferData.upload_file(dbx,file_from, file_to)#subir el archivo

    	except dropbox.exceptions.BadInputError :#excepcion con mal registro
    		print('Usuario no registrado, debe registrar usuario mediante la ejecución python3 chat.py registrar')
    		sys.exit(1)
    	except dropbox.exceptions.AuthError :#token no existente
    		print('Usuario no registrado, debe registrar usuario mediante la ejecución python3 chat.py registrar')    	
    elif sys.argv[1]== 'borrar':#opcion borrar
    	#auth_code= sys.argv[2]
    	transferData = TransferData("", "")
    	token=transferData.existe(sys.argv[2])#busca si el usuario existe
    	if token!="fail":  #si token existe
    		try:

    			dbx = dropbox.Dropbox(token)#conexion a dropbox
    			transferData = TransferData(dbx, token)#inicializacion
    			file_from = 'chat.txt'#archivo local
    			file_to = '/ChatDTN/chat.txt'#archivo en la cuenta dropbox
    			print('Esta seguro que desea borrar todo (s/n)')
    			mensaje = input()#toma del usuario si desea borrar
    			if mensaje=='s' or mensaje=='S' :#recepta s mayuscila y minuscula

    				transferData.borrarChat(dbx)#borra el archivo
				
    				transferData.upload_file(dbx,file_from, file_to)
    				print('Todos los mensajes han sido borrados')

    		except dropbox.exceptions.BadInputError :
    			print('Usuario no registrado, debe registrar usuario mediante la ejecución python3 chat.py registrar')
    			sys.exit(1)
    	else:
    		print('Usuario no registrado, debe registrar usuario mediante la ejecución python3 chat.py registrar')		
    else:
    
    	print("Ayuda ChatDTN\nComandos disponibles: \nPara registrar un nuevo usuario use: python3 chatdtn.py registrar\nPara ver y enviar mensajes(debe tener ya un token de activación) use: python3 chatdtn.py iniciar <token>\nPara borrar todo el historial de chat use: python3 chatdtn.py borrar <token> ")
	
if __name__ == '__main__':
	main()

