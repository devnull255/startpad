package org.startpad.android.enigma;
import android.content.Context;
import android.media.MediaPlayer;
import android.util.AttributeSet;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnTouchListener;

public class EnigmaView extends View {
	Context context;
	
	private static final String TAG = "EnigmaView";
	static int simWidth = 1024;
	static int simHeight = 1200;
	
    MediaPlayer mpDown;
    MediaPlayer mpUp;
    MediaPlayer mpRotor;
	
	boolean fLidClosed = true;
	
	int viewWidth;
	int viewHeight;
	
	protected void onMeasure(int xSpec, int ySpec)
		{
		super.onMeasure(xSpec, ySpec);
		viewWidth = getMeasuredWidth();
		viewHeight = getMeasuredHeight();
		Log.d(TAG, viewWidth + ", " + viewHeight);
		}

	public EnigmaView(Context context) {
		super(context);
		init(context);
	}

	public EnigmaView(Context context, AttributeSet attrs) {
		super(context, attrs);
		init(context);
	}

	public EnigmaView(Context context, AttributeSet attrs, int defStyle) {
		super(context, attrs, defStyle);
		init(context);
	}
	
    // Initialize Simulation View
    private void init(Context context)
	    {
    	this.context = context;
    	
        mpDown = MediaPlayer.create(context, R.raw.key_down);
        mpUp = MediaPlayer.create(context, R.raw.key_up);
        mpRotor = MediaPlayer.create(context, R.raw.rotor);
    	
	    setOnTouchListener(new OnTouchListener()
	        {
	        boolean fDown = false;
	        public boolean onTouch(View view, MotionEvent event)
	            {
	            if (fLidClosed)
	                {
	                fLidClosed = false;
	                setBackgroundResource(R.drawable.enigma);
	                return false;
	                }
	            switch (event.getAction())
	            {
	            case MotionEvent.ACTION_DOWN:
	                if (!fDown)
	                    {
	                    fDown = true;
	                    mpDown.seekTo(0);
	                    mpDown.start();
	                    }
	                break;
	            case MotionEvent.ACTION_UP:
	                if (fDown)
	                    {
	                    fDown = false;            
	                    mpUp.seekTo(0);
	                    mpUp.start();
	                    }
	                break;
	            }
	            return true;
	            }
	        });
	    }
}
