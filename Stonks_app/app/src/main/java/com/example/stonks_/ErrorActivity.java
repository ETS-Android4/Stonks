package com.example.stonks_;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import java.util.Objects;

public class ErrorActivity extends AppCompatActivity {
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.error);
        Objects.requireNonNull(getSupportActionBar()).hide();

        Intent intent= getIntent();
        String error = intent.getExtras().getString("error");

        Log.e("stonks", "Could not parse malformed JSON: ");
        TextView error1;
        Button b1;
        b1 = findViewById(R.id.button);
        error1 = findViewById(R.id.error1);
        error1.setText(error);
        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(ErrorActivity.this,HomeActivity.class);
                startActivity(intent);
            }
        });
    }
}
