package com.liu.imgcore;


import java.awt.AlphaComposite;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Polygon;
import java.awt.RenderingHints;
import java.awt.geom.Rectangle2D;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
  
/**  
 * 图片水印  
 * @blog http://sjsky.iteye.com  
 * @author Michael  
 */  
public class ImageMarkLogoByIcon {   
  
	static Color sDefaulColor=Color.RED;
	static int sDefaulSize=30;
	static String mapName="log.txt";
	static String imgDir="img";
	static boolean logSwitch=false;
	static boolean cleanSwitch=false;
    /**  
     * @param args  
     */  
    public static void main(String[] args) {
        //from args过来
        String outPath="G:/lwh/xwandou/code/monkeytest/out/20160106_204837/";
        if(args==null||args.length==0){
			System.out.println("error params is null!");
        	return;
        }
        for(String str:args){
        	String strp=str.trim().toLowerCase();
        	if(strp.startsWith("color=")||strp.startsWith("c=")){
    			try{
    				sDefaulColor=Color.decode(str.split("=")[1]);
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("-log")||strp.startsWith("-l")){
    			try{
    				logSwitch=true;
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("size=")||strp.startsWith("s=")){
    			try{
    				sDefaulSize=Integer.valueOf(str.split("=")[1]);
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("out=")||strp.startsWith("o=")){
    			try{
    				outPath=str.split("=")[1];
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("map=")||strp.startsWith("m=")){
    			try{
    				mapName=str.split("=")[1];
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("-clean")||strp.startsWith("-cl")){
    			try{
    				cleanSwitch=true;
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}
        }
        HashMap<String,String[]>map=readConfigToMap(outPath);
        
        File file=new File(outPath+imgDir+"/");
        File[] tempList = file.listFiles();
        log("该目录下对象个数："+tempList.length);
		for (int i = 0; i < tempList.length; i++) {
			if (tempList[i].isFile()) {
				if(!tempList[i].getName().startsWith("ok")){
			        ArrayList<String[]>list=new ArrayList<String[]>();
			        ArrayList<String>liststr=new ArrayList<String>();
			        String[]strs= map.get(tempList[i].getName().split("\\.")[0]);
			        if(null!=strs&&strs.length>0){
			        	String[]xys=strs[0].split(";");
			        	for(String xy:xys){
			        		list.add(new String[]{xy.split(",")[0],xy.split(",")[1]});
			        	}
			        	
			        	String[]xsss=strs[1].split(";");
			        	for(String xy:xsss){
			        		liststr.add(xy);
			        	}
			        	markImageByString(liststr, tempList[i].getAbsolutePath(), tempList[i].getParent()+"/ok"+tempList[i].getName(), list);
			        }else{
//		        		list.add(new String[]{"10","10"});
//			        	markImageByString("", tempList[i].getAbsolutePath(), tempList[i].getParent()+"/ok"+tempList[i].getName(), list);
			        }
				}
				log("文     件：" + tempList[i]);
			}
//			if (tempList[i].isDirectory()) {
//				System.out.println("文件夹：" + tempList[i]);
//			}
		}
  }
  public static void log(String str){
	  if(logSwitch){
			System.out.println(str);
	  }
  }
  public static HashMap<String,String[]> readConfigToMap(String outPath){
      HashMap<String,String[]>map=new HashMap<String,String[]>();
      try{
      	FileReader reader = new FileReader(outPath+mapName);
      	BufferedReader br = new BufferedReader(reader);
      	String str = null;
      	while((str = br.readLine()) != null) {
      		if(null!=str&&str.trim().length()>0){
      			String[]mm=str.split("-");
      			if(mm.length>2){
      				map.put(mm[0], new String[]{mm[1],mm[2]});
      			}
      		}
      	}
      	br.close();
      	reader.close();
      }catch(Exception e){
      	e.printStackTrace();
      }
      return map;
  }
    public void testAddLoto(){
        String srcImgPath = "G:/lwh/xwandou/code/monkeytest/out/20160106_204837/img/164_678.png";   
        String iconPath = "G:/ilfe_new/ilife/images/icon1.png";   
        String targerPath = "G:/lwh/xwandou/code/monkeytest/out/20160106_204837/img_mark_icon.jpg";   
        String targerPath2 = "G:/lwh/xwandou/code/monkeytest/out/20160106_204837/img_mark_icon_rotate.jpg";   
        // 给图片添加水印   
        ImageMarkLogoByIcon.markImageByIcon(iconPath, srcImgPath, targerPath);   
//         给图片添加水印,水印旋转-45   
        ImageMarkLogoByIcon.markImageByIcon(iconPath, srcImgPath, targerPath2,   
                -45);   
        ArrayList<String[]>list=new ArrayList<String[]>();
        list.add(new String[]{"164","678"});
        list.add(new String[]{"200","200"});
        ArrayList<String>liststr=new ArrayList<String>();
        liststr.add("asdasd");
        markImageByString(liststr, srcImgPath, targerPath2, list);
    	
    }
    /**  
     * 给图片添加水印  
     * @param iconPath 水印图片路径  
     * @param srcImgPath 源图片路径  
     * @param targerPath 目标图片路径  
     */  
    public static void markImageByIcon(String iconPath, String srcImgPath,   
            String targerPath) {   
        markImageByIcon(iconPath, srcImgPath, targerPath, null);   
    }   
  
    /**  
     * 给图片添加水印、可设置水印图片旋转角度  
     * @param iconPath 水印图片路径  
     * @param srcImgPath 源图片路径  
     * @param targerPath 目标图片路径  
     * @param degree 水印图片旋转角度  
     */  
    public static void markImageByIcon(String iconPath, String srcImgPath,   
            String targerPath, Integer degree) {   
        OutputStream os = null;   
        try {   
            Image srcImg = ImageIO.read(new File(srcImgPath));   
  
            BufferedImage buffImg = new BufferedImage(srcImg.getWidth(null),   
                    srcImg.getHeight(null), BufferedImage.TYPE_INT_RGB);   
  
            // 得到画笔对象   
            // Graphics g= buffImg.getGraphics();   
            Graphics2D g = buffImg.createGraphics();   
  
            // 设置对线段的锯齿状边缘处理   
            g.setRenderingHint(RenderingHints.KEY_INTERPOLATION,   
                    RenderingHints.VALUE_INTERPOLATION_BILINEAR);   
  
            g.drawImage(srcImg.getScaledInstance(srcImg.getWidth(null), srcImg   
                    .getHeight(null), Image.SCALE_SMOOTH), 0, 0, null);   
  
            if (null != degree) {   
                // 设置水印旋转   
                g.rotate(Math.toRadians(degree),   
                        (double) buffImg.getWidth() / 2, (double) buffImg   
                                .getHeight() / 2);   
            }   
  
            // 水印图象的路径 水印一般为gif或者png的，这样可设置透明度   
            ImageIcon imgIcon = new ImageIcon(iconPath);   
  
            // 得到Image对象。   
            Image img = imgIcon.getImage();   
  
            float alpha = 0.5f; // 透明度   
            g.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_ATOP,   
                    alpha));   
  
            // 表示水印图片的位置   
            g.drawImage(img, 150, 300, null);   
  
            g.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER));   
  
            g.dispose();   
  
            os = new FileOutputStream(targerPath);   
  
            // 生成图片   
            ImageIO.write(buffImg, "JPG", os);   
  
            System.out.println("图片完成添加Icon印章。。。。。。");   
        } catch (Exception e) {   
            e.printStackTrace();   
        } finally {   
            try {   
                if (null != os)   
                    os.close();   
            } catch (Exception e) {   
                e.printStackTrace();   
            }   
        }   
    }   

    /**  
     * 给图片添加水印、可设置水印图片旋转角度  
     * @param iconPath 水印图片路径  
     * @param srcImgPath 源图片路径  
     * @param targerPath 目标图片路径  
     * @param degree 水印图片旋转角度  
     */  
    public static void markImageByString(List<String> iconPath, String srcImgPath,   
            String targerPath, List<String[]> xylist) {   
        OutputStream os = null;
        String filename="";
        try {
        	File file=new File(srcImgPath);
        	filename=file.getName();
            Image srcImg = ImageIO.read(file);   
            if(cleanSwitch)file.delete();
            BufferedImage buffImg = new BufferedImage(srcImg.getWidth(null),   
                    srcImg.getHeight(null), BufferedImage.TYPE_INT_RGB);   
  
            // 得到画笔对象   
            // Graphics g= buffImg.getGraphics();   
            Graphics2D g = buffImg.createGraphics();   
  
            // 设置对线段的锯齿状边缘处理   
            g.setRenderingHint(RenderingHints.KEY_INTERPOLATION,   
                    RenderingHints.VALUE_INTERPOLATION_BILINEAR);   
  
            g.drawImage(srcImg.getScaledInstance(srcImg.getWidth(null), srcImg   
                    .getHeight(null), Image.SCALE_SMOOTH), 0, 0, null);   
            Rectangle2D rd= g.getFont().getStringBounds(iconPath.get(0), g.getFontRenderContext());
            	
            // 水印图象的路径 水印一般为gif或者png的，这样可设置透明度   
//            ImageIcon imgIcon = new ImageIcon(iconPath);   
  
            // 得到Image对象。   
//            Image img = imgIcon.getImage();   
            g.setColor(sDefaulColor); 
            g.setFont(new Font(null,Font.BOLD,sDefaulSize)); //字体、字型、字号 
            float alpha = 0.9f; // 透明度   
            g.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_ATOP,   
                    alpha));   
  
            // 表示水印图片的位置   
            int OvalWidth=15;
            int OvalWidthSmall=3;
//            g.drawImage(img, 150, 300, null); 
            if(xylist.size()>1){
            	int ii=0;
            	Polygon pPolygon=new Polygon();
            	for(String[] items:xylist){
            		pPolygon.addPoint(Integer.valueOf(items[0]), Integer.valueOf(items[1]));
            		g.drawString(iconPath.get(ii), Float.valueOf(items[0])-(int)(rd.getWidth()/2), Float.valueOf(items[1])-OvalWidth-OvalWidthSmall);
            		for(int i=0;i<3;i++){
                		OvalWidth=OvalWidth-i;
                		g.drawOval(Integer.valueOf(items[0])-OvalWidth,
                				Integer.valueOf(items[1])-OvalWidth, OvalWidth*2, OvalWidth*2);
                	}
                	g.fillOval(Integer.valueOf(items[0])-OvalWidthSmall,
                			Integer.valueOf(items[1])-OvalWidthSmall, OvalWidthSmall*2, OvalWidthSmall*2);
                	ii++;
            	}
            	
            	g.drawPolygon(pPolygon);
            }else{
            	g.drawString(iconPath.get(0), Integer.valueOf(xylist.get(0)[0])-(int)(rd.getWidth()/2), Integer.valueOf(xylist.get(0)[1])-OvalWidth-OvalWidthSmall);
            	for(int i=0;i<3;i++){
            		OvalWidth=OvalWidth-i;
            		g.drawOval(Integer.valueOf(xylist.get(0)[0])-OvalWidth,
            				Integer.valueOf(xylist.get(0)[1])-OvalWidth, OvalWidth*2, OvalWidth*2);
            	}
            	g.fillOval(Integer.valueOf(xylist.get(0)[0])-OvalWidthSmall,
            			Integer.valueOf(xylist.get(0)[1])-OvalWidthSmall, OvalWidthSmall*2, OvalWidthSmall*2);
            }
            
  
            g.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER));   
  
            g.dispose();   
  
            os = new FileOutputStream(targerPath);   
  
            // 生成图片   
            ImageIO.write(buffImg, "JPG", os);   
  
            log("图片:"+filename+" 完成添加!");   
        } catch (Exception e) {   
            e.printStackTrace();   
        } finally {   
            try {   
                if (null != os)   
                    os.close();   
            } catch (Exception e) {   
                e.printStackTrace();   
            }   
        }   
    }  
}  