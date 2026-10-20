package io.freemytv;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;

/** Ordered user choices, with seven readable tiles per dock page. No total-app limit. */
final class ShelfPolicy {
    static final int PAGE_SIZE = 7;
    private ShelfPolicy() {}
    static List<String> packages(String csv) {
        LinkedHashSet<String> unique = new LinkedHashSet<>();
        for (String value : csv.split(",")) {
            String pkg = value.trim();
            if (pkg.matches("[A-Za-z_][A-Za-z0-9_]*(\\.[A-Za-z_][A-Za-z0-9_]*)+")) unique.add(pkg);
        }
        return new ArrayList<>(unique);
    }
    static int start(int index) { return Math.max(0, index) / PAGE_SIZE * PAGE_SIZE; }
    static int visibleCount(int first, int total) { return Math.max(0, Math.min(PAGE_SIZE, total - first)); }
    static boolean accessible(int index, int first, int total) {
        return index >= 0 && index < total && index >= first - 1 && index <= first + PAGE_SIZE;
    }
}
