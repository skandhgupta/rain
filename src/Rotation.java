
import java.awt.*;
import java.awt.event.*;
import java.applet.Applet;
import java.net.*;


public class Rotation extends Applet implements KeyListener,FocusListener,MouseListener,MouseMotionListener 
{
    
        int x=50,y=50,mx=50,my=60;
        private Image img;
	int low = 0, high= 99, step =5;
	boolean isButtonPressed = false;
	boolean focussed = false;
	boolean flag = false,f1 = false;
	
	Graphics bufferGraphics; 
	
	public void update(Graphics g)
	{
		paint(g);
	} 
	public void init()
	{
		img = null;

		loadImage(x,y,mx,my);
		addKeyListener(this);
		addMouseListener( this );
		//addFocusListener(this);
		addMouseMotionListener(this);
	}
	public void loadImage(int a,int b,int ma,int mb)
	{
		try
		{	
			String url = "http://10.3.3.220:9998/work?x="+mx+"&y="+my+"&lx="+x+"&lz="+y;			
			//String url = "http://10.3.3.220:9998/work?x=y=60&lx=50&lz=50";
			System.out.println("URL= "+url);
			img = getImage(new URL(url));
		}
		catch(Exception e){}
	}

	public void paint(Graphics g)
	{		
		//loadImage(x,y,mx,my);
		
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
        
   	}
   

   	public void focusLost(FocusEvent evt) {
         
   	}

  	 public void keyPressed(KeyEvent evt) 
  	 {          
         
	      int key = evt.getKeyCode();  // keyboard code for the key that was pressed
      		
	      if(!f1){
	      if (key == KeyEvent.VK_LEFT) {         
		 x -= step;
        	 if ( x<= low)
        	    x = low;        
	               loadImage(x,y,mx,my);
        	 repaint();
      	      }
	      if (key == KeyEvent.VK_RIGHT) {
         
		 x += step;
        	 if ( x>= high)
        	    x = high;
         
	               loadImage(x,y,mx,my);
        	 repaint();
              }
      
	      if (key == KeyEvent.VK_UP) {
        	 y += step;
        	 if ( y>= high)
        	    y = high;
         
	               loadImage(x,y,mx,my);
        	 repaint();
      	      }
	      if (key == KeyEvent.VK_DOWN) {
        	     y -= step;     
        	     if ( y<= low)
	             y = low;
     
	               loadImage(x,y,mx,my);
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
	               loadImage(x,y,mx,my);
        	 repaint();
      	      }
	      if (key == KeyEvent.VK_RIGHT) {
         
		 mx += step;
        	 if ( mx>= high)
        	    mx = high;
	               loadImage(x,y,mx,my);
         
        	 repaint();
              }
      
	      if (key == KeyEvent.VK_UP) {
        	 my += step;
        	 if ( my>= high)
        	    my = high;
	               loadImage(x,y,mx,my);
         
        	 repaint();
      	      }
	      if (key == KeyEvent.VK_DOWN) {
        	     my -= step;     
        	     if ( my<= low)
	             my = low;
     
	               loadImage(x,y,mx,my);
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
	               loadImage(x,y,mx,my);
		        repaint();
      		}
		if (ch == 'D' || ch == 'd') {
			f1 = false;
	               loadImage(x,y,mx,my);
		        repaint();
      		}
   	}

	public void mouseEntered( MouseEvent e ) {     		
   	}

   	public void mouseExited( MouseEvent e ) {
  	 }

	public void mouseClicked( MouseEvent e ) {
     	 	
   	}

	public void mousePressed( MouseEvent e ) {  // called after a button is pressed down
		
   	}
  	 public void mouseReleased( MouseEvent e ) {  // called after a button is released
		
     		//e.consume();
	
     		
  	 }
   
   	public void mouseDragged( MouseEvent e ) {  // called during motion with buttons down
   	
   	}


   	public void mouseMoved(MouseEvent e) {
	       int j,k,jj,kk;
               j=e.getX();
               k=e.getY();

               jj = j/8 + 30;
               kk = k/8 + 30;
               //System.out.println("You clicked on "+j+" "+k+"  "+mx+","+my);
		if(jj != mx && kk!= my){
			mx = jj;my = kk;
	               loadImage(x,y,mx,my);
		}
               repaint();        
               e.consume();

   	}
  

   
} 


