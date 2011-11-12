
import java.awt.*;
import java.awt.event.*;
import java.applet.Applet;
import java.net.*;


public class Rotation extends Applet implements KeyListener,FocusListener,MouseListener,MouseMotionListener 
{
    
        int x=50,y=50,mx=50,my=60;
        private Image img;
	int low = 0, high= 99, step =5, steplook = 1 ;
	boolean isButtonPressed = false;
	boolean focussed = false;
	boolean flag = false,f1 = false;
	
	Graphics bufferGraphics; 
	//Dimension dim; 
/*
	private Image dbImage;
	private Graphics dbg; 

	public void update (Graphics g)
	{
		System.out.println("call to update\n\n");
	      // initialize buffer
	      if (dbImage == null)
	      {
		    dbImage = createImage (this.getSize().width, this.getSize().height);
		    dbg = dbImage.getGraphics ();
	      }

	      // clear screen in background
	      dbg.setColor (getBackground ());
	      dbg.fillRect (0, 0, this.getSize().width, this.getSize().height);

	      // draw elements in background
	      dbg.setColor (getForeground());
	      paint (dbg);

	      // draw image on the screen
	      g.drawImage (dbImage, 0, 0, this);

	}*/
	public void update(Graphics g)
	{
		paint(g);
	} 
	public void init()
	{
		img = null;

		addKeyListener(this);
		addMouseListener( this );
		//addFocusListener(this);
		//addMouseMotionListener(this);
	}
	public void loadImage(int a,int b,int ma,int mb)
	{
		try
		{	
			 String url = "http://10.3.3.220:9998/work?x="+mx+"&y="+my+"&lx="+x+"&lz="+y;			
			//String url = "http://127.0.0.1:9998/work?x=50&y=60&lx=50&lz=50";
			 img = getImage(new URL(url));
		}
		catch(Exception e){}
	}

	public void paint(Graphics g)
	{		
		loadImage(x,y,mx,my);
		
		//g.drawImage(img, 0, 0,318,240, this);
		g.drawImage(img, 0, 0,320,320, this);
		if(f1)
		{
			g.setColor(Color.red);
			g.drawString("Camera enabled",100,50);
			//f1 = false;	
		}
	}
   
	public void focusGained(FocusEvent evt) {
         // The applet now has the input focus.
	      //focussed = true;
	    //  repaint();  // redraw with cyan border
   	}
   

   	public void focusLost(FocusEvent evt) {
         // The applet has now lost the input focus.
      		//focussed = false;
     	 	//repaint();  // redraw without cyan border
   	}

  	 public void keyPressed(KeyEvent evt) 
  	 {          
         
	      int key = evt.getKeyCode();  // keyboard code for the key that was pressed
      		
	      if(!f1){
	      if (key == KeyEvent.VK_LEFT) {         
		 x -= steplook;
        	 if ( x<= low)
        	    x = low;        
        	 repaint();
      	      }
	      if (key == KeyEvent.VK_RIGHT) {
         
		 x += steplook;
        	 if ( x>= high)
        	    x = high;
         
        	 repaint();
              }
      
	      if (key == KeyEvent.VK_UP) {
        	 y += steplook;
        	 if ( y>= high)
        	    y = high;
         
        	 repaint();
      	      }
	      if (key == KeyEvent.VK_DOWN) {
        	     y -= steplook;     
        	     if ( y<= low)
	             y = low;
     
                     repaint();
              }}
	      
	      else
		{
			if (key == KeyEvent.VK_LEFT) {  
				//mx = (int)(mx/3.18);
				//my = (int)(k/2.4);       
		 mx -= step;
        	 if ( mx<= low)
        	    mx = low;        
        	 repaint();
      	      }
	      if (key == KeyEvent.VK_RIGHT) {
         
		 mx += step;
        	 if ( mx>= high)
        	    mx = high;
         
        	 repaint();
              }
      
	      if (key == KeyEvent.VK_UP) {
        	 my += step;
        	 if ( my>= high)
        	    my = high;
         
        	 repaint();
      	      }
	      if (key == KeyEvent.VK_DOWN) {
        	     my -= step;     
        	     if ( my<= low)
	             my = low;
     
                     repaint();
              }
		}

        }  // end keyPressed()


   	public void keyReleased(KeyEvent evt) { 
     	 // empty method, required by the KeyListener Interface
   	}
   	public void keyTyped(KeyEvent evt) {
	
		char ch = evt.getKeyChar();  // The character typed.

	        if (ch == 'C' || ch == 'c') {
			f1 = true;
		        repaint();
      		}
		if (ch == 'D' || ch == 'd') {
			f1 = false;
		        repaint();
      		}
   	}

	public void mouseEntered( MouseEvent e ) {     		
   	}

   	public void mouseExited( MouseEvent e ) {
  	 }

	public void mouseClicked( MouseEvent e ) {
     	 	
		//int j,k;
		//j=e.getX();
		//k=e.getY();

		//mx = (int)(j/3.18);
		//my = (int)(k/2.4);
		//System.out.println("You clicked on "+j+" "+k+"  "+mx+","+my);
		//repaint();	
		//e.consume();
   	}

	public void mousePressed( MouseEvent e ) {  // called after a button is pressed down
		//flag = true;
     		 //requestFocus();
   	}
  	 public void mouseReleased( MouseEvent e ) {  // called after a button is released
		//flag = false;
     		//repaint();
     		e.consume();
	
     		//requestFocus();
  	 }
   
   	public void mouseDragged( MouseEvent e ) {  // called during motion with buttons down
   	
   	}


   	public void mouseMoved(MouseEvent e) {

   	}
  

   
} 


