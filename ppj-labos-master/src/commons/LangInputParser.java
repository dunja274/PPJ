package commons;

import java.io.*;
import java.util.*;

public class LangInputParser {

    private ArrayList<String> fileContent;
    private List<String> lexStates;
    private List<String> lexTokens;
    public HashMap<Pair<String, String>, ArrayList<String>> lexRules;
    private HashMap<String, String> regExDict = new HashMap<>();



    public LangInputParser(String filePath) {
        try {
            fileContent = LangInputParser.ReadFileAsString(filePath);
        } catch (IOException e) {
            e.printStackTrace();
        }
        this.ParseFile();
    }

    private void ParseFile() {
        int part = -1;
        ArrayList<String> data = new ArrayList<>();

        for (String line : fileContent) {
            if (part == -1 && line.contains("%X ")) {
                part = 1;
            } else if (part == -1 && line.contains("%L ")) {
                part = 2;
            } else if (part == 2 && line.contains("<")) {
                part = 3;
            }

            switch (part) {
                case 1:
                    this.regExDict = RegExParse(data);
                    data = new ArrayList<>();
                    part = -1;
                    break;
                case 2:
                    this.lexStates = LexerStateParse(data);
                    data = new ArrayList<>();
                    break;
                case 3:
                    this.lexTokens = LexerTokenParse(data);
                    part = -1;
                    data = new ArrayList<>();
                    break;
                default:
                    break;
            }
            data.add(line);
        }
        this.lexRules = LexerRulesParse(data);

    }


    private static HashMap<String, String> RegExParse(ArrayList<String> data) {
        if(data.isEmpty()) return null;

        HashMap<String, String> dict = new HashMap<>();

        for (String line : data) {
            String[] arr = line.split(" ");
            dict.put(arr[0], arr[1]);
        }

        for (Map.Entry<String, String> right : dict.entrySet()) {
            for (Map.Entry<String, String> left : dict.entrySet()) {
                if (right.getValue().contains(left.getKey())) {
                    var key = left.getKey().replaceAll("\\{", "\\\\{");
                    key = key.replaceAll("\\}", "\\\\}");
                    var tmp = right.getValue().replaceAll(key, "(" + left.getValue() + ")");
                    dict.replace(right.getKey(), tmp);
                }
            }
        }
        return dict;
    }

    private List<String> LexerStateParse(ArrayList<String> data) {
        var states = new ArrayList<String>();
        for(var str : data)
        {
            str = str.replace("%X ", "");
            for(String state : str.split(" ")) {
                states.add(state.replace("\n", ""));
            }
        }
        return states;
    }

    private List<String> LexerTokenParse(ArrayList<String> data) {
        var states = new ArrayList<String>();
        for(var str : data)
        {
            str = str.replace("LX ", "");
            for(String state : str.split(" ")) {
                states.add(state.replace("\n", ""));
            }
        }
        return states;
    }

    public HashMap<Pair<String, String>, ArrayList<String>> getLexRules() {
        return lexRules;
    }

    private HashMap<Pair<String, String>, ArrayList<String>> LexerRulesParse(ArrayList<String> data) {
        HashMap<Pair<String, String>, ArrayList<String>> dict = new HashMap<>();

        Pair<String, String> ps = new Pair("", "");
        ArrayList<String> array = new ArrayList<>();

        boolean read = false;
        for(String line : data) {
            if(line.contains("<")) {
                ps = new Pair(line.substring(1, line.indexOf(">")), line.substring(line.indexOf(">") + 1));
            }

            if(line.contains("{")) {
                read = true;
            } else if(line.contains("}")) {
                var str = ps.second;
                str = str.replace("\\_", "_");

                if(regExDict != null)
                {
                    for(String regex : regExDict.keySet()) {
                        if(str.contains(regex)) {
                            var value = regExDict.get(regex);
                            var key = regex.replaceAll("\\{", "\\\\{");
                            key = key.replaceAll("\\}", "\\\\}");
                            str = str.replaceAll(key, value);
                        }
                    }
                }

                ps.second = str;
                dict.put(ps, array);
                read = false;
                ps = new Pair("", "");
                array = new ArrayList<>();
            } else if(read) {
                array.add(line);

            }
        }
        return dict;
    }


    public HashMap<String, String> GetRegExDict() {
        return regExDict;
    }

    public static ArrayList<String> ReadFileAsString(String filePath) throws IOException {
        ArrayList<String> file = null;
        try {
            InputStream is = new FileInputStream(filePath);
            BufferedReader buf = new BufferedReader(new InputStreamReader(is));

            file = new ArrayList<>();
            String line = buf.readLine();
            while (line != null) {
                file.add(line);
                line = buf.readLine();
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        return file;
    }

    public List<String> getLexStates() {
        return lexStates;
    }
}
