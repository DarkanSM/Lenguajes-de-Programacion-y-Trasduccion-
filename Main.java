import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ParseTree;

public class Main {

    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.out.println("Uso: java Main <archivo_entrada>");
            return;
        }

        CharStream input = CharStreams.fromFileName(args[0]);
        InstruccionesLexer lexer = new InstruccionesLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        tokens.fill();

        System.out.println("=== TOKENS ===");
        for (Token t : tokens.getTokens()) {
            if (t.getType() == Token.EOF) {
                System.out.println("EOF");
            } else {
                String nombre = InstruccionesLexer.VOCABULARY.getSymbolicName(t.getType());
                System.out.println(nombre + " -> " + t.getText());
            }
        }

        tokens.seek(0);
        InstruccionesParser parser = new InstruccionesParser(tokens);
        ParseTree arbol = parser.programa();

        System.out.println("\n=== ARBOL SINTACTICO ===");
        System.out.println(arbol.toStringTree(parser));

        System.out.println("\nErrores de sintaxis: " + parser.getNumberOfSyntaxErrors());
    }
}
