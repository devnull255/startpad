package org.startpad.android.enigma;

import org.startpad.android.enigma.R;

import android.app.TabActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TabHost;
import android.widget.AdapterView;
import android.widget.ToggleButton;
import android.widget.AdapterView.OnItemSelectedListener;

public class Enigma extends TabActivity
	{
	private static final String TAG = "Enigma";
    Spinner[] aspnRotors = new Spinner[3];
    int[] aRotors = new int[] {0,1,2};
    ToggleButton toggleGroup;
    boolean fGroup = false;
    EditText edit;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    	{
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
        
        // Initialize Simulator view
        toggleGroup = (ToggleButton) findViewById(R.id.group_text);
        toggleGroup.setOnClickListener(
        		new ToggleButton.OnClickListener()
	        		{
					public void onClick(View v)
						{
						fGroup = !fGroup;
						Log.d(TAG, "Group: " + fGroup);
						}
	        		});
        
        edit = (EditText) findViewById(R.id.input);
        edit.setOnKeyListener(
        		new EditText.OnKeyListener()
	        		{
					public boolean onKey(View v, int keyCode, KeyEvent event)
						{	
							Log.d(TAG, "Key");
							return false;
						}
	        		});
        
        // Initialize Settings view
        
        ArrayAdapter<CharSequence> adapter;
        
        adapter = ArrayAdapter.createFromResource(this, R.array.rotor_names, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        for (int i = 0; i < 3; i++)
        	{
        	aspnRotors[i] = (Spinner) findViewById(R.id.spn_rotors_1 + i);
        	aspnRotors[i].setAdapter(adapter);
        	aspnRotors[i].setSelection(aRotors[i]);
        	
        	aspnRotors[i].setOnItemSelectedListener(
            		new OnItemSelectedListener()
            			{
    					public void onItemSelected(AdapterView<?> parent, View view, int pos, long id)
    						{
    						int iMe;
    						for (iMe = 0; iMe < 3; iMe++)
    							if (aspnRotors[iMe] == parent)
    								break;

    						Log.d(TAG, "Selected:" + iMe + " to:"+ id);
    						
    						// If rotor already used - swap it out with this rotor's value
    						for (int i = 0; i < 3; i++)
	    						{
    							if (i == iMe)
    								continue;
    							 if (aRotors[i] == id)
    							 	{
    								aspnRotors[i].setSelection(aRotors[iMe]);
    								aRotors[i] = aRotors[iMe];
    							 	}
	    						}
    						
    						aRotors[iMe] = (int) id;
    						
    						Log.d(TAG, "Rotors: " + aRotors[0] + ", " + aRotors[1] + ", " + aRotors[2]);
    						}

    					public void onNothingSelected(AdapterView<?> arg0) {}
            			});
        	}
        	
        adapter = ArrayAdapter.createFromResource(this, R.array.alpha, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        
        for (int i = 0; i < 3; i++)
        	((Spinner) findViewById(R.id.spn_rings_1 + i)).setAdapter(adapter);

    	}
	}