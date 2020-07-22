package kundu;

import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;

import androidx.annotation.NonNull;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

import kundu.masky.MainActivity;

public class MessagingService extends FirebaseMessagingService {
    public void onMessageReceived(@NonNull RemoteMessage remoteMessage) {
        super.onMessageReceived(remoteMessage);
        shownotification(this, remoteMessage.getNotification().getTitle(),remoteMessage.getNotification().getBody());

        String click_action = remoteMessage.getNotification().getClickAction();
        Intent i = new Intent(click_action);
//        startActivity(i);

    }

    public void shownotification(Context context, String title, String message){


        Intent intent =new Intent(context, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(context,100,intent, PendingIntent.FLAG_CANCEL_CURRENT);
        NotificationCompat.Builder builder=new NotificationCompat.Builder(this,"MyNotifications")
                .setContentTitle(title)
//                .setSmallIcon(R.drawable.innovacion)
//                .setAutoCancel(true)
                .setContentIntent(pendingIntent)
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setContentText(message);
        NotificationManagerCompat manager= NotificationManagerCompat.from(this);
        manager.notify(999,builder.build());
    }

}
