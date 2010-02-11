package org.startpad.android.enigma;

import org.startpad.Enigma;

import android.content.Context;
import android.content.res.Resources;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
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
	private Rect rcAllRotors;
	private Rect[] rcSpinners = new Rect[3];
	private Rect rcLetters;
	
	Qwertzu qLights = new Qwertzu();
	Qwertzu qKeys = new Qwertzu();
	
	boolean fDown = false;
	char chLight = 0;
	
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
            if (i == 0)
                rcAllRotors = new Rect(rcRotors[i]);
            else
                rcAllRotors.union(rcRotors[i]);
			Log.d(TAG, "Rotor: " + rcRotors[i].toString());
			rcRotors[i].inset((int) (xScale*7), (int) (yScale*20));
			}
		
		int yLetters = (int) (res.getDimension(R.dimen.y_letters) * yScale);
		int dyLetters = (int) (res.getDimension(R.dimen.dy_letters) * yScale);
		int xLetters = (int) (res.getDimension(R.dimen.x_letters) * xScale);
		int dxLetters = (int) (res.getDimension(R.dimen.dx_letters) * xScale);
		
		rcLetters = new Rect(xLetters, yLetters, xLetters+dxLetters, yLetters+dyLetters);
		
		// Setup dimensions of keyboard for hit testing
		int xP = (int) (res.getDimension(R.dimen.x_P_key) * xScale);
		int yP = (int) (res.getDimension(R.dimen.y_P_key) * yScale);
		int dxKey = (int) (res.getDimension(R.dimen.dx_key) * xScale);
		int dyKey = (int) (res.getDimension(R.dimen.dy_key) * yScale);
		Rect rcPKey = new Rect(xP, yP, xP + dxKey, yP + dyKey);
		
		int dxRightKey = (int) (res.getDimension(R.dimen.dx_right_key) * xScale);
		int dxUpKey = (int) (res.getDimension(R.dimen.dx_up_key) * xScale);
		int dyUpKey = (int) (res.getDimension(R.dimen.dy_up_key) * yScale);
		Point ptRightKey = new Point(dxRightKey, 0);
		Point ptUpKey = new Point(dxUpKey, dyUpKey);
		qKeys.setSize(rcPKey, ptRightKey, ptUpKey);
		
		// Setup dimensions of lights for display
		xP = (int) (res.getDimension(R.dimen.x_P_light) * xScale);
        yP = (int) (res.getDimension(R.dimen.y_P_light) * yScale);
        int dxLight = (int) (res.getDimension(R.dimen.dx_light) * xScale);
        int dyLight = (int) (res.getDimension(R.dimen.dy_light) * yScale);
        Rect rcPLight = new Rect(xP, yP, xP + dxLight, yP + dyLight);
        
        int dxRightLight = (int) (res.getDimension(R.dimen.dx_right_light) * xScale);
        int dxUpLight = (int) (res.getDimension(R.dimen.dx_up_light) * xScale);
        int dyUpLight = (int) (res.getDimension(R.dimen.dy_up_light) * yScale);
        Point ptRightLight = new Point(dxRightLight, 0);
        Point ptUpLight = new Point(dxUpLight, dyUpLight);
        qLights.setSize(rcPLight, ptRightLight, ptUpLight);
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
		
		if (fDown)
		    {
		    canvas.save();
		    canvas.clipRect(qLights.rectFromChar(chLight));
    		letters.setBounds(rcLetters);
    		letters.draw(canvas);
    		canvas.restore();
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
	                Point ptClick = new Point((int) event.getX(), (int) event.getY());
	                char ch = qKeys.charFromPt(ptClick);
	                if (ch == 0)
	                    return false;

                    fDown = true;

                    chLight = machine.encodeChar(ch);
                    Log.d(TAG, "Encode " + ch + " -> " + chLight);
                    
                    invalidate(rcAllRotors);
                    invalidate(qLights.rectFromChar(chLight));
	                    
                    EnigmaApp.SoundEffect.KEY_DOWN.play();
	                break;

	            case MotionEvent.ACTION_UP:
	                if (fDown)
	                    {
	                    fDown = false;
	                    invalidate(qLights.rectFromChar(chLight));
	                    EnigmaApp.SoundEffect.KEY_UP.play();
	                    }
	                break;
	            }
	            return true;
	            }
	        });
	    }
    
    /* Convert from x,y to a keyboard/light character.  Assumes QWERTU
     * character layout.
     */
    
    private static String[] asRows = new String[] {"QWERTZUIO", "ASDFGHJK", "PYXCVBNML"};
    
    class Qwertzu
        {
        private Point ptRight;
        private Rect[] arcRows;
        
        public void setSize(Rect rcP, Point ptRight, Point ptUp)
            {
            this.ptRight = new Point(ptRight);
            
            rcP = new Rect(rcP);
            
            Rect rcA = new Rect(rcP);
            rcA.offset(ptRight.x, ptRight.y);
            rcA.offset(ptUp.x, ptUp.y);
            
            Rect rcQ = new Rect(rcA);
            rcQ.offset(ptUp.x, ptUp.y);
            
            arcRows = new Rect[] {rcQ, rcA, rcP};
            }
        
        public char charFromPt(Point ptClick)
            {
            for (int i = 0; i < arcRows.length; i++)
                {
                Rect rcChar = new Rect(arcRows[i]);
                
                for (int j = 0; j < asRows[i].length(); j++)
                    {
                    if (rcChar.contains(ptClick.x, ptClick.y))
                        return asRows[i].charAt(j);
                    rcChar.offset(ptRight.x, ptRight.y);
                    }
                }
                
            return 0;
            }
        
        public Rect rectFromChar(char ch)
            {
            for (int i = 0; i < arcRows.length; i++)
                {
                Rect rcChar = new Rect(arcRows[i]);

                for (int j = 0; j < asRows[i].length(); j++)
                    {
                    if (ch == asRows[i].charAt(j))
                        return rcChar;
                    rcChar.offset(ptRight.x, ptRight.y);
                    }
                }
            
            return null;
            }
        }
}
