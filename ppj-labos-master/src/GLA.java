import commons.ENKA;
import commons.LangInputParser;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

public class GLA {

    public static void main(String[] args) throws IOException {
        LangInputParser lip = new LangInputParser("C:\\Users\\Dino\\dev\\FER\\PPJ\\test\\test4.lan");

        HashMap<String, ENKA> automati = new HashMap<>();

        for (var reg : lip.lexRules.entrySet()) {
            var rule = reg.getKey().toString();
            rule = rule.replaceAll("/\\_ ", "\\_");
            var expression = reg.getKey().getSecond();

            var enka = automati.get(rule);
            if (enka != null) {
                enka.RegexToENKA(expression);
                automati.replace(rule, enka);
            } else {
                enka = new ENKA();
                enka.RegexToENKA(expression);
                automati.put(rule, enka);
            }
        }

        StringBuilder file = new StringBuilder();
        file.append("package analizator;\n" +
                "\n" +
                "import commons.ENKA;\n" +
                "import commons.Pair;import java.util.HashMap;\n" +
                "import java.util.ArrayList;\n" +
                "\n" +
                "public class LA {" +
                "public static void main(String[] args) { ");

        StringBuilder sb = new StringBuilder();
        sb.append("HashMap<String, ENKA> data = new HashMap<>() {{");

        for (var entry : automati.entrySet()) {
            String format = "put(\"%s\", new ENKA(new HashMap<>() {{ %s }}, new ArrayList<>() {{ %s }}));";
            StringBuilder enkaBuilder = new StringBuilder();
            var enkas = entry.getValue();

            StringBuilder transitions = new StringBuilder();
            for (var automat : enkas.getTransitions().entrySet()) {
                String transFormat = "put(new Pair<>%s, new ArrayList<>() {{ %s }});";
                StringBuilder stateBuilder = new StringBuilder();
                for (var state : automat.getValue()) {
                    String stateFormat = "add(%d);";
                    stateBuilder.append(String.format(stateFormat, state));
                }
                transitions.append(String.format(transFormat, automat.getKey(), stateBuilder));
            }

            StringBuilder accStatesBuilder = new StringBuilder();
            for (var state : enkas.getAcceptableState()) {
                accStatesBuilder.append(String.format("add(%d);", state));
            }

            var entryString = entry.getKey();
            entryString = entryString.replace("\\", "\\\\");
            entryString = entryString.replace("\"", "\\\"");
            entryString = entryString.replace("\n", "\\\n");
            enkaBuilder.append(String.format(format, entryString, transitions, accStatesBuilder));
            sb.append(enkaBuilder);
        }
        sb.append("}};");


        var states = lip.getLexRules();
        StringBuilder sb2 = new StringBuilder();
        sb2.append("HashMap<commons.Pair<String, String>, ArrayList<String>> rules = new HashMap<>() {{ ");

        for (var entry : states.entrySet()) {
            StringBuilder rules = new StringBuilder();
            String format = "put(new commons.Pair<>(\"%s\", \"%s\"), new ArrayList<>() {{ %s }});";

            for (var rule : entry.getValue()) {
                rules.append(String.format("add(\"%s\");", rule));
            }
            var tmpp = entry.getKey().getSecond();
            tmpp = tmpp.replace("\\", "\\\\");

            sb2.append(String.format(format, entry.getKey().getFirst(), tmpp, rules));
        }

        var starting = lip.getLexStates().get(0);
        file.append(sb);
        file.append(sb2);
        file.append(String.format("}}; new Analyzer(data, rules, \"%s\").run();", starting));
        file.append("}\n" +
                "}\n");

        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter("src/analizator/LA.java"));
            //writer.write("");
            writer.write(file.toString());
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
