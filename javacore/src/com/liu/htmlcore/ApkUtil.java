package com.liu.htmlcore;

import java.io.BufferedReader;
import java.io.Closeable;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;


public class ApkUtil {

	public static final String VERSION_CODE = "versionCode";
	public static final String VERSION_NAME = "versionName";
	public static final String SDK_VERSION = "sdkVersion";
	public static final String TARGET_SDK_VERSION = "targetSdkVersion";
	public static final String USES_PERMISSION = "uses-permission";
	public static final String APPLICATION_LABEL = "application-label";
	public static final String APPLICATION_ICON = "application-icon";
	public static final String USES_FEATURE = "uses-feature";
	public static final String USES_IMPLIED_FEATURE = "uses-implied-feature";
	public static final String SUPPORTS_SCREENS = "supports-screens";
	public static final String SUPPORTS_ANY_DENSITY = "supports-any-density";
	public static final String DENSITIES = "densities";
	public static final String PACKAGE = "package";
	public static final String APPLICATION = "application:";
	public static final String LAUNCHABLE_ACTIVITY = "launchable-activity";

	private ProcessBuilder mBuilder;
	private static final String SPLIT_REGEX = "(: )|(=')|(' )|'";
	private static final String FEATURE_SPLIT_REGEX = "(:')|(',')|'";
	/**
	 * aapt所在的目录。
	 */
	private String mAaptPath = "lib/aapt";

	public ApkUtil(String aaptpath) {
		mAaptPath=aaptpath;
		mBuilder = new ProcessBuilder();
		mBuilder.redirectErrorStream(true);
	}

	/**
	 * 返回一个apk程序的信息。
	 * 
	 * @param apkPath
	 *            apk的路径。
	 * @return apkInfo 一个Apk的信息。
	 */
	public ApkInfo getApkInfo(String apkPath) throws Exception {
		Process process = mBuilder.command(mAaptPath, "d", "badging", apkPath)
				.start();
		InputStream is = null;
		is = process.getInputStream();
		BufferedReader br = new BufferedReader(
				new InputStreamReader(is, "utf8"));
		String tmp = br.readLine();
		try {
			if (tmp == null || !tmp.startsWith("package")) {
				throw new Exception("参数不正确，无法正常解析APK包。输出结果为:\n" + tmp + "...");
			}
			ApkInfo apkInfo = new ApkInfo();
			do {
				setApkInfoProperty(apkInfo, tmp);
			} while ((tmp = br.readLine()) != null);
			return apkInfo;
		} catch (Exception e) {
			throw e;
		} finally {
			process.destroy();
			closeIO(is);
			closeIO(br);
		}
	}

	/**
	 * 设置APK的属性信息。
	 * 
	 * @param apkInfo
	 * @param source
	 */
	private void setApkInfoProperty(ApkInfo apkInfo, String source) {
		if (source.startsWith(PACKAGE)) {
			splitPackageInfo(apkInfo, source);
		} else if(source.startsWith(LAUNCHABLE_ACTIVITY)){
			apkInfo.setLaunchableActivity(getPropertyInQuote(source));
		} else if (source.startsWith(SDK_VERSION)) {
			apkInfo.setSdkVersion(getPropertyInQuote(source));
		} else if (source.startsWith(TARGET_SDK_VERSION)) {
			apkInfo.setTargetSdkVersion(getPropertyInQuote(source));
		} else if (source.startsWith(USES_PERMISSION)) {
			apkInfo.addToUsesPermissions(getPropertyInQuote(source));
		} else if (source.startsWith(APPLICATION_LABEL)) {
			apkInfo.setApplicationLable(getPropertyInQuote(source));
		} else if (source.startsWith(APPLICATION_ICON)) {
			apkInfo.addToApplicationIcons(getKeyBeforeColon(source),
					getPropertyInQuote(source));
		} else if (source.startsWith(APPLICATION)) {
			String[] rs = source.split("( icon=')|'");
			apkInfo.setApplicationIcon(rs[rs.length - 1]);
		} else if (source.startsWith(USES_FEATURE)) {
			apkInfo.addToFeatures(getPropertyInQuote(source));
		} else if (source.startsWith(USES_IMPLIED_FEATURE)) {
			apkInfo.addToImpliedFeatures(getFeature(source));
		} else {
//			System.out.println(source);
		}
	}

	private ImpliedFeature getFeature(String source) {
		String[] result = source.split(FEATURE_SPLIT_REGEX);
		ImpliedFeature impliedFeature = new ImpliedFeature(result[1], result[2]);
		return impliedFeature;
	}

	/**
	 * 返回出格式为name: 'value'中的value内容。
	 * 
	 * @param source
	 * @return
	 */
	private String getPropertyInQuote(String source) {
		int index = source.indexOf("'") + 1;
		return source.substring(index, source.indexOf('\'', index));
	}

	/**
	 * 返回冒号前的属性名称
	 * 
	 * @param source
	 * @return
	 */
	private String getKeyBeforeColon(String source) {
		return source.substring(0, source.indexOf(':'));
	}

	/**
	 * 分离出包名、版本等信息。
	 * 
	 * @param apkInfo
	 * @param packageSource
	 */
	private void splitPackageInfo(ApkInfo apkInfo, String packageSource) {
		String[] packageInfo = packageSource.split(SPLIT_REGEX);
		apkInfo.setPackageName(packageInfo[2]);
		apkInfo.setVersionCode(packageInfo[4]);
		apkInfo.setVersionName(packageInfo[6]);
	}

	/**
	 * 释放资源。
	 * 
	 * @param c
	 *            将关闭的资源
	 */
	private final void closeIO(Closeable c) {
		if (c != null) {
			try {
				c.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	public static void main(String[] args) {
		try {
//			apkpath=g:\lwh\zhenkun\b2c1.apk
//				aaptpath=g:\lwh\xwandou\code\monkeytest\bin\aapt.exe
			String demo = "g:\\lwh\\zhenkun\\b2c1.apk";
			if (args.length > 0) {
				if(args[0].equals("-version") || args[0].equals("-v")){
					System.out.println("ApkUtil   -by Geek_Soledad");
					System.out.println("Version:" + Version.getVersion());
					return;
				}
				demo = args[0];
			}
			ApkInfo apkInfo = new ApkUtil("g:\\lwh\\xwandou\\code\\monkeytest\\bin\\aapt.exe").getApkInfo(demo);
			System.out.println(apkInfo);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public String getmAaptPath() {
		return mAaptPath;
	}

	public void setmAaptPath(String mAaptPath) {
		this.mAaptPath = mAaptPath;
	}
}
