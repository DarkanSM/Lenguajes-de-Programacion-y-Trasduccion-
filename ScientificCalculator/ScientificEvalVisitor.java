import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ScientificEvalVisitor
        extends ScientificCalcBaseVisitor<Double> {

    Map<String, Double> memory = new HashMap<>();

    // Reto 5: tabla de funciones definidas por el usuario -> f(x) = x^2 + 2*x + 1
    static class FunctionDef {
        String param;
        ScientificCalcParser.ExprContext body;

        FunctionDef(String param, ScientificCalcParser.ExprContext body) {
            this.param = param;
            this.body = body;
        }
    }

    Map<String, FunctionDef> functions = new HashMap<>();

    // ---------- Números ----------

    @Override
    public Double visitNumber(ScientificCalcParser.NumberContext ctx) {
        return Double.parseDouble(ctx.NUMBER().getText());
    }

    // ---------- Suma y resta ----------

    @Override
    public Double visitAddSub(ScientificCalcParser.AddSubContext ctx) {
        double left = visit(ctx.expr(0));
        double right = visit(ctx.expr(1));

        if (ctx.op.getType() == ScientificCalcParser.ADD) {
            return left + right;
        }

        return left - right;
    }

    // ---------- Multiplicación y división ----------

    @Override
    public Double visitMulDiv(ScientificCalcParser.MulDivContext ctx) {
        double left = visit(ctx.expr(0));
        double right = visit(ctx.expr(1));

        if (ctx.op.getType() == ScientificCalcParser.MUL) {
            return left * right;
        }

        if (right == 0) {
            System.err.println("Error: division por cero.");
            return 0.0;
        }

        return left / right;
    }

    // ---------- Paréntesis ----------

    @Override
    public Double visitParens(ScientificCalcParser.ParensContext ctx) {
        return visit(ctx.expr());
    }

    // ---------- Potencia ----------

    @Override
    public Double visitPower(ScientificCalcParser.PowerContext ctx) {
        double base = visit(ctx.expr(0));
        double exponent = visit(ctx.expr(1));

        return Math.pow(base, exponent);
    }

    // ---------- Operadores unarios ----------

    @Override
    public Double visitUnary(ScientificCalcParser.UnaryContext ctx) {
        double value = visit(ctx.expr());

        if (ctx.op.getText().equals("-")) {
            return -value;
        }

        return value;
    }

    // ---------- Funciones matemáticas de un argumento ----------
    // Reto 1: asin, acos, atan, floor, ceil agregados aquí

    @Override
    public Double visitFunctionCall(ScientificCalcParser.FunctionCallContext ctx) {
        String function = ctx.function().getText();
        double value = visit(ctx.expr());

        switch (function) {
            case "sin":
                return Math.sin(value);
            case "cos":
                return Math.cos(value);
            case "tan":
                return Math.tan(value);
            case "sqrt":
                return Math.sqrt(value);
            case "log":
                return Math.log10(value);
            case "ln":
                return Math.log(value);
            case "abs":
                return Math.abs(value);
            case "exp":
                return Math.exp(value);
            case "asin":
                return Math.asin(value);
            case "acos":
                return Math.acos(value);
            case "atan":
                return Math.atan(value);
            case "floor":
                return Math.floor(value);
            case "ceil":
                return Math.ceil(value);
            default:
                throw new RuntimeException("Funcion desconocida: " + function);
        }
    }

    // ---------- Reto 2: funciones con dos argumentos ----------

    @Override
    public Double visitFunctionCall2(ScientificCalcParser.FunctionCall2Context ctx) {
        String function = ctx.function2().getText();
        double a = visit(ctx.expr(0));
        double b = visit(ctx.expr(1));

        switch (function) {
            case "pow":
                return Math.pow(a, b);
            case "max":
                return Math.max(a, b);
            case "min":
                return Math.min(a, b);
            default:
                throw new RuntimeException("Funcion desconocida: " + function);
        }
    }

    // ---------- Constantes matemáticas ----------

    @Override
    public Double visitConstantExpr(ScientificCalcParser.ConstantExprContext ctx) {
        String constant = ctx.constant().getText();

        if (constant.equals("pi")) {
            return Math.PI;
        }

        if (constant.equals("e")) {
            return Math.E;
        }

        return 0.0;
    }

    // ---------- Variables ----------

    @Override
    public Double visitAssign(ScientificCalcParser.AssignContext ctx) {
        String id = ctx.ID().getText();
        double value = visit(ctx.expr());

        memory.put(id, value);

        return value;
    }

    @Override
    public Double visitId(ScientificCalcParser.IdContext ctx) {
        String id = ctx.ID().getText();

        if (memory.containsKey(id)) {
            return memory.get(id);
        }

        System.err.println("Variable no definida: " + id);
        return 0.0;
    }

    // ---------- Reto 5: definir funciones propias ----------
    // f(x) = x^2 + 2*x + 1

    @Override
    public Double visitFuncDef(ScientificCalcParser.FuncDefContext ctx) {
        String name = ctx.ID(0).getText();
        String param = ctx.ID(1).getText();

        functions.put(name, new FunctionDef(param, ctx.expr()));

        System.out.println("Funcion " + name + "(" + param + ") definida.");

        return 0.0;
    }

    @Override
    public Double visitUserFunctionCall(ScientificCalcParser.UserFunctionCallContext ctx) {
        String name = ctx.ID().getText();

        if (!functions.containsKey(name)) {
            System.err.println("Funcion no definida: " + name);
            return 0.0;
        }

        FunctionDef def = functions.get(name);

        double argument = visit(ctx.expr());

        // Guardamos el valor anterior del parámetro (si existía como variable)
        // para no perderlo, y lo restauramos al terminar (evita efectos raros
        // si la variable ya se usaba con otro propósito fuera de la función).
        Double previous = memory.get(def.param);

        memory.put(def.param, argument);

        double result = visit(def.body);

        if (previous != null) {
            memory.put(def.param, previous);
        } else {
            memory.remove(def.param);
        }

        return result;
    }

    // ---------- Mostrar resultados ----------

    @Override
    public Double visitPrintExpr(ScientificCalcParser.PrintExprContext ctx) {
        double value = visit(ctx.expr());
        System.out.println(value);
        return value;
    }

    // ---------- Comando clear ----------

    @Override
    public Double visitClear(ScientificCalcParser.ClearContext ctx) {
        memory.clear();
        functions.clear();
        System.out.println("Memoria eliminada.");
        return 0.0;
    }

    // ---------- Comando vars ----------

    @Override
    public Double visitShowVars(ScientificCalcParser.ShowVarsContext ctx) {
        if (memory.isEmpty() && functions.isEmpty()) {
            System.out.println("No hay variables ni funciones definidas.");
            return 0.0;
        }

        for (Map.Entry<String, Double> entry : memory.entrySet()) {
            System.out.println(entry.getKey() + " = " + entry.getValue());
        }

        for (Map.Entry<String, FunctionDef> entry : functions.entrySet()) {
            System.out.println(
                entry.getKey() + "(" + entry.getValue().param + ") = <funcion>"
            );
        }

        return 0.0;
    }

    // ---------- Comando plot (una función, con Reto 3: ymin/ymax opcional) ----------

    @Override
    public Double visitPlotExpr(ScientificCalcParser.PlotExprContext ctx) {
        double xmin = visit(ctx.expr(1));
        double xmax = visit(ctx.expr(2));

        int samples = 800;

        List<Double> xs = new ArrayList<>();
        List<Double> ys = new ArrayList<>();

        for (int i = 0; i < samples; i++) {
            double x = xmin + i * (xmax - xmin) / (samples - 1);

            memory.put("x", x);

            double y = visit(ctx.expr(0));

            // Solo almacenamos valores válidos (evita Infinity / NaN,
            // por ejemplo en discontinuidades como 1/x en x=0)
            if (Double.isFinite(y)) {
                xs.add(x);
                ys.add(y);
            }
        }

        // Reto 3: si el usuario indicó ymin,ymax además de xmin,xmax
        // (plot(expr, xmin, xmax, ymin, ymax)), usamos ese rango fijo
        // en lugar de calcularlo automáticamente a partir de los datos.
        if (ctx.expr().size() == 5) {
            double ymin = visit(ctx.expr(3));
            double ymax = visit(ctx.expr(4));
            new PlotWindow(xs, ys, ymin, ymax);
        } else {
            new PlotWindow(xs, ys);
        }

        return 0.0;
    }

    // ---------- Reto 4: graficar varias funciones a la vez ----------
    // plot(sin(x), cos(x); -6.28, 6.28)

    @Override
    public Double visitPlotMulti(ScientificCalcParser.PlotMultiContext ctx) {
        int totalExpr = ctx.expr().size();

        // Los últimos dos expr son xmin y xmax; todos los anteriores
        // son las funciones a graficar (separadas por coma, antes del ';').
        double xmin = visit(ctx.expr(totalExpr - 2));
        double xmax = visit(ctx.expr(totalExpr - 1));

        int samples = 800;
        int numFunctions = totalExpr - 2;

        List<String> labels = new ArrayList<>();
        List<List<Double>> allYs = new ArrayList<>();
        List<Double> xs = new ArrayList<>();

        for (int f = 0; f < numFunctions; f++) {
            labels.add(ctx.expr(f).getText());
            allYs.add(new ArrayList<>());
        }

        for (int i = 0; i < samples; i++) {
            double x = xmin + i * (xmax - xmin) / (samples - 1);
            memory.put("x", x);

            boolean allFinite = true;
            List<Double> valuesAtX = new ArrayList<>();

            for (int f = 0; f < numFunctions; f++) {
                double y = visit(ctx.expr(f));
                valuesAtX.add(y);
                if (!Double.isFinite(y)) {
                    allFinite = false;
                }
            }

            // Para simplificar el dibujo, solo conservamos los puntos
            // donde TODAS las funciones son válidas en ese x.
            if (allFinite) {
                xs.add(x);
                for (int f = 0; f < numFunctions; f++) {
                    allYs.get(f).add(valuesAtX.get(f));
                }
            }
        }

        new PlotWindow(labels, xs, allYs);

        return 0.0;
    }
}
