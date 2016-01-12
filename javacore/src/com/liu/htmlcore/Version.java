package com.liu.htmlcore;

public class Version {


	/**
	 * 返回版本号。
	 * 
	 * @return
	 */
	public static String getVersion() {
		return String.format("%d.%d.%d", getMajorVersion(), getMinorVersion(), getRevisionNumber());
	}

	/**
	 * ` 返回主版本号。
	 * 
	 * @return
	 */
	public static int getMajorVersion() {
		return 1;
	}

	/**
	 * 返回次版本号。
	 * 
	 * @return
	 */
	public static int getMinorVersion() {
		return 1;
	}

	/**
	 * 返回修正版本号。
	 * 
	 * @return
	 */
	public static int getRevisionNumber() {
		return 0;
	}
}
