package com.liu.htmlcore;


import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
  
/**  
 * 输出html报表 
 * @author lwh  
 */  
public class HtmlOutPutCore {   
  
	static String outName="";
	static String basePath="";
	static boolean logSwitch=false;
	static boolean cleanSwitch=false;

	static String startTime="";
	static String endTime="";
	static String apkPath="";
	static String aaptPath="";
	static String deviceName="";
	static String result="成功/失败 ???";
    /**  
     * @param args  
     */  
    public static void main(String[] args) {
        //from args过来
        if(args==null||args.length==0){
			System.out.println("error params is null!");
        	return;
        }
        for(String str:args){
        	String strp=str.trim().toLowerCase();
        	if(strp.startsWith("-log")||strp.startsWith("-l")){
    			try{
    				logSwitch=true;
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("path=")||strp.startsWith("p=")){
    			try{
    				basePath=str.split("=")[1];
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("out=")||strp.startsWith("o=")){
    			try{
    				outName=str.split("=")[1];
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("-clean")||strp.startsWith("-cl")){
    			try{
    				cleanSwitch=true;
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("endtime=")||strp.startsWith("et=")){
    			try{
    				endTime=str.split("=")[1];
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("starttime=")||strp.startsWith("st=")){
    			try{
    				startTime=str.split("=")[1];
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("apkpath=")||strp.startsWith("ap=")){
    			try{
    				apkPath=str.split("=")[1];
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("aaptpath=")||strp.startsWith("apt=")){
    			try{
    				aaptPath=str.split("=")[1];
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("devicename=")||strp.startsWith("dn=")){
    			try{
    				deviceName=str.split("=")[1];
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}else if(strp.startsWith("result=")||strp.startsWith("r=")){
    			try{
    				result=str.split("=")[1];
    			}catch (Exception e) {
    				e.printStackTrace();
    			}
        	}
        	log(strp);
        }

        String iconPath=basePath+"out\\"+outName+"\\icon.png";
        ApkInfo apkInfo=null;
		try {
//        	log("aaptPath:"+aaptPath);
//        	log("apkPath:"+apkPath);
			apkInfo = new ApkUtil(aaptPath).getApkInfo(apkPath);
            IconUtil.extractFileFromApk(apkPath, apkInfo.getApplicationIcon(), iconPath);  
//			log(apkInfo.toString());
		} catch (Exception e) {
			e.printStackTrace();
		}
        String outpath=basePath+"out\\"+outName+"\\index.htm";
        addOutPutDetailPage(basePath+"html_model\\chart_md.htm", basePath+"html_model\\options.txt",outpath,apkInfo);
        addOutPutDetailImgPage(basePath+"html_model\\chart_img_md.htm", basePath+"html_model\\sectionimg.txt",basePath+"out\\"+outName+"\\sh.htm",apkInfo);
        addToOutPutList(basePath+"html_model\\home_md.htm", basePath+"html_model\\section.txt", basePath+"out\\index.htm", "./"+outName+"/index.htm", outName, result, outName,apkInfo);
  }
  public static void log(String str){
	  if(logSwitch){
			System.out.println(str);
	  }
  }

  public static String getStringFromFile(String mdPath){
	  StringBuilder str = new StringBuilder();
      try {
              String tempStr = "";
              FileInputStream is = new FileInputStream(mdPath);//读取模块文件
              BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"));
              while ((tempStr = br.readLine()) != null)
            	  str.append(tempStr);
              is.close();
      } catch (IOException e) {
              e.printStackTrace();
              return "";
              
      }
      return str.toString();
  }
  /***
   * 添加到主列表页面
   * 将报表路径，结果添加到报表列表页面
   * 替换<!--###section###-->的内容
   * ###section-url###
   * ###section-title###
   * ###section-content###
   * ###section-datetime###
   * */
	public static boolean addToOutPutList(String mdPath, String sectionmdPath,
			String outputHtmlFile, String url, String title, String content,
			String date,ApkInfo apkInfo) {
		log("mdPath:" + mdPath);
		log("sectionmdPath:" + sectionmdPath);
		log("outputHtmlFile:" + outputHtmlFile);
		log("url:" + url);
		String mdPathStr = getStringFromFile(mdPath);
		File ff = new File(outputHtmlFile);
		if (cleanSwitch)
			ff.delete();
		if (ff.exists()) {
			mdPathStr = getStringFromFile(outputHtmlFile);
		}
		String mdSectionStr = getStringFromFile(sectionmdPath);
		long beginDate = (new Date()).getTime();
		try {
			url= url.replaceAll("\\\\", "\\\\\\\\\\\\\\\\");
			mdSectionStr = mdSectionStr.replaceAll("###section-url###", url);
			String appname="";
			if(null!=apkInfo)appname = apkInfo.getApplicationLable();// 替换掉模块中相应的地方
			mdSectionStr = mdSectionStr.replaceAll("###section-title###", appname+":"+title);
			mdSectionStr = mdSectionStr.replaceAll("###section-content###",	content);// 替换掉模块中相应的地方
			mdSectionStr = mdSectionStr.replaceAll("###section-datetime###",date);// 替换掉模块中相应的地方

			log("mdSectionStr:" + mdSectionStr);
			mdPathStr = mdPathStr.replaceAll("<!--###section.txt###-->",
					 "<!--###section.txt###-->" +mdSectionStr);// 替换掉模块中相应的地方

			// <!--###section.txt###-->
			File f = new File(outputHtmlFile);
			//BufferedWriter o = new BufferedWriter(new FileWriter(f));
			BufferedWriter o = new BufferedWriter(new OutputStreamWriter(
					   new FileOutputStream(f), "UTF-8"));
			o.write(mdPathStr);
			o.close();
			log("共用时：" + ((new Date()).getTime() - beginDate) + "ms");
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}


	  /***
	   * 生成报表页面
	   * **/
	public static boolean addOutPutDetailPage(String mdPath,
			String optionmdPath, String outputHtmlFile,ApkInfo apkInfo) {
		log("mdPath:" + mdPath);
		log("optionmdPath:" + optionmdPath);
		log("outputHtmlFile:" + outputHtmlFile);
		String mdPathStr = getStringFromFile(mdPath);
		String mdSectionStr = getStringFromFile(optionmdPath);
		log("outputHtmlFile:" + mdSectionStr);
		//log("outputHtmlFile:" + outputHtmlFile);
		long beginDate = (new Date()).getTime();
		try {
			StringBuilder sbx=new StringBuilder();
			StringBuilder sbser=new StringBuilder();
			String mempath=basePath+"out\\"+outName+"\\meminfo";
			ArrayList<MemInfo>  datamap=getMemList(mempath);
			sbx.append("[");
			sbser.append("[");
			
			for(MemInfo minfo:datamap) {
				sbx.append("'").append(Float.valueOf(minfo.getValue())/1000+"").append("',");
				sbser.append("'").append(minfo.getformatTime()).append("',");
			}
			sbx.deleteCharAt(sbx.length()-1);
			sbser.deleteCharAt(sbser.length()-1);
			sbx.append("]");
			sbser.append("]");
			log("x:"+sbx.toString());
			log("ser:"+sbser.toString());
			// ['周一','周二','周三','周四','周五','周六','周日']
			mdSectionStr = mdSectionStr.replaceAll("###opstionsxAxis###",sbx.toString());
			// [1, -2, 2, 5, 3, 2, 0]
			mdSectionStr = mdSectionStr.replaceAll("###opstionsxSeries###",sbser.toString());

			// ../html_model
			mdPathStr = mdPathStr.replaceAll("###startTime###",startTime);// 替换掉模块中相应的地方
			// ../html_model
			mdPathStr = mdPathStr.replaceAll("###endTime###",endTime);// 替换掉模块中相应的地方
			mdPathStr = mdPathStr.replaceAll("../html_model","../../html_model");// 替换掉模块中相应的地方
			// ../html_model
			if(null!=apkInfo)mdPathStr = mdPathStr.replaceAll("###appName###",apkInfo.getApplicationLable());// 替换掉模块中相应的地方

			if(null!=apkInfo)mdPathStr = mdPathStr.replaceAll("###versionName###",apkInfo.getVersionName());// 替换掉模块中相应的地方
			if(null!=apkInfo)mdPathStr = mdPathStr.replaceAll("###MinSdk###",apkInfo.getSdkVersion());// 替换掉模块中相应的地方
			if(null!=deviceName&&!"".equals(deviceName))mdPathStr = mdPathStr.replaceAll("###devicename###",deviceName);// 替换掉模块中相应的地方
			
//			String logpath=basePath+"out\\"+outName+"\\androidlog.txt";
//			logpath= logpath.replaceAll("\\\\", "\\\\\\\\");
//			###chart-log###
			
			mdPathStr = mdPathStr.replaceAll("###opstions###", mdSectionStr);// 替换掉模块中相应的地方
//			mdPathStr = mdPathStr.replaceAll("###chart-log###", logpath);// 替换掉模块中相应的地方

			File f = new File(outputHtmlFile);
			//BufferedWriter o = new BufferedWriter(new FileWriter(f));
			   BufferedWriter o = new BufferedWriter(new OutputStreamWriter(
					   new FileOutputStream(f), "UTF-8"));
			o.write(mdPathStr);
			o.close();
			log("共用时：" + ((new Date()).getTime() - beginDate) + "ms");
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}

public static class MemInfo implements Comparable{
	public String time;
	public String value;
	
	public MemInfo(String time, String value) {
		super();
		this.time = time;
		this.value = value;
	}
	@Override
	public int compareTo(Object arg0) {
		MemInfo obj = (MemInfo) arg0;  
        return Integer.valueOf(time) - Integer.valueOf(obj.time);  
	}
	public String getValue(){
		return value;
	}
	public String getformatTime(){
		return time.substring(0, 2)+":"+time.substring(2,4)+":"+time.substring(4,6);
	}
	@Override
	public String toString() {
		return "MemInfo [time=" + time + ", value=" + value + "]";
	}
	
	
}
	  /***
	   * 生成报表页面
	   * **/
	public static boolean addOutPutDetailImgPage(String mdPath,
			String optionmdPath, String outputHtmlFile,ApkInfo apkInfo) {
		log("mdPath:" + mdPath);
		log("optionmdPath:" + optionmdPath);
		log("outputHtmlFile:" + outputHtmlFile);
		String mdPathStr = getStringFromFile(mdPath);
		String mdSectionStr = getStringFromFile(optionmdPath);
		log("outputHtmlFile:" + mdSectionStr);
		//log("outputHtmlFile:" + outputHtmlFile);
		long beginDate = (new Date()).getTime();

		StringBuilder sbList=new StringBuilder();
		String fileurl="";
		
		File root = new File(basePath+"out\\"+outName+"\\img");
	    File[] files = root.listFiles();
	    for(File file:files){
	    	if(file.isFile()){
	    		fileurl=file.getAbsolutePath();
	    		fileurl= "./img/"+file.getName();
	    		String sss=mdSectionStr.replaceAll("###section-url###", fileurl);
	    		log(sss);
				sbList.append(sss);
	    	}
	    }
	
		try {
			// ../html_model
			
			if(null!=apkInfo)mdPathStr = mdPathStr.replaceAll("###appName###",apkInfo.getApplicationLable());// 替换掉模块中相应的地方
			mdPathStr = mdPathStr.replaceAll("../html_model","../../html_model");// 替换掉模块中相应的地方
			mdPathStr = mdPathStr.replaceAll("<!--###section###-->", sbList.toString());// 替换掉模块中相应的地方

			File f = new File(outputHtmlFile);
			   BufferedWriter o = new BufferedWriter(new OutputStreamWriter(
					   new FileOutputStream(f), "UTF-8"));
			o.write(mdPathStr);
			o.close();
			log("共用时：" + ((new Date()).getTime() - beginDate) + "ms");
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}


    public static ArrayList<MemInfo>   getCpuList(String filess){
    	return getInfoList(filess,2);
    }

    public static ArrayList<MemInfo>   getMemList(String filess){
    	return getInfoList(filess,1);
    }
    public static ArrayList<MemInfo>  getInfoList(String filess,int col){
        ArrayList<MemInfo> map=new ArrayList<MemInfo>();
		File root = new File(filess);
	    File[] files = root.listFiles();
	    for(File file:files){
	    	if(file.isFile()){
	    		String ss=getStringFromFile(file.getAbsolutePath());
//	            String str ="20532  3   0% S    13 1517432K  45852K  bg u0_a90   android.liu.weidata";

//adb shell top -n 1 -d 0.5| grep android.liu.weidata
//  PID PR CPU% S  #THR     VSS     RSS PCY UID      Name
//20532  3   0% S    13 1517432K  45852K  bg u0_a90   android.liu.weidata

//adb shell dumpsys meminfo android.liu.weidata | grep TOTAL
//TOTAL    27005    21548     2832        0    37199    23853    13345
//TOTAL    32970    26984     3180        0    42927    28896    14030
	    		String []list=ss.split(" ");
	            int i=0;
	            for(String s:list){
	            	if(null!=s&&!"".equals(s.trim())){
	            		if(i==col){
		            		map.add(new MemInfo(file.getName().substring(9, 15), s));
	            			break;
	            		}
	            		i++;
	            	}
	            }
	            Collections.sort(map); 
//	            System.out.println(map);
	    	}
	    }
	    return map;
    }

}  