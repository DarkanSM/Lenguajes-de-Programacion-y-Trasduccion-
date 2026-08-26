import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ScientificEvalVisitor
        extends ScientificCalcBaseVisitor<Double> {

    Map<String, Double> memory = new HashMap<>();

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

    // ---------- Funciones matemáticas ----------

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
        System.out.println("Memoria eliminada.");
        return 0.0;
    }

    // ---------- Comando vars ----------

    @Override
    public Double visitShowVars(ScientificCalcParser.ShowVarsContext ctx) {
        if (memory.isEmpty()) {
            System.out.println("No hay variables definidas.");
            return 0.0;
        }

        for (Map.Entry<String, Double> entry : memory.entrySet()) {
            System.out.println(entry.getKey() + " = " + entry.getValue());
        }

        return 0.0;
    }

    // ---------- Comando plot ----------

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

        new PlotWindow(xs, ys);

        return 0.0;
    }
}
