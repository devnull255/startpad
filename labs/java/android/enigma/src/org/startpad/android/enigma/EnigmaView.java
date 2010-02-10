package org.startpad.android.enigma;

import org.startpad.Enigma;

import android.content.Context;
import android.content.res.Resources;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.util.AttributeSet;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;

public class EnigmaView extends View {
	Resources res;
	Enigma machine;
	Drawable letters;
	
	private static final String TAG = "EnigmaView";
	static int simWidth = 1024;
	static int simHeight = 1200;
	int viewWidth;
	int viewHeight;
	
	private Rect[] rcRotors = new Rect[3];
	private Rect[] rcSpinners = new Rect[3];
	private Rect rcLetters;
	
	boolean fLidClosed = true;
	
	protected void onMeasure(int xSpec, int ySpec)
		{
		super.onMeasure(xSpec, ySpec);
		viewWidth = getMeasuredWidth();
		viewHeight = getMeasuredHeight();
		int yRotor;
		int[] axRotors = new int[3];
		int dxRotor;
		int dyRotor;
		
		float xScale;
		float yScale;
		
		xScale = (float) viewWidth/simWidth;
		yScale = (float) viewHeight/simHeight;
		
		yRotor = (int) (res.getDimension(R.dimen.y_rotors) * yScale);
		axRotors[0] = (int) (res.getDimension(R.dimen.x_left_rotor) * xScale);
		axRotors[1] = (int) (res.getDimension(R.dimen.x_center_rotor) * xScale);
		axRotors[2] = (int) (res.getDimension(R.dimen.x_right_rotor) * xScale);
		
		dxRotor = (int) (res.getDimension(R.dimen.dx_rotor) * xScale);
		dyRotor = (int) (res.getDimension(R.dimen.dy_rotor) * yScale);
		
		for (int i = 0; i < 3; i++)
			{
			rcRotors[i] = new Rect(axRotors[i]-dxRotor/2, yRotor-dyRotor/2,
								   axRotors[i]+dxRotor/2, yRotor+dyRotor/2);
			Log.d(TAG, "Rotor: " + rcRotors[i].toString());
			rcRotors[i].inset((int) (xScale*7), (int) (yScale*20));
			}
		
		int yLetters = (int) (res.getDimension(R.dimen.y_letters) * yScale);
		int dyLetters = (int) (res.getDimension(R.dimen.dy_letters) * yScale);
		int xLetters = (int) (res.getDimension(R.dimen.x_letters) * xScale);
		int dxLetters = (int) (res.getDimension(R.dimen.dx_letters) * xScale);
		
		rcLetters = new Rect(xLetters, yLetters, xLetters+dxLetters, yLetters+dyLetters);
		}
	
	protected void onDraw(Canvas canvas)
		{
		super.onDraw(canvas);
		if (fLidClosed)
			return;
		
		Paint paint = new Paint();
		paint.setTextAlign(Paint.Align.CENTER);
		paint.setColor(Color.BLACK);
		paint.setTextSize(rcRotors[0].height());
		paint.setAntiAlias(true);
		
		String sPosition = machine.sPosition();
		
		for (int i = 0; i < 3; i++)
			{
			canvas.drawText(sPosition.substring(i,i+1), rcRotors[i].centerX(), rcRotors[i].bottom, paint);
			}
		
		letters.setBounds(rcLetters);
		letters.draw(canvas);
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
	
	public void setMachine(Enigma machine)
		{
		this.machine = machine;	
		}
	
    // Initialize Simulation View
    private void init(Context context)
	    {
    	this.res = context.getResources();
    	this.letters = this.res.getDrawable(R.drawable.letters);
    	
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
	                return true;
	                }
	            switch (event.getAction())
	            {
	            case MotionEvent.ACTION_DOWN:
	                if (!fDown)
	                    {
	                    fDown = true;
	                    EnigmaApp.SoundEffect.KEY_DOWN.play();
	                    
	                    machine.spinRotor(2, 1);
	                    invalidate(rcRotors[2]);
	                    }
	                break;
	            case MotionEvent.ACTION_UP:
	                if (fDown)
	                    {
	                    fDown = false;
	                    EnigmaApp.SoundEffect.KEY_UP.play();
	                    }
	                break;
	            }
	            return true;
	            }
	        });
	    }
}
