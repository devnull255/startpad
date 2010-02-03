package org.startpad.android.enigma;

import java.util.List;

import org.startpad.android.enigma.R;

import android.app.TabActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TabHost;

public class Enigma extends TabActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TabHost tabHost = getTabHost();
        
        // Setup top-level tabbled layout screen 
        
        LayoutInflater.from(this).inflate(R.layout.main, tabHost.getTabContentView(), true);

        tabHost.addTab(tabHost.newTabSpec("sim")
                .setIndicator("Simulator")
                .setContent(R.id.sim));
        tabHost.addTab(tabHost.newTabSpec("settings")
                .setIndicator("Settings")
                .setContent(R.id.settings));
        
        // Initializing the Settings view
        
        Spinner s1 = (Spinner) findViewById(R.id.spn_rotors_1);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(
                this, R.array.rotor_names, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        s1.setAdapter(adapter);
    }
}