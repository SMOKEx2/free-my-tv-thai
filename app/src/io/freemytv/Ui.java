package io.freemytv;

import android.content.Context;
import android.content.res.AssetManager;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;
import android.graphics.Typeface;
import android.os.Build;

import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;
import java.util.function.Supplier;

/**
 * Fonts and text for the home screen, the screensaver and the settings. Font: Inter (variable, assets/fonts, SIL OFL),
 * with the "display" optical size for large text and the "text" size for small text; without it, the system font at a
 * similar weight.
 */
final class Ui {
    private Ui() {}

    /** Android 9 to 11: older TVs and boxes, whose GPUs need the cheaper drawing paths (Shadows, rounded images). */
    static final boolean LEGACY = Build.VERSION.SDK_INT < 31;
    static final Locale PT = new Locale("pt", "BR");
    /** English, Portuguese, Spanish or Thai, from the settings or, with "auto", the TV's own language. */
    static volatile String language = language();
    static volatile boolean en = "en".equals(language), es = "es".equals(language), th = "th".equals(language);
    static Typeface thin, light, displayMedium, displaySemibold, regular, medium, semibold;
    private static AssetManager assets;
    private static final Rect BOUNDS = new Rect();
    private static final RectF OVAL = new RectF();

    static synchronized void init(Context c) {
        assets = c.getAssets();
        loadFonts();
    }

    private static void loadFonts() {
        if (assets == null) return;
        thin = font(assets, 32, 200);
        light = font(assets, 32, 300);
        displayMedium = font(assets, 32, 500);
        displaySemibold = font(assets, 32, 600);
        regular = font(assets, 14, 400);
        medium = font(assets, 14, 500);
        semibold = font(assets, 14, 600);
    }

    /** Inter for Latin, Noto Sans Thai when the Thai UI is selected; both use variable weights. */
    private static Typeface font(AssetManager a, int opticalSize, int weight) {
        if (th && has(a, THAI_FONT)) {
            try {
                Typeface t = new Typeface.Builder(a, THAI_FONT)
                        .setFontVariationSettings("'wdth' 100, 'wght' " + weight).build();
                if (t != null) return t;
            } catch (RuntimeException ignored) {
            }
        }
        if (has(a, FONT)) {
            try {
                Typeface t = new Typeface.Builder(a, FONT)
                        .setFontVariationSettings("'opsz' " + opticalSize + ", 'wght' " + weight).build();
                if (t != null) return t;
            } catch (RuntimeException ignored) {
            }
        }
        return Typeface.create(Typeface.DEFAULT, weight, false);
    }

    private static final String FONT = "fonts/InterVariable.ttf";
    private static final String THAI_FONT = "fonts/NotoSansThai.ttf";

    /** "pt", "es" or "en": the one picked (TV settings or config.properties), or with "auto" the TV's own, else English. */
    private static String language() {
        String lang = Prefs.language();
        if (!lang.equals("auto")) return lang;
        lang = Locale.getDefault().getLanguage();
        return "pt".equals(lang) || "es".equals(lang) || "th".equals(lang) ? lang : "en";
    }

    /** After the language changes in the settings (and once Prefs can read them). */
    static void applyLanguage() {
        language = language();
        en = "en".equals(language);
        es = "es".equals(language);
        th = "th".equals(language);
        synchronized (Ui.class) { loadFonts(); }
    }

    private static boolean has(AssetManager a, String path) {
        try (InputStream in = a.open(path)) {
            return in != null;
        } catch (IOException e) {
            return false;
        }
    }

    static Paint text(Typeface face, float size, int color) {
        Paint p = new Paint(Paint.ANTI_ALIAS_FLAG | Paint.SUBPIXEL_TEXT_FLAG);
        p.setTypeface(face);
        p.setTextSize(size);
        p.setColor(color);
        return p;
    }

    /** Fixed-width digits (the clock and the prices don't jitter when a digit changes). */
    static Paint numbers(Typeface face, float size, int color) {
        Paint p = text(face, size, color);
        p.setFontFeatureSettings("'tnum'");
        return p;
    }

    /** Height of capital letters (and digits) above the baseline. */
    static float cap(Paint p) {
        synchronized (BOUNDS) {
            p.getTextBounds("H8", 0, 2, BOUNDS);
            return -BOUNDS.top;
        }
    }

    /** Half the cap height: added to the center line, it gives the baseline that centers the text. */
    static float halfCap(Paint p) {
        return cap(p) / 2f;
    }

    /** Left bearing of the first character (large, thin fonts start a little inward). */
    static float leftBearing(Paint p, String s) {
        if (s.isEmpty()) return 0;
        synchronized (BOUNDS) {
            p.getTextBounds(s, 0, 1, BOUNDS);
            return BOUNDS.left;
        }
    }

    static int alpha(int color, float a) {
        int base = (color >>> 24) & 255;
        return (Math.round(base * Math.max(0, Math.min(1, a))) << 24) | (color & 0xFFFFFF);
    }

    static float clamp(float v) {
        return Math.max(0, Math.min(1, v));
    }

    static String tr(String pt, String english) {
        return th ? Thai.text(english) : es ? Spanish.text(english) : en ? english : pt;
    }

    static String tr(String pt, String english, String spanish) {
        return th ? Thai.text(english) : es ? spanish : en ? english : pt;
    }

    static Locale locale() {
        return th ? new Locale("th", "TH") : es ? spanish() : en ? Locale.US : PT;
    }

    /** The TV's own Spanish (es-MX, es-AR…) when it is in Spanish, Spain's otherwise. */
    private static Locale spanish() {
        Locale tv = Locale.getDefault();
        return "es".equals(tv.getLanguage()) ? tv : new Locale("es", "ES");
    }

    /** "21:47" (in English, "9:47", like the iPhone in the US). */
    static String clock(long now) {
        return en ? new SimpleDateFormat("h:mm", Locale.US).format(new Date(now))
                : new SimpleDateFormat("HH:mm", locale()).format(new Date(now));
    }

    /** "5:21" (sunrise and sunset; in English, "5:21 AM"). */
    static String time(long at) {
        return once("time", at, () -> en ? new SimpleDateFormat("h:mm a", Locale.US).format(new Date(at))
                : new SimpleDateFormat("H:mm", locale()).format(new Date(at)));
    }

    private static final HashMap<String, String> FORMATTED = new HashMap<>();

    /**
     * A formatted value, made once per language: the bottom drawer is redrawn on every frame of its focus animation,
     * and SimpleDateFormat and String.format there cost ~10 ms a frame on a Mi Box 3.
     */
    static String once(String kind, double value, Supplier<String> format) {
        String key = kind + '|' + language + '|' + value;
        synchronized (FORMATTED) {
            String s = FORMATTED.get(key);
            if (s == null) {
                if (FORMATTED.size() > 200) FORMATTED.clear();
                s = format.get();
                FORMATTED.put(key, s);
            }
            return s;
        }
    }

    /** "domingo, 18 de outubro" (lowercase, like the iPhone in Portuguese); "Sunday, October 18" in English. */
    static String date(long now) {
        return en ? new SimpleDateFormat("EEEE, MMMM d", Locale.US).format(new Date(now))
                : new SimpleDateFormat("EEEE, d 'de' MMMM", locale()).format(new Date(now));
    }

    /** Spinning arc (work in progress). */
    static void spinner(Canvas c, float cx, float cy, float r, float seconds, Paint stroke) {
        OVAL.set(cx - r, cy - r, cx + r, cy + r);
        c.drawArc(OVAL, (seconds * 360f) % 360f, 270f, false, stroke);
    }
}
