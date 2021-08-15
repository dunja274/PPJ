package commons;

import java.util.*;

public class ENKA {

    private HashMap<Pair<Integer, Character>, ArrayList<Integer>> transitions;
    private int count = 0;
    private ArrayList<Integer> acceptableState;

    public ENKA() {
        transitions = new HashMap<>();
        acceptableState = new ArrayList<>();
    }

    public ENKA(HashMap<Pair<Integer, Character>, ArrayList<Integer>> transitions, ArrayList<Integer> acceptableState)
    {
        this.transitions = transitions;
        this.acceptableState = acceptableState;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ENKA enka = (ENKA) o;
        return count == enka.count &&
                Objects.equals(transitions, enka.transitions) &&
                Objects.equals(acceptableState, enka.acceptableState);
    }

    @Override
    public int hashCode() {
        return Objects.hash(transitions, count, acceptableState);
    }

    private int NewState() {
        count = count + 1;
        return count - 1;
    }

    private Boolean IsOperator(String exp, int idx) {
        int br = 0;
        while (idx - 1 >= 0 && exp.charAt(idx - 1) == '\\') {
            br++;
            idx = idx - 1;
        }
        return br % 2 == 0;
    }

    private int IdxGroup(String exp, int curr, int size) {
        if (size == 0)
            return 0;

        List<String> tmps = Arrays.asList(exp.split("|"));
        int res = exp.indexOf(tmps.get(size));

        if (res == -1)
            return 0;

        return res < curr ? res : 0;
    }

    public Pair<Integer, Integer> RegexToENKA(String regex) {
        ArrayList<String> choices = new ArrayList<>();
        int brackets = 0;
        int lastCut = 0;
        for (int i = 0; i < regex.length(); i++) {
            char curr = regex.charAt(i);

            if (curr == '(' && IsOperator(regex, i))
                brackets++;
            else if (curr == ')' && IsOperator(regex, i))
                brackets--;
            else if (brackets == 0 && curr == '|' && IsOperator(regex, i)) {
                if (lastCut != 0)
                    choices.add(regex.substring(lastCut + 1, i));
                else
                    choices.add(regex.substring(lastCut, i));
                lastCut = i;
            }

        }

        if (choices.size() > 1)
            choices.add(regex.substring(lastCut + 1, regex.length()));

        int left = NewState();
        int right = NewState();

        if (choices.size() > 1) {
            for (int i = 0; i < choices.size(); i++) {
                Pair<Integer, Integer> tmp = RegexToENKA(choices.get(i));
                AddEpsilonState(left, tmp.first);
                AddEpsilonState(right, tmp.second);
            }
        } else {
            Boolean prefix = false;
            Integer last = left;

            for (int i = 0; i < regex.length(); i++) {
                Integer a, b;
                char curr = regex.charAt(i);

                if (prefix) {
                    char transition;
                    prefix = false;
                    if (curr == 't')
                        transition = '\t';
                    else if (curr == 'n')
                        transition = '\n';
                    else if (curr == '_')
                        transition = ' ';
                    else
                        transition = curr;

                    a = NewState();
                    b = NewState();
                    AddTransition(a, b, transition);
                } else {
                    if (curr == '\\') {
                        prefix = true;
                        continue;
                    }
                    if (curr != '(') {
                        a = NewState();
                        b = NewState();

                        if (curr == '$')
                            AddEpsilonState(a, b);
                        else
                            AddTransition(a, b, curr);
                        // 2b
                    } else {
                        int j = 0;
                        int brOpen = 0;
                        int brClose = 0;
                        for (int k = 0; k < regex.length(); k++) {

                            char currNew = regex.charAt(k);

                            if (i >= k) {
                                if (currNew == '(' && IsOperator(regex, k))
                                    brOpen++;
                            }
                            if (currNew == ')' && IsOperator(regex, k))
                                brClose++;
                            if (brClose == brOpen && brOpen != 0 && k > i) {
                                j = k;
                                break;
                            }

                        }
                        Pair<Integer, Integer> tmp = RegexToENKA(regex.substring(i + 1, j + 1));
                        a = tmp.first;
                        b = tmp.second;
                        i = j;
                    }
                }

                if (i + 1 < regex.length() && regex.charAt(i + 1) == '*') {
                    int x = a;
                    int y = b;
                    a = NewState();
                    b = NewState();
                    AddEpsilonState(a, x);
                    AddEpsilonState(y, b);
                    AddEpsilonState(a, b);
                    AddEpsilonState(y, x);
                    i = i + 1;
                }

                AddEpsilonState(last, a);
                last = b;
            }
            AddEpsilonState(last, right);
        }

        acceptableState.add(right);
        AddEpsilonState(0, left);
        return new Pair<>(left, right);
    }

    private void AddEpsilonState(Integer left, Integer right) {
        AddTransition(left, right, '$');
    }

    private void AddTransition(Integer left, Integer right, Character transition) {
        Pair<Integer, Character> pair = new Pair(left, transition);
        ArrayList<Integer> tmp = this.transitions.get(pair);
        if (tmp == null)
            tmp = new ArrayList<>();
        if (!tmp.contains(right))
            tmp.add(right);

        if (transitions.get(pair) != null)
            this.transitions.replace(pair, tmp);
        else
            this.transitions.put(pair, tmp);
    }

    public ArrayList<Integer> ETransition(Pair<Integer, Character> delta) {
        Stack<Integer> stog = new Stack<>();
        ArrayList<Integer> Y = new ArrayList<>();

        var states = transitions.get(delta);
        if (states != null) {
            for (var state : states) {
                stog.push(state);
                Y.add(state);
            }
        }

        while (!stog.empty()) {
            Integer t = stog.pop();
            var etrans = transitions.get(new Pair<>(t, '$'));
            if (etrans != null) {
                for (Integer v : etrans) {
                    if (!Y.contains(v)) {
                        Y.add(v);
                        stog.push(v);
                    }
                }
            }
        }

        return Y;
    }

    public HashMap<Pair<Integer, Character>, ArrayList<Integer>> getTransitions() {
        return transitions;
    }

    public ArrayList<Integer> getAcceptableState() {
        return acceptableState;
    }
}
