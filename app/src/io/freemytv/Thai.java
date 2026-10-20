package io.freemytv;

import java.util.HashMap;
import java.util.Map;

/** Thai UI strings. Untranslated titles and service names stay in their original form. */
final class Thai {
    private Thai() {}

    private static final Map<String, String> TEXT = new HashMap<>();
    static {
        m("", "");
        m(" of ", " จาก ");
        m(" of 2", " จาก 2");
        m(" of 3", " จาก 3");
        m(", selected", ", เลือกแล้ว");
        m(", tab ", ", แท็บ ");
        m(". In use", ". กำลังใช้งาน");
        m("24h change", "เปลี่ยนแปลงใน 24 ชม.");
        m("Accept “Allow USB debugging?” on the TV (tick “Always allow”).", "กดยอมรับ “อนุญาตการแก้ไขข้อบกพร่อง USB?” บนทีวี (เลือก “อนุญาตเสมอ”)");
        m("All Apps", "แอปทั้งหมด");
        m("Android didn't accept the new home screen", "Android ไม่ยอมรับหน้าโฮมใหม่");
        m("Automatic", "อัตโนมัติ");
        m("COMPARISON", "เปรียบเทียบ");
        m("Connecting…", "กำลังเชื่อมต่อ…");
        m("Couldn't check Free My TV: ", "ตรวจสอบ Free My TV ไม่สำเร็จ: ");
        m("Couldn't go back to the original: ", "กลับไปหน้าเดิมไม่สำเร็จ: ");
        m("Couldn't open ", "เปิดไม่สำเร็จ ");
        m("Couldn't turn on Free My TV: ", "เปิด Free My TV ไม่สำเร็จ: ");
        m("Crypto", "คริปโท");
        m("Dark", "มืด");
        m("Disney and Globoplay: the TV itself controls those buttons.", "ปุ่ม Disney และ Globoplay ควบคุมโดยทีวี");
        m("Dollar", "ดอลลาร์");
        m("Error: ", "ข้อผิดพลาด: ");
        m("Fetching titles…", "กำลังโหลดรายการ…");
        m("For You", "สำหรับคุณ");
        m("Free My TV's home screen crashed 3 times in a row; I switched back to the original one.", "หน้าโฮม Free My TV ขัดข้อง 3 ครั้งติดกัน จึงกลับไปใช้หน้าโฮมเดิม");
        m("Free My TV's home screen ran into a problem.\nGoing back to the TV's original home screen…", "หน้าโฮม Free My TV พบปัญหา\nกำลังกลับไปหน้าโฮมเดิมของทีวี…");
        m("Free memory", "หน่วยความจำว่าง");
        m("HDMI Inputs", "อินพุต HDMI");
        m("Home Screen", "หน้าโฮม");
        m("Home Screen, ", "หน้าโฮม, ");
        m("Home Settings", "ตั้งค่าหน้าโฮม");
        m("Home button", "ปุ่ม Home");
        m("Home screen memory", "หน่วยความจำของหน้าโฮม");
        m("Inputs", "อินพุต");
        m("Language", "ภาษา");
        m("Light", "สว่าง");
        m("Live TV", "ทีวีสด");
        m("Measuring Free My TV…", "กำลังวัดประสิทธิภาพ Free My TV…");
        m("Measuring the original home screen…", "กำลังวัดประสิทธิภาพหน้าโฮมเดิม…");
        m("NOTICES", "การแจ้งเตือน");
        m("Netflix button", "ปุ่ม Netflix");
        m("No TMDB key: see the README (config.properties).", "ไม่พบ TMDB API key: ดูวิธีตั้งค่าใน README (config.properties)");
        m("No ads, with the new screensaver", "ไม่มีโฆษณา พร้อมภาพพักหน้าจอแบบใหม่");
        m("No weather data right now.", "ยังไม่มีข้อมูลสภาพอากาศ");
        m("None yet.", "ยังไม่มี");
        m("Not installed", "ยังไม่ได้ติดตั้ง");
        m("Nothing", "ไม่มี");
        m("OK or the arrows change the value.", "กด OK หรือปุ่มลูกศรเพื่อเปลี่ยนค่า");
        m("OK picks, Back cancels.", "กด OK เพื่อเลือก หรือ Back เพื่อยกเลิก");
        m("Off", "ปิด");
        m("On", "เปิด");
        m("On the TV: tick “Always allow” and press OK.", "บนทีวี เลือก “อนุญาตเสมอ” แล้วกด OK");
        m("Original", "หน้าเดิม");
        m("Original mode, but I couldn't turn back on: ", "กลับสู่โหมดเดิมแล้ว แต่เปิดสิ่งเหล่านี้กลับไม่สำเร็จ: ");
        m("Original mode: the factory home screen, screensaver and apps are back.", "กลับสู่โหมดเดิมแล้ว: คืนค่าหน้าโฮม ภาพพักหน้าจอ และแอปเดิมแล้ว");
        m("Preview", "ดูตัวอย่าง");
        m("Prime Video button", "ปุ่ม Prime Video");
        m("Quotes widget", "วิดเจ็ตราคาเหรียญ");
        m("RECOMMENDATIONS", "รายการแนะนำ");
        m("Remote Buttons", "ปุ่มบนรีโมต");
        m("Restoring the original home screen…", "กำลังกู้คืนหน้าโฮมเดิม…");
        m("Screensaver", "ภาพพักหน้าจอ");
        m("Screensaver, preview", "ภาพพักหน้าจอ, ดูตัวอย่าง");
        m("Series", "ซีรีส์");
        m("Settings", "การตั้งค่า");
        m("Shelf", "แถบแอป");
        m("Shortcuts", "ทางลัด");
        m("Starting…", "กำลังเริ่ม…");
        m("Sunrise ", "พระอาทิตย์ขึ้น ");
        m("Sunset ", "พระอาทิตย์ตก ");
        m("Switching takes a few seconds; the screen blinks while it measures.", "การสลับใช้เวลาสักครู่ หน้าจออาจกะพริบระหว่างวัดผล");
        m("Switching the home screen and screensaver…", "กำลังเปลี่ยนหน้าโฮมและภาพพักหน้าจอ…");
        m("TCL Channel button", "ปุ่ม TCL Channel");
        m("TV Settings", "การตั้งค่าทีวี");
        m("Temperature", "อุณหภูมิ");
        m("The TV update turned back on ", "การอัปเดตทีวีเปิดสิ่งเหล่านี้กลับมา ");
        m("The TV was updated; Free My TV is still on.", "ทีวีได้รับการอัปเดตแล้ว และ Free My TV ยังทำงานอยู่");
        m("The TV's factory home screen", "หน้าโฮมดั้งเดิมของทีวี");
        m("Theme", "ธีม");
        m("These are the TCL remote's buttons: on this TV, the buttons work as they always did.", "ปุ่มเหล่านี้คือปุ่มบนรีโมต TCL ซึ่งยังทำงานเหมือนเดิมบนทีวีเครื่องนี้");
        m("This product uses the TMDB API but is not endorsed or certified by TMDB.", "แอปนี้ใช้ TMDB API แต่ไม่ได้รับการรับรองหรือสนับสนุนจาก TMDB");
        m("Turned off what was missing: ", "ปิดแอปที่ยังเหลืออยู่: ");
        m("Turning apps back on (", "กำลังเปิดแอปกลับ (");
        m("Turning off apps (", "กำลังปิดแอป ( ");
        m("Turning the apps back on…", "กำลังเปิดแอปกลับ…");
        m("Weather", "สภาพอากาศ");
        m("Weather widget", "วิดเจ็ตสภาพอากาศ");
        m("YouTube button", "ปุ่ม YouTube");
        m("Your TV's home screen and screensaver", "หน้าโฮมและภาพพักหน้าจอของทีวี");
        m("no ads, with the new screensaver", "ไม่มีโฆษณา พร้อมภาพพักหน้าจอใหม่");
        m("not on the shelf", "ไม่ได้อยู่บนแถบแอป");
        m("now", "ตอนนี้");
        m("on the shelf, place ", "บนแถบแอป ลำดับที่ ");
        m("prices from ", "ราคา ณ ");
        m("the TV's factory home screen", "หน้าโฮมดั้งเดิมของทีวี");
        m("the home screen", "หน้าโฮม");
        m("the original home screen", "หน้าโฮมเดิม");
        m("the screensaver", "ภาพพักหน้าจอ");
    }

    private static void m(String english, String thai) { TEXT.put(english, thai); }

    static String text(String english) {
        String translated = TEXT.get(english);
        if (translated != null) return translated;
        if (english.matches("On · \\d+ titles from the TV's apps, 3 new ones every hour\\."))
            return "เปิดอยู่ · " + english.replaceAll("[^0-9]", " ").trim().split(" +")[0] + " เรื่องจากแอปบนทีวี เปลี่ยน 3 เรื่องทุกชั่วโมง";
        if (english.matches("Free My TV is on: new home screen and screensaver, \\d+ apps turned off\\."))
            return "เปิด Free My TV แล้ว: หน้าโฮมและภาพพักหน้าจอใหม่ ปิดแอป "
                    + english.replaceAll("[^0-9]", "").trim() + " แอป";
        return translated == null ? english : translated;
    }

    static String condition(int code, boolean day) {
        if (code < 0) return "";
        if (code == 0) return "ท้องฟ้าแจ่มใส";
        if (code == 1) return day ? "มีแดดเป็นส่วนใหญ่" : "ท้องฟ้าโปร่งเป็นส่วนใหญ่";
        if (code == 2) return "มีเมฆบางส่วน";
        if (code == 3) return "มีเมฆมาก";
        if (code == 45 || code == 48) return "มีหมอก";
        if (code >= 51 && code <= 57) return "ฝนปรอย";
        if (code == 65 || code == 67 || code == 82) return "ฝนตกหนัก";
        if (code >= 71 && code <= 77 || code == 85 || code == 86) return "หิมะตก";
        if (code >= 95) return "ฝนฟ้าคะนอง";
        return "ฝนตก";
    }
}
