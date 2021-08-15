package analizator;

import commons.ENKA;
import commons.Pair;

import java.util.HashMap;
import java.util.ArrayList;

public class LA {
    public static void main(String[] args) {
        HashMap<String, ENKA> data = new HashMap<>() {{
            put("(S_p,abcd*)", new ENKA(new HashMap<>() {{
                put(new Pair<>(2, 'a'), new ArrayList<>() {{
                    add(3);
                }});
                put(new Pair<>(5, '$'), new ArrayList<>() {{
                    add(6);
                }});
                put(new Pair<>(3, '$'), new ArrayList<>() {{
                    add(4);
                }});
                put(new Pair<>(0, '$'), new ArrayList<>() {{
                    add(2);
                    add(0);
                }});
                put(new Pair<>(11, '$'), new ArrayList<>() {{
                    add(1);
                }});
                put(new Pair<>(10, '$'), new ArrayList<>() {{
                    add(8);
                    add(11);
                }});
                put(new Pair<>(9, '$'), new ArrayList<>() {{
                    add(11);
                    add(8);
                }});
                put(new Pair<>(8, 'd'), new ArrayList<>() {{
                    add(9);
                }});
                put(new Pair<>(6, 'c'), new ArrayList<>() {{
                    add(7);
                }});
                put(new Pair<>(7, '$'), new ArrayList<>() {{
                    add(10);
                }});
                put(new Pair<>(4, 'b'), new ArrayList<>() {{
                    add(5);
                }});
            }}, new ArrayList<>() {{
                add(1);
            }}));
            put("(S_p,xyz*)", new ENKA(new HashMap<>() {{
                put(new Pair<>(5, '$'), new ArrayList<>() {{
                    add(8);
                }});
                put(new Pair<>(3, '$'), new ArrayList<>() {{
                    add(4);
                }});
                put(new Pair<>(0, '$'), new ArrayList<>() {{
                    add(2);
                    add(0);
                }});
                put(new Pair<>(6, 'z'), new ArrayList<>() {{
                    add(7);
                }});
                put(new Pair<>(4, 'y'), new ArrayList<>() {{
                    add(5);
                }});
                put(new Pair<>(2, 'x'), new ArrayList<>() {{
                    add(3);
                }});
                put(new Pair<>(9, '$'), new ArrayList<>() {{
                    add(1);
                }});
                put(new Pair<>(8, '$'), new ArrayList<>() {{
                    add(6);
                    add(9);
                }});
                put(new Pair<>(7, '$'), new ArrayList<>() {{
                    add(9);
                    add(6);
                }});
            }}, new ArrayList<>() {{
                add(1);
            }}));
            put("(S_p,\\n)", new ENKA(new HashMap<>() {{
                put(new Pair<>(3, '$'), new ArrayList<>() {{
                    add(1);
                }});
                put(new Pair<>(0, '$'), new ArrayList<>() {{
                    add(2);
                    add(0);
                }});
                put(new Pair<>(2, '\n'), new ArrayList<>() {{
                    add(3);
                }});
            }}, new ArrayList<>() {{
                add(1);
            }}));
        }};
        HashMap<commons.Pair<String, String>, ArrayList<String>> rules = new HashMap<>() {{
            put(new commons.Pair<>("S_p", "xyz*"), new ArrayList<>() {{
                add("NIKAD");
            }});
            put(new commons.Pair<>("S_p", "\\n"), new ArrayList<>() {{
                add("-");
                add("NOVI_REDAK");
            }});
            put(new commons.Pair<>("S_p", "abcd*"), new ArrayList<>() {{
                add("NIKAD");
            }});
        }};
        new Analyzer(data, rules, "S_p").run();
    }
}
