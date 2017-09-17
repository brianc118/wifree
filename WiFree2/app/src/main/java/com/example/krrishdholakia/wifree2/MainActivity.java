package com.example.krrishdholakia.wifree2;

import android.Manifest;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationManager;
import android.net.Uri;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.CardView;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.telephony.SmsManager;

import android.app.AlertDialog;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.GoogleMap.OnMyLocationButtonClickListener;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.LatLng;

import java.util.Arrays;
import java.util.List;

import static android.R.id.message;


public class MainActivity extends AppCompatActivity {
    private GoogleMap gMap;
    private static final int MY_PERMISSIONS_REQUEST_SEND_SMS = 0;

    private String co_ordinates = "";
    private String messages = "";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView wifi = (TextView) findViewById(R.id.wifi_Text);

        ArrayAdapter adapter = ArrayAdapter.createFromResource(this,
                R.array.travel_modes, R.layout.spinner_item);

        adapter.setDropDownViewResource(R.layout.spinner_dropdown_item);
        wifi.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //push the geodata to the server and find nearest wifi spot
                final String phoneNumber = "415-853-1662";
                //SmsManager smsManager1 = SmsManager.getDefault();
                //smsManager1.sendTextMessage("+17708783106", null, "hello", null, null);
                if (co_ordinates != null) {
                    try {

                        System.out.println("going into the tunnel");
                        if (ActivityCompat.checkSelfPermission(MainActivity.this, android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                            ActivityCompat.requestPermissions(MainActivity.this, new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION}, 1);
                        } else {

                            System.out.println(" user location");
                            LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
                            final Location myLocation = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                            if (ActivityCompat.checkSelfPermission(MainActivity.this, Manifest.permission.SEND_SMS) != PackageManager.PERMISSION_GRANTED) {
                                ActivityCompat.requestPermissions(MainActivity.this, new String[]{android.Manifest.permission.SEND_SMS}, 1);
                            } else {
                                LatLng userLocation = new LatLng(myLocation.getLatitude(), myLocation.getLongitude());
                                co_ordinates = "" + userLocation.latitude + "," + userLocation.longitude;
                                System.out.println(co_ordinates + " : 123");
                                AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);

                                final String[] colors = new String[]{
                                        "driving",
                                        "walking",
                                        "transit",
                                };

                                // Boolean array for initial selected items
                                final boolean[] checkedColors = new boolean[]{
                                        false, // Red
                                        false, // Green
                                        false

                                };

                                // Convert the color array to list
                                final List<String> colorsList = Arrays.asList(colors);

                                builder.setMultiChoiceItems(colors, checkedColors, new DialogInterface.OnMultiChoiceClickListener() {
                                    @Override
                                    public void onClick(DialogInterface dialog, int which, boolean isChecked) {

                                        // Update the current focused item's checked status
                                        for(int count = 0; count < checkedColors.length; count++)
                                        {
                                            if (count == which) {
                                                checkedColors[count]=true;
                                                ((AlertDialog) dialog).getListView().setItemChecked(count, true);
                                            }
                                            else {
                                                checkedColors[count]=false;
                                                ((AlertDialog) dialog).getListView().setItemChecked(count, false);
                                            }

                                        }
                                        checkedColors[which] = isChecked;

                                        // Get the current focused item
                                        String currentItem = colorsList.get(which);



                                    }
                                });

                                // Specify the dialog is not cancelable
                                builder.setCancelable(false);

                                // Set a title for alert dialog
                                builder.setTitle("Your preferred mode?");

                                // Set the positive/yes button click listener
                                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                                    @Override
                                    public void onClick(DialogInterface dialog, int which) {
                                        // Do something when click positive button
                                        for (int i = 0; i<checkedColors.length; i++){
                                            boolean checked = checkedColors[i];
                                            if (checked) {
                                                final Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("sms:" + phoneNumber));
                                                messages = colors[i] + "," + co_ordinates;
                                                System.out.println(colors[i] + " do these match? " + messages);
                                                intent.putExtra("sms_body", messages);
                                                startActivity(intent);
                                            }
                                        }
                                    }
                                });
                                AlertDialog dialog = builder.create();
                                // Display the alert dialog on interface
                                dialog.show();




                            }
                        }

                    } catch (Exception e) {


                    }
                }
            }
        });


    }

}





