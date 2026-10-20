package io.freemytv;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Package-manager enabled states must survive an Original/Free round trip unchanged. */
final class PackageState {
    private PackageState() {}
    static boolean needsRecovery(boolean free, int pending, boolean baseline) { return free || pending > 0 || baseline; }
    static boolean busy(long now, long at) { return at > 0 && now >= at && now - at < 180000; }
    static boolean shouldDisable(int before, boolean alreadyOwned) { return alreadyOwned || before == 0 || before == 1; }
    static int parse(String dump) {
        Matcher m = Pattern.compile("User 0:.*?\\benabled=([0-4])").matcher(dump);
        if (!m.find()) throw new IllegalArgumentException("Cannot read package enabled state");
        return Integer.parseInt(m.group(1));
    }
    static String restoreCommand(int before, String pkg) {
        if (!pkg.matches("[A-Za-z_][A-Za-z0-9_]*(\\.[A-Za-z_][A-Za-z0-9_]*)+"))
            throw new IllegalArgumentException("Invalid package ID");
        String[] actions = {"default-state", "enable", "disable", "disable-user", "disable-until-used"};
        if (before < 0 || before >= actions.length) throw new IllegalArgumentException("Invalid package state");
        return "pm " + actions[before] + " --user 0 " + pkg;
    }
}
