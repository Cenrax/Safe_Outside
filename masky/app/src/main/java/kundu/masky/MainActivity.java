package kundu.masky;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.messaging.FirebaseMessaging;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    final int startDelay = 2000;
    final int delay = 5000;

    Handler handler = new Handler();
    Runnable runnable;
    TextView textView;
    ImageView back;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = findViewById(R.id.textview);
        back = findViewById(R.id.back);
        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                MainActivity.super.onBackPressed();
            }
        });
        FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();


        ///////////////NOTIFICATIONS///////////////////

        if(Build.VERSION.SDK_INT>=Build.VERSION_CODES.O){
            NotificationChannel channel=new NotificationChannel("MyNotifications","MyNotifications", NotificationManager.IMPORTANCE_DEFAULT);
            NotificationManager manager=getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);
        }

        FirebaseMessaging.getInstance().subscribeToTopic("users")
                .addOnCompleteListener(new OnCompleteListener<Void>() {
                    public void onComplete(@NonNull Task<Void> task) {
                        String msg = "msg sent successfully";
                        if (!task.isSuccessful()) {
                            msg = "msg failed";
                        }
                    }
                });




        handler.postDelayed(runnable = () -> {
            // Repeating code starts here

            FirebaseFirestore db = FirebaseFirestore.getInstance();
            db.collection("users").document(user.getUid())
                    .get()
                    .addOnCompleteListener(task -> {
                        if (task.isSuccessful()) {
                            DocumentSnapshot document = task.getResult();
                            if (document.exists()) {
                                String status = document.getString("state");
                                if(status.equals("No_Mask")){
                                    textView.setText("Wear Mask");
                                }

                                else if (status.equals("No_Cover"))
                                {
                                    textView.setText("Cover Your Mouth!");
                                }
                            } else {
                                Map<String, Object> newuser = new HashMap<>();
                                newuser.put("state", "No_user");

                                db.collection("users").document(user.getUid())
                                        .set(newuser)
                                        .addOnSuccessListener(documentReference -> Log.i("Firestore", "Update success"))
                                        .addOnFailureListener(e -> Log.e("Firestore", "Update failure"));
                            }
                        }
                    });

            // repeating code ends here
            handler.postDelayed(runnable, delay); // the call for repeat
        }, startDelay);

    }
}