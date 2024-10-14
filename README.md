# IntApp-EDA

# Requerimientos
- Docker (https://www.docker.com/)
- Serverless (https://serverless.com/ -> Registrarse / Crear Cuenta)
- Node JS y NPM (v21.1.0+)
- Python 3.10+

- Modificar numero de cuenta de sandbox en serverless.yaml: 
![alt text](.doc/image.png)

Instalar: 
npm install serverless
npm install serverless-python-requirements
npm install serverless-scriptable-plugin

# Configurar CLI
Se necesita actualizar el Sandbox API Key, API Secret, API Access Token set. Crear un perfil "aws-academy" en .aws/config:
[profile aws-academy]
region = us-east-1
output = json

Copiar credenciales del sandbox y pegar en .aws/credentials:
[aws-academy]
aws_access_key_id=ASIA24FA4IFROT4LWUOH
aws_secret_access_key=dGwxWWFVgESV*******zT2M5ZJDuhxLo6vq9
aws_session_token=IQoJb3JpZ2lL8JN/li/G0zC0uZ*******361zZ2XuQjJtdKxzXJtYFTW02M+izA==


# Ejecutar
serverless deploy
