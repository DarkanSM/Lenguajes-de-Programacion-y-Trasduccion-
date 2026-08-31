import javax.swing.*;
import java.awt.*;
import java.util.List;

public class PlotWindow extends JPanel {

    // ---- Modo simple: una sola función, rango automático ----
    private List<Double> xs;
    private List<Double> ys;
    private boolean fixedRange = false;
    private double fixedYmin, fixedYmax;

    // ---- Reto 4: modo múltiple, varias funciones a la vez ----
    private boolean multiMode = false;
    private List<String> labels;
    private List<List<Double>> allYs;

    private static final Color[] PALETTE = {
        Color.BLUE, Color.RED, new Color(0, 150, 0), Color.MAGENTA,
        Color.ORANGE, Color.CYAN, Color.DARK_GRAY
    };

    // Constructor original (paso 33 del tutorial): rango automático
    public PlotWindow(List<Double> xs, List<Double> ys) {
        this.xs = xs;
        this.ys = ys;
        openFrame();
    }

    // Reto 3: rango vertical fijo, indicado por el usuario
    public PlotWindow(List<Double> xs, List<Double> ys, double ymin, double ymax) {
        this.xs = xs;
        this.ys = ys;
        this.fixedRange = true;
        this.fixedYmin = ymin;
        this.fixedYmax = ymax;
        openFrame();
    }

    // Reto 4: varias funciones sobre el mismo eje x
    public PlotWindow(List<String> labels, List<Double> xs, List<List<Double>> allYs) {
        this.multiMode = true;
        this.labels = labels;
        this.xs = xs;
        this.allYs = allYs;
        openFrame();
    }

    private void openFrame() {
        JFrame frame = new JFrame("Scientific Calculator");
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frame.setSize(800, 600);
        frame.add(this);
        frame.setVisible(true);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        if (xs == null || xs.size() < 2) {
            return;
        }

        if (multiMode) {
            paintMulti(g2);
        } else {
            paintSingle(g2);
        }
    }

    private void paintSingle(Graphics2D g2) {
        if (ys.size() < 2) return;

        double xmin = xs.stream().mapToDouble(Double::doubleValue).min().orElse(-1);
        double xmax = xs.stream().mapToDouble(Double::doubleValue).max().orElse(1);

        double ymin, ymax;
        if (fixedRange) {
            ymin = fixedYmin;
            ymax = fixedYmax;
        } else {
            ymin = ys.stream().mapToDouble(Double::doubleValue).min().orElse(-1);
            ymax = ys.stream().mapToDouble(Double::doubleValue).max().orElse(1);
        }

        if (xmax == xmin) xmax = xmin + 1;
        if (ymax == ymin) ymax = ymin + 1;

        drawAxes(g2, xmin, xmax, ymin, ymax);

        g2.setColor(Color.BLUE);
        g2.setStroke(new BasicStroke(2f));
        drawSeries(g2, xs, ys, xmin, xmax, ymin, ymax);
    }

    private void paintMulti(Graphics2D g2) {
        double xmin = xs.stream().mapToDouble(Double::doubleValue).min().orElse(-1);
        double xmax = xs.stream().mapToDouble(Double::doubleValue).max().orElse(1);

        double ymin = Double.POSITIVE_INFINITY;
        double ymax = Double.NEGATIVE_INFINITY;

        for (List<Double> ySeries : allYs) {
            for (double y : ySeries) {
                if (y < ymin) ymin = y;
                if (y > ymax) ymax = y;
            }
        }

        if (xmax == xmin) xmax = xmin + 1;
        if (ymax <= ymin) { ymin -= 1; ymax += 1; }

        drawAxes(g2, xmin, xmax, ymin, ymax);

        for (int f = 0; f < allYs.size(); f++) {
            g2.setColor(PALETTE[f % PALETTE.length]);
            g2.setStroke(new BasicStroke(2f));
            drawSeries(g2, xs, allYs.get(f), xmin, xmax, ymin, ymax);
        }

        // Leyenda simple en la esquina superior izquierda
        int ly = 20;
        for (int f = 0; f < labels.size(); f++) {
            g2.setColor(PALETTE[f % PALETTE.length]);
            g2.fillRect(10, ly - 8, 12, 12);
            g2.setColor(Color.BLACK);
            g2.drawString(labels.get(f), 28, ly + 2);
            ly += 18;
        }
    }

    private void drawAxes(Graphics2D g2, double xmin, double xmax, double ymin, double ymax) {
        g2.setColor(Color.LIGHT_GRAY);
        if (ymin < 0 && ymax > 0) {
            int zeroY = getHeight() - (int) ((0 - ymin) / (ymax - ymin) * getHeight());
            g2.drawLine(0, zeroY, getWidth(), zeroY);
        }
        if (xmin < 0 && xmax > 0) {
            int zeroX = (int) ((0 - xmin) / (xmax - xmin) * getWidth());
            g2.drawLine(zeroX, 0, zeroX, getHeight());
        }
    }

    private void drawSeries(Graphics2D g2, List<Double> xs, List<Double> ys,
                             double xmin, double xmax, double ymin, double ymax) {

        int n = Math.min(xs.size(), ys.size());

        for (int i = 1; i < n; i++) {
            double x1 = xs.get(i - 1);
            double y1 = ys.get(i - 1);
            double x2 = xs.get(i);
            double y2 = ys.get(i);

            int px1 = (int) ((x1 - xmin) / (xmax - xmin) * getWidth());
            int py1 = getHeight() - (int) ((y1 - ymin) / (ymax - ymin) * getHeight());
            int px2 = (int) ((x2 - xmin) / (xmax - xmin) * getWidth());
            int py2 = getHeight() - (int) ((y2 - ymin) / (ymax - ymin) * getHeight());

            g2.drawLine(px1, py1, px2, py2);
        }
    }
}
