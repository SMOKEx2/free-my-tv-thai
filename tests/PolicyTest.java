package io.freemytv;

public final class PolicyTest {
    public static void main(String[] args) {
        check(ShelfPolicy.packages(" a.one,b.two,a.one,invalid, ").size() == 2, "ordered deduplication");
        check(ShelfPolicy.start(0) == 0 && ShelfPolicy.start(6) == 0, "first seven");
        check(ShelfPolicy.start(7) == 7 && ShelfPolicy.start(14) == 14, "page boundaries");
        check(ShelfPolicy.visibleCount(7, 8) == 1 && ShelfPolicy.visibleCount(7, 14) == 7, "partial pages");
        check(ShelfPolicy.accessible(7, 0, 15), "next page reachable to TalkBack");
        check(ShelfPolicy.accessible(6, 7, 15), "previous page reachable to TalkBack");
        check(!ShelfPolicy.accessible(14, 0, 15), "only adjacent page edge exposed");
        check(PackageState.needsRecovery(false, 1, false), "partial activation can retry Original");
        check(PackageState.needsRecovery(false, 0, true), "Home/dream-only recovery can retry");
        check(!PackageState.needsRecovery(false, 0, false), "untouched Original needs no recovery");
        try {
            java.io.File dir = java.nio.file.Files.createTempDirectory("journal-test").toFile();
            java.io.File target = new java.io.File(dir, "state");
            RecoveryFile.write(target, "baseline".getBytes("UTF-8"));
            check(new String(java.nio.file.Files.readAllBytes(target.toPath()), "UTF-8").equals("baseline"), "journal persisted");
            RecoveryFile.write(target, "progress".getBytes("UTF-8"));
            check(new String(java.nio.file.Files.readAllBytes(target.toPath()), "UTF-8").equals("progress"), "journal atomically replaced");
            check(!PackageState.busy(200000, 1), "interrupted busy state expires");
            check(PackageState.busy(1000, 900), "active operation remains busy");
            boolean failed = false;
            try { RecoveryFile.write(new java.io.File(target, "impossible"), new byte[0]); }
            catch (java.io.IOException expected) { failed = true; }
            check(failed, "journal write failure propagates before mutations");
            target.delete(); dir.delete();
        } catch (java.io.IOException e) { throw new AssertionError(e); }
        check(AdPackages.forDevice("Xiaomi", "Xiaomi").length > 0, "Xiaomi ads available");
        check(AdPackages.forDevice("Sony", "Sony").length == 0, "no Xiaomi policy on other brands");
        for (String pkg : new String[] {"com.google.android.gms", "com.xiaomi.tvqs.overseas.y24",
                "com.xiaomi.android.tvsetup.partnercustomizer", "com.android.bluetooth", "com.google.android.apps.mediashell"}) {
            check(!AdPackages.isAd(pkg), "essential package protected: " + pkg);
        }
        check(!PackageState.shouldDisable(3, false), "predisabled package preserved");
        check(!PackageState.shouldDisable(2, false), "system-disabled package preserved");
        check(PackageState.shouldDisable(0, false), "default enabled can change");
        check(PackageState.restoreCommand(0, "a.b").equals("pm default-state --user 0 a.b"), "default state recovery");
        check(PackageState.restoreCommand(3, "a.b").equals("pm disable-user --user 0 a.b"), "disabled state recovery");
        boolean rejected = false;
        try { PackageState.restoreCommand(0, "bad;reboot"); } catch (IllegalArgumentException e) { rejected = true; }
        check(rejected, "no shell injection");
        check(Thai.condition(65, true).equals("ฝนตกหนัก"), "Thai weather");
        check(Thai.text("On · 24 titles from the TV's apps, 3 new ones every hour.").contains("24 เรื่อง"), "dynamic Thai count");
        System.out.println("PASS Java shelf/ad/recovery policies");
    }
    private static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
}
