package org.startpad.android.enigma;

import org.startpad.Enigma;
import org.startpad.android.enigma.EnigmaApp.SoundEffect;

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
import android.widget.Toast;

public class EnigmaView extends View {
    private Context context;
	private Resources res;
	
	Enigma machine;
	Drawable letters;
	
	private static final String TAG = "EnigmaView";
	private static int simWidth = 1024;
	private static int simHeight = 1200;
	private int viewWidth;
	private int viewHeight;
	
    private float xScale;
    private float yScale;
	
	private Rect[] rcRotors = new Rect[3];
	private Rect rcAllRotors;
	private Rect[] rcSpinners = new Rect[3];
	private Rect rcLetters;
	
	QWERTZU qLights = new QWERTZU();
	QWERTZU qKeys = new QWERTZU();
	
	boolean fDown = false;
	char chLight = 0;
	
	boolean fLidClosed = true;
	
	Toast toast;
	
   enum RegPoint
       {
       DPT_ROTOR(R.dimen.dx_rotor, R.dimen.dy_rotor),
       
       PT_LETTERS(R.dimen.x_letters, R.dimen.y_letters),
       DPT_LETTERS(R.dimen.dx_letters, R.dimen.dy_letters),
       
       PT_P_KEY(R.dimen.x_P_key, R.dimen.y_P_key),
       DPT_KEY(R.dimen.dx_key, R.dimen.dy_key),
       DPT_RIGHT_KEY(R.dimen.dx_right_key, 0),
       DPT_UP_KEY(R.dimen.dx_up_key, R.dimen.dy_up_key),
       
       PT_P_LIGHT(R.dimen.x_P_light, R.dimen.y_P_light),
       DPT_LIGHT(R.dimen.dx_light, R.dimen.dy_light),
       DPT_RIGHT_LIGHT(R.dimen.dx_right_light, 0),
       DPT_UP_LIGHT(R.dimen.dx_up_light, R.dimen.dy_up_light),

       ;

       private int ridX;
       private int ridY;
       private Point ptRaw;
       private Point ptScaled;
       
       RegPoint(int ridX, int ridY)
           {
           this.ridX = ridX;
           this.ridY = ridY;
           }
       
       public void init(Resources res, float xScale, float yScale)
           {
           ensurePoint(res);
           ptScaled = new Point((int) (ptRaw.x * xScale), (int) (ptRaw.y * yScale));
           }
       
       private void ensurePoint(Resources res)
           {
           if (ptRaw == null)
               {
               int x = 0;
               int y = 0;
               
               if (ridX != 0)
                   x = (int) (res.getDimension(ridX));
               if (ridY != 0)
                   y = (int) (res.getDimension(ridY));
               ptRaw = new Point(x,y);
               }
           }
       
       public Point getPoint()
           {
           return ptScaled;
           }
       
       static Rect rectFromPtDpt(RegPoint rpt, RegPoint rdpt)
           {
           Point pt = rpt.getPoint();
           Point dpt = rdpt.getPoint();
           return new Rect(pt.x, pt.y, pt.x + dpt.x, pt.y + dpt.y);
           }
       }
	
	protected void onMeasure(int xSpec, int ySpec)
		{
		super.onMeasure(xSpec, ySpec);
		viewWidth = getMeasuredWidth();
		viewHeight = getMeasuredHeight();
		int yRotor;
		int[] axRotors = new int[3];
		
		xScale = (float) viewWidth/simWidth;
		yScale = (float) viewHeight/simHeight;
		
		Log.d(TAG, "Scaling: " + xScale + ", " + yScale);
		
        for (RegPoint rpt : RegPoint.values())
            rpt.init(this.res, xScale, yScale);
		
		// Setup rotor windows - from centers and window sizes
		yRotor = (int) (res.getDimension(R.dimen.y_rotors) * yScale);
		axRotors[0] = (int) (res.getDimension(R.dimen.x_left_rotor) * xScale);
		axRotors[1] = (int) (res.getDimension(R.dimen.x_center_rotor) * xScale);
		axRotors[2] = (int) (res.getDimension(R.dimen.x_right_rotor) * xScale);
		
		Point dptRotor = RegPoint.DPT_ROTOR.getPoint();
		for (int i = 0; i < 3; i++)
			{
			rcRotors[i] = new Rect(axRotors[i]-dptRotor.x/2, yRotor-dptRotor.y/2,
								   axRotors[i]+dptRotor.x/2, yRotor+dptRotor.y/2);
            if (i == 0)
                rcAllRotors = new Rect(rcRotors[i]);
            else
                rcAllRotors.union(rcRotors[i]);
			rcRotors[i].inset((int) (xScale*7), (int) (yScale*20));
			}
		
		// Setup lights overlay PNG
		rcLetters = RegPoint.rectFromPtDpt(RegPoint.PT_LETTERS, RegPoint.DPT_LETTERS);
		
		// Setup dimensions of keyboard for hit testing
		Rect rcPKey = RegPoint.rectFromPtDpt(RegPoint.PT_P_KEY, RegPoint.DPT_KEY);
		qKeys.setSize(rcPKey, RegPoint.DPT_RIGHT_KEY.getPoint(), RegPoint.DPT_UP_KEY.getPoint());
		
		// Setup dimensions of lights for display
		Rect rcPLight = RegPoint.rectFromPtDpt(RegPoint.PT_P_LIGHT, RegPoint.DPT_LIGHT);
		qLights.setSize(rcPLight, RegPoint.DPT_RIGHT_LIGHT.getPoint(), RegPoint.DPT_UP_LIGHT.getPoint());
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
	    this.context = context;
    	this.res = context.getResources();
    	this.letters = this.res.getDrawable(R.drawable.letters);
    	
        toast = Toast.makeText(context, R.string.startup_message, Toast.LENGTH_LONG);
        toast.show();
    	
	    setOnTouchListener(new OnTouchListener()
	        {
	        public boolean onTouch(View view, MotionEvent event)
	            {
	            if (fLidClosed)
	                {
	                fLidClosed = false;
	                setBackgroundResource(R.drawable.enigma);
	                invalidate(0, 0, viewWidth, viewHeight);
	                
	                toast = Toast.makeText(((EnigmaView) view).context, R.string.sim_hint, Toast.LENGTH_LONG);
	                toast.show();
	                return true;
	                }
	            
	            switch (event.getAction())
	            {
	            case MotionEvent.ACTION_DOWN:
	                Point ptClick = new Point((int) event.getX(), (int) event.getY());
	                char ch = qKeys.charFromPt(ptClick);
	                if (ch == 0)
	                    {
	                    Log.d(TAG, "No key detected");
	                    return false;
                        }

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
    
    class QWERTZU
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
            int d2Min = -1;
            char chBest = 0;
            
            Log.d(TAG, "charFromPt" + ptClick);
            
            if (ptClick.y < arcRows[0].top - 10)
                return 0;
            
            Log.d(TAG, "possible key");
                
            for (int i = 0; i < arcRows.length; i++)
                {
                Rect rcChar = new Rect(arcRows[i]);

                for (int j = 0; j < asRows[i].length(); j++)
                    {
                    Point ptChar = new Point(rcChar.centerX(), rcChar.centerY());
                    int d2 = (int) (Math.pow(ptChar.x - ptClick.x,2) + Math.pow(ptChar.y - ptClick.y, 2));
                    if (d2Min < 0 || d2 < d2Min)
                        {
                        d2Min = d2;
                        chBest = asRows[i].charAt(j);
                        Log.d(TAG, "Better " + chBest + " at " + d2);
                        }
                    rcChar.offset(ptRight.x, ptRight.y);
                    }
                }
            
            return chBest;
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
