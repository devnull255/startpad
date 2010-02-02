package org.startpad.android.enigma;

import org.startpad.android.enigma.R;

import android.app.TabActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.widget.TabHost;

public class Enigma extends TabActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TabHost tabHost = getTabHost();
        
        LayoutInflater.from(this).inflate(R.layout.main, tabHost.getTabContentView(), true);

        tabHost.addTab(tabHost.newTabSpec("sim")
                .setIndicator("Simulator")
                .setContent(R.id.sim));
        tabHost.addTab(tabHost.newTabSpec("settings")
                .setIndicator("Settings")
                .setContent(R.id.settings));
    }
}