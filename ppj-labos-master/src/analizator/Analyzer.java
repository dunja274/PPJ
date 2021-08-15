package analizator;

import commons.ENKA;
import commons.Pair;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;

public class Analyzer {
    private HashMap<String, ENKA> data;
    private HashMap<Pair<String, String>, ArrayList<String>> rules;
    private String starting;

    public Analyzer(HashMap<String, ENKA> data, HashMap<Pair<String, String>, ArrayList<String>> rules, String starting) {

        this.data = data;
        this.rules = rules;
        this.starting = starting;
    }

    public void run() {
        StringBuilder file = new StringBuilder();
        try {
            InputStream is = new FileInputStream("C:\\Users\\Dino\\dev\\FER\\PPJ\\test\\test3.in");
            BufferedReader buf = new BufferedReader(new InputStreamReader(is));
            String line = buf.readLine();
            while (line != null) {
                file.append(line);
                file.append("\n");
                line = buf.readLine();
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        //  struktura izlaz = ime jedinke, red, leksicka jedinka
        //  lista struktura izlaz

        //  int i  i treba biti glbalna varijabla jer ga mijenjamo u funkciji pravila // pointer na trenutno slovo

        //  trenutno_stanje = pocetno
        //  string leksicka jedinka = ""
        //  lista prihvacena_stanja = "" (regexi koji su prosli)
        String currentState = this.starting;
        String lexUnit = "";
        ArrayList<String> accLexStates = new ArrayList<>();

        //  trenutni redak = 1
        int row = 1;
        int current;

        //  uzimamo znak po znak i predajemo ga pocetnim stanjima automata
        //  koji pripada trenutnom stanju, spremamo u listu leksickih jedinki
        for (current = 0; current < file.length(); current++) {

/*
            za svaki znak ulaznog programa:
            leksicka_jedinka += znak
            tmp lista = provuci kroz automat(trenutno_stanje, string leksicka_jedinka) // uvijek se lista overwritea novom listom*/

            //System.out.println(lexUnit);
            char curr = file.charAt(current);
            lexUnit += curr;

            var tmp = autoRun(currentState, lexUnit);

/*
            NE ///ako je lista prihvatljivih automata prazna -> continue
            ako lista nije prazna i ako ima vise od jednog prihvatljivog automata (size>1) nastavi dalje*/

            if (accLexStates.isEmpty()) {
                continue;
            } else {
/*
                ako tmp_lista nije prazna:
                prihvatljiva_stanja = tmp lista
*/
                if (!tmp.isEmpty()) {
                    accLexStates = tmp;
                }
                /*ako je tmp lista automata prazna:
                pogledaj jel ima ista u listi prihvacenih stanja;
                ako je lista prihvacenih stanja prazna:
                //oporavak od pogreske???
                ispis retka na kojem je greska i ispis prvog znaka leksicke jedinke
                //problem ako odbaci prvi znak a prvi znak+ostali iza njega nisu pogreska???
                // ne moze ovako*/

                else {
                    if (accLexStates.isEmpty()) {
                        System.out.println(row);
                        System.out.println(lexUnit);
                    } else {
                        lexUnit = lexUnit.substring(0, lexUnit.length() - 1);
                        var state = accLexStates.get(0);
                        current--;

                        lexUnit = rule(state, lexUnit);
                        accLexStates = new ArrayList<>();
                    }
                }
                /*
                inace ako je size liste prih stanja == 1 // ili ako nije prazna?? zbog pravila o poretku, uzima se prvo stanje
                leksicka_jedinka = leksicka_jedinka[:-1] //mice se zadnji znak jer je dodan znak s kojim jedinka ne spada nigdje
                uzmi to stanje (trebao bi size biti 1 uvijek)
                treba se vratit na proslu iteraciju petlje, vratiti zadnji znak  u neprocitane znakove ne prosla iteracija
                funkcija pravilo(stanje iz liste stanje key (pravilo+regex), lekscka_jednika)
                leksicka_jedinka = "" trebala bi biti return funkcije pravilo
                prihvatljiva_Stanja=""
            */
            }
        }
    }


    /*
        def provuci_kroz_automat(stanje, jedinka):
        idi po dictionaryju i svim keyevima koji sadrze trenutno stanje u substringu:
        provedi jedinku kroz sve automate
        spremi automate koji su zavrsili u prihvatiljivom stanju?? nez jel ih moze biti vise
    */
    public ArrayList<String> autoRun(String state, String unit) {
        ArrayList<String> tmp = new ArrayList<>();
        for (var entry : this.data.entrySet()) {
            if (!entry.getKey().contains(state)) {
                continue;
            }

            var states = entry.getValue().getTransitions().get(new Pair<>(0, '$'));
            if (states == null)
                continue;

            for (var idx = 0; idx < unit.length(); idx++) {
                for (var st : states) {
                    var trans = entry.getValue().ETransition(new Pair<>(st, unit.charAt(idx)));
                    for (var tran : trans) {
                        if (entry.getValue().getAcceptableState().contains(tran)) {
                            tmp.add(entry.getKey());
                        }
                    }
                }
            }

        }
        return tmp;
    }

    public String rule(String state, String lexUnit) {
        var resp = "";
        var st = this.rules.get(state);

        var tmp = st.get(0);
        if (tmp.equals("-")) {
            return resp;
        } else if (tmp.contains("<")) {
            resp = tmp;
        } else if (tmp.equals("NOVI_READ")) {
            return resp;
        } else if (tmp.contains("VRATI_SE")) {
            return resp;
        } else if (st.get(0) != "-") {
            resp = st.get(0);
            System.out.println(resp);
            // dodaj u listu struktura
        }
        return resp;
    }

/*
    def pravilo(stanje (key pravila nzapravo), jedinka):
    ide po dictionaryju pravila: stanje je zapravo key dictionaryja ne mora biti petlja(stanje+regex)
    idi po tom pravilu:
    ako je prvi value -:
            continue
    ako prvi value nije -:
    ime_jedinke = pravila[stanje].values[0]
    dodaj u listu struktura (ime jedinke, trenutni redak, jedinka)
    ako je udji u stanje:
    trenutno stanje = novo stanje
    ako je novi_redak:
    trenutni_redak ++;
    ako je vrati se x:
    jedinka[x:] uzmemo sve znakove od x i vratimo ih u pocetni niz (smanjujemo onaj i iz petlje??)
    uzmemo duljinu jedinke - x i za toliko vratimo pointer u nizu?
            //da bi radilo s oporavkom od gresaka od gore mozda resetirat leksicku jedinku ovdje i dodat joj znakove, a ne opet citat i vrtit automate?
            return ili "" ili novu lek jedinku ako postoji vrati se???
*/


}
