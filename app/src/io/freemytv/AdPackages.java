package io.freemytv;

import java.util.Arrays;

/** Conservative ad/analytics subset researched from cleanyourtv's Mi Box lists; no general debloat. */
final class AdPackages {
    private AdPackages() {}
    private static final String[] XIAOMI = {
        "com.miui.tv.analytics", "com.xiaomi.statistic", "tv.alphonso.alphonso_eula",
        "com.google.android.feedback", "com.google.android.tv.bugreportsender",
        "com.android.tv.feedbackconsent", "com.mitv.tvhome.oemtab", "com.mitv.tvhome.michannel",
        "com.xm.webcontent", "android.autoinstalls.config.xioami.mibox3",
        "android.autoinstalls.config.soc.amlogic"
    };
    static String[] forDevice(String manufacturer, String brand) {
        return "xiaomi".equalsIgnoreCase(manufacturer) || "xiaomi".equalsIgnoreCase(brand)
                ? XIAOMI.clone() : new String[0];
    }
    static boolean isAd(String pkg) { return Arrays.asList(XIAOMI).contains(pkg); }
}
