const AWS = require('aws-sdk');

// Opción 1: Usar perfil configurado en ~/.aws/credetials (por ejemplo, 'aws-academy')
//const credentials = new AWS.SharedIniFileCredentials({ profile: 'aws-academy' });
//AWS.config.credentials = credentials;
//AWS.config.update({ region: 'us-east-1' });

// Opción 2: Usar credenciales estáticas en viarables de entorno
AWS.config.update({
  accessKeyId: 'TU_ACCESS_KEY_ID',
  secretAccessKey: 'TU_SECRET_ACCESS_KEY',
  sessionToken: "TU_SESSION_TOKEN",
  region: 'us-east-1',
});


// Crear el cliente de EventBridge
const eventBridge = new AWS.EventBridge();

async function sendTestEvent() {
  const params = {
    Entries: [
      {
        EventBusName: 'arn:aws:events:us-east-1:654654390511:event-bus/default',  // campo obligatorio (valor constante, no tocar)
        Source: 'artist-module',  // campo obligatorio; el valor es un ejemplo nomas.
        DetailType: 'recital',  // campo obligatorio; el valor es un ejemplo nomas.
        Detail: JSON.stringify({ // el detail es un payload dinamico, puede venir cualquier cosa
          artista: 'Monolink',
          lugar: 'Platea A',
          estadio: 'Monumental',
          fecha_presentacion: '2024-09-29',
          fecha_creacion: '2024-09-29',
          fecha_actualizacion: '2024-09-29',
        }),
      },
    ],
  };

  try {
    const response = await eventBridge.putEvents(params).promise();
    console.log('Evento enviado:', JSON.stringify(response, null, 2));

    response.Entries.forEach((entry) => {
      if (entry.EventId) {
        console.log(`Evento enviado exitosamente. Event ID: ${entry.EventId}`);
      } else {
        console.error(`Error al enviar evento: ${entry.ErrorCode} - ${entry.ErrorMessage}`);
      }
    });
  } catch (error) {
    console.error('Error al enviar evento:', error);
  }
}

// Ejecutar la función si se llama desde la línea de comandos
if (require.main === module) {
  sendTestEvent();
}
