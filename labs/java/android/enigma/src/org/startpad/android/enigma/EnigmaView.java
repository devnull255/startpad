package org.startpad.android.enigma;
import android.content.Context;
import android.content.res.Resources;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.media.MediaPlayer;
import android.util.AttributeSet;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnTouchListener;

public class EnigmaView extends View {
	Context context;
	Resources res;
	
	private static final String TAG = "EnigmaView";
	static int simWidth = 1024;
	static int simHeight = 1200;
	int viewWidth;
	int viewHeight;
	float dxRotor;
	float dyRotor;
	
	private float[] axRotors = new float[3];
	private float yRotor;
	
    MediaPlayer mpDown;
    MediaPlayer mpUp;
    MediaPlayer mpRotor;
	
	boolean fLidClosed = true;
	
	
	protected void onMeasure(int xSpec, int ySpec)
		{
		super.onMeasure(xSpec, ySpec);
		viewWidth = getMeasuredWidth();
		viewHeight = getMeasuredHeight();
		
		yRotor = res.getDimension(R.dimen.y_rotors)/simHeight*viewHeight;
		axRotors[0] = res.getDimension(R.dimen.x_left_rotor)/simWidth*viewWidth;
		axRotors[1] = res.getDimension(R.dimen.x_center_rotor)/simWidth*viewWidth;
		axRotors[2] = res.getDimension(R.dimen.x_right_rotor)/simWidth*viewWidth;
		
		dxRotor = res.getDimension(R.dimen.dx_rotor)/simWidth*viewWidth;
		dyRotor = res.getDimension(R.dimen.dy_rotor)/simHeight*viewHeight;
		
		Log.d(TAG, "Y: " + yRotor);
		
		Log.d(TAG, viewWidth + ", " + viewHeight);
		
		
		}
	
	protected void onDraw(Canvas canvas)
		{
		super.onDraw(canvas);
		if (fLidClosed)
			return;
		
		Paint paint = new Paint();
		paint.setTextAlign(Paint.Align.CENTER);
		paint.setColor(Color.BLACK);
		paint.setTextSize((float) (dyRotor*0.7));
		paint.setAntiAlias(true);
		
		for (int i = 0; i < 3; i++)
			{
			canvas.drawText("W", axRotors[i], (float) (yRotor+dyRotor*0.7/2), paint);
			}
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
    	this.res = context.getResources();
    	
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
	                invalidate(0, 0, viewWidth, viewHeight);
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
