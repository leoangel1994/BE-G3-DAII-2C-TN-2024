import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.eventbridge.EventBridgeClient;
import software.amazon.awssdk.services.eventbridge.model.PutEventsRequest;
import software.amazon.awssdk.services.eventbridge.model.PutEventsRequestEntry;
import software.amazon.awssdk.services.eventbridge.model.PutEventsResponse;
import software.amazon.awssdk.services.eventbridge.model.PutEventsResultEntry;

import java.util.List;

public class EventBridgeExample {

    public static void main(String[] args) {

        // Opción 1: Usar perfil configurado en ~/.aws/credentials (por ejemplo, 'aws-academy')
        //EventBridgeClient client = EventBridgeClient.builder()
        //       .region(Region.US_EAST_1)
        //      .credentialsProvider(ProfileCredentialsProvider.create("aws-academy"))
        //      .build();

        // Opción 2: Usar credenciales en variables de entorno
        
        AwsBasicCredentials awsCreds = AwsBasicCredentials.create("TU_ACCESS_KEY_ID", "TU_SECRET_ACCESS_KEY", "TU_SESSION_TOKEN");
        EventBridgeClient client = EventBridgeClient.builder()
                .region(Region.US_EAST_1)
                .credentialsProvider(StaticCredentialsProvider.create(awsCreds))
                .build();
        

        sendTestEvent(client);
        client.close();
    }

    private static void sendTestEvent(EventBridgeClient client) {
        // en el campo detail peude ir cualquier cosa
        String detail = """
                {
                    "artista": "Monolink",
                    "lugar": "Platea A",
                    "estadio": "Monumental",
                    "fecha_presentacion": "2024-09-29",
                    "fecha_creacion": "2024-09-29",
                    "fecha_actualizacion": "2024-09-29"
                }
                """;

        PutEventsRequestEntry entry = PutEventsRequestEntry.builder()
                .eventBusName("arn:aws:events:us-east-1:654654390511:event-bus/default")  // no tocar
                .source("artist-module") // obligatorio, el valor es un ejemplo
                .detailType("recital")  // obligatorio  el valor es un ejemplo
                .detail(detail)
                .build();

        PutEventsRequest request = PutEventsRequest.builder()
                .entries(entry)
                .build();

        try {
            PutEventsResponse response = client.putEvents(request);
            List<PutEventsResultEntry> resultEntries = response.entries();

            for (PutEventsResultEntry result : resultEntries) {
                if (result.eventId() != null) {
                    System.out.println("Evento enviado exitosamente. Event ID: " + result.eventId());
                } else {
                    System.err.println("Error al enviar evento: " + result.errorCode() + " - " + result.errorMessage());
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
