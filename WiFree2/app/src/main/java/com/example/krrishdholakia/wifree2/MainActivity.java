package com.example.krrishdholakia.wifree2;

import android.Manifest;
import android.content.Context;
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
import android.view.View;
import android.widget.Button;
import android.telephony.SmsManager;

import android.app.AlertDialog;
import android.widget.Spinner;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.GoogleMap.OnMyLocationButtonClickListener;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.LatLng;

import static android.R.id.message;


public class MainActivity extends AppCompatActivity {
    private GoogleMap gMap;
    private static final int MY_PERMISSIONS_REQUEST_SEND_SMS = 0;
    private Spinner directions;
    private String co_ordinates = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button wifi = (Button) findViewById(R.id.button);
        directions = (Spinner) findViewById(R.id.spinner1);
        wifi.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //push the geodata to the server and find nearest wifi spot
                String phoneNumber = "415-853-1662";
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
                            Location myLocation = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                            if (ActivityCompat.checkSelfPermission(MainActivity.this, Manifest.permission.SEND_SMS) != PackageManager.PERMISSION_GRANTED) {
                                ActivityCompat.requestPermissions(MainActivity.this, new String[]{android.Manifest.permission.SEND_SMS}, 1);
                            } else {
                                LatLng userLocation = new LatLng(myLocation.getLatitude(), myLocation.getLongitude());
                                co_ordinates = "" + userLocation.latitude + "," + userLocation.longitude;
                                System.out.println(co_ordinates + " : 123");
                                //SmsManager smsManager = SmsManager.getDefault();
                                //smsManager.sendTextMessage("+17708783106", null, "hello", null, null);
                                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("sms:" + phoneNumber));
                                String message = String.valueOf(directions.getSelectedItem())+ "," + co_ordinates;
                                intent.putExtra("sms_body", message);
                                startActivity(intent);

                            }
                        }

                    } catch (Exception e) {


                    }
                }
            }
        });


    }

}





