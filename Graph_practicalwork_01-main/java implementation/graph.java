import java.io.*;
import java.util.*;

public class Graph {
    private Map<Integer, List<Edge>> outNeighbours = new HashMap<>();
    private Map<Integer, Edge> edges = new HashMap<>();
    private int edgeCount = 0;

    public Graph(String fileName) {
        readFromFile(fileName);
    }

    public Graph(int vertices) {
        for (int i = 0; i < vertices; i++) {
            outNeighbours.put(i, new ArrayList<>());
        }
    }

    private void readFromFile(String fileName) {
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line = br.readLine();
            String[] parts = line.split(" ");
            int vertices = Integer.parseInt(parts[0]);
            int edgesCount = Integer.parseInt(parts[1]);

            // Reinitialize the graph
            this.outNeighbours.clear();
            this.edges.clear();
            for (int i = 0; i < vertices; i++) {
                outNeighbours.put(i, new ArrayList<>());
            }

            while ((line = br.readLine()) != null) {
                String[] edgeParts = line.split(" ");
                int u = Integer.parseInt(edgeParts[0]);
                int v = Integer.parseInt(edgeParts[1]);
                int w = Integer.parseInt(edgeParts[2]);
                addEdge(u, v, w);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public boolean addEdge(int u, int v, int weight) {
        if (!outNeighbours.get(u).contains(new Edge(u, v, weight))) {
            outNeighbours.get(u).add(new Edge(u, v, weight));
            edges.put(edgeCount++, new Edge(u, v, weight));
            return true;
        }
        return false;
    }

    public boolean removeEdge(int u, int v) {
        List<Edge> edgesList = outNeighbours.get(u);
        return edgesList.removeIf(edge -> edge.getTarget() == v);
    }

    public boolean removeVertex(int vertex) {
        if (outNeighbours.containsKey(vertex)) {
            outNeighbours.remove(vertex);
            edges.values().removeIf(edge -> edge.getSource() == vertex || edge.getTarget() == vertex);
            return true;
        }
        return false;
    }

    public boolean addVertex(int vertex) {
        if (!outNeighbours.containsKey(vertex)) {
            outNeighbours.put(vertex, new ArrayList<>());
            return true;
        }
        return false;
    }

    public List<Edge> getOutboundEdges(int vertex) {
        return outNeighbours.get(vertex);
    }

    public Set<Integer> getVertices() {
        return outNeighbours.keySet();
    }

    public int getNumberOfVertices() {
        return outNeighbours.size();
    }

    public boolean isEdge(int u, int v) {
        for (Edge edge : outNeighbours.get(u)) {
            if (edge.getTarget() == v) {
                return true;
            }
        }
        return false;
    }

    public static void writeToFile(Graph graph, String fileName) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(fileName))) {
            bw.write(graph.getNumberOfVertices() + " " + graph.edges.size() + "\n");
            for (Edge edge : graph.edges.values()) {
                bw.write(edge.getSource() + " " + edge.getTarget() + " " + edge.getWeight() + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void generateRandomGraph(int numberVertices, int numberEdges) {
        for (int i = 0; i < numberEdges; i++) {
            int x = new Random().nextInt(numberVertices);
            int y = new Random().nextInt(numberVertices);
            int weight = new Random().nextInt(100) + 1;

            if (x != y && !isEdge(x, y)) {
                addEdge(x, y, weight);
            }
        }
    }

    public static Graph readGraphFromFile(String fileName) {
        Graph graph = null;
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line = br.readLine();
            String[] parts = line.split(" ");
            int vertices = Integer.parseInt(parts[0]);
            graph = new Graph(vertices);

            while ((line = br.readLine()) != null) {
                String[] edgeParts = line.split(" ");
                int u = Integer.parseInt(edgeParts[0]);
                int v = Integer.parseInt(edgeParts[1]);
                int w = Integer.parseInt(edgeParts[2]);
                graph.addEdge(u, v, w);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return graph;
    }

    // Edge class for storing edges
    public static class Edge {
        private final int source;
        private final int target;
        private final int weight;

        public Edge(int source, int target, int weight) {
            this.source = source;
            this.target = target;
            this.weight = weight;
        }

        public int getSource() {
            return source;
        }

        public int getTarget() {
            return target;
        }

        public int getWeight() {
            return weight;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Edge edge = (Edge) o;
            return source == edge.source && target == edge.target && weight == edge.weight;
        }

        @Override
        public int hashCode() {
            return Objects.hash(source, target, weight);
        }
    }
}

class GraphUI {
    private Graph graph;

    public GraphUI(Graph graph) {
        this.graph = graph;
    }

    public void loadGraphFromFileUI() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter file name to load the graph: ");
        String fileName = scanner.nextLine();
        this.graph = Graph.readGraphFromFile(fileName);
        System.out.println("Graph loaded from " + fileName);
    }

    public void saveGraphToFileUI() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter file name to save the graph: ");
        String fileName = scanner.nextLine();
        Graph.writeToFile(graph, fileName);
        System.out.println("Graph saved to " + fileName);
    }

    public void displayMenu() {
        System.out.println("\nGraph Menu:");
        System.out.println("1. Show Graph");
        System.out.println("2. Add Vertex");
        System.out.println("3. Remove Vertex");
        System.out.println("4. Add Edge");
        System.out.println("5. Remove Edge");
        System.out.println("6. Check if an Edge Exists");
        System.out.println("7. Show All Vertices");
        System.out.println("8. Show Outbound Edges of a Vertex");
        System.out.println("9. Show Inbound Edges of a Vertex");
        System.out.println("10. Save Graph to File");
        System.out.println("11. Load Graph from File");
        System.out.println("12. Generate Random Graph");
        System.out.println("13. Exit");
    }

    public void handleMenuOption(int option) {
        Scanner scanner = new Scanner(System.in);
        switch (option) {
            case 1:
                showGraph();
                break;
            case 2:
                System.out.print("Enter vertex to add: ");
                int vertexToAdd = scanner.nextInt();
                if (graph.addVertex(vertexToAdd)) {
                    System.out.println("Vertex " + vertexToAdd + " added.");
                } else {
                    System.out.println("Vertex already exists.");
                }
                break;
            case 3:
                System.out.print("Enter vertex to remove: ");
                int vertexToRemove = scanner.nextInt();
                if (graph.removeVertex(vertexToRemove)) {
                    System.out.println("Vertex " + vertexToRemove + " removed.");
                } else {
                    System.out.println("Vertex does not exist.");
                }
                break;
            case 4:
                System.out.print("Enter source vertex: ");
                int src = scanner.nextInt();
                System.out.print("Enter target vertex: ");
                int tgt = scanner.nextInt();
                System.out.print("Enter weight: ");
                int weight = scanner.nextInt();
                if (graph.addEdge(src, tgt, weight)) {
                    System.out.println("Edge " + src + " -> " + tgt + " with weight " + weight + " added.");
                } else {
                    System.out.println("Edge already exists.");
                }
                break;
            case 5:
                System.out.print("Enter source vertex: ");
                int source = scanner.nextInt();
                System.out.print("Enter target vertex: ");
                int target = scanner.nextInt();
                if (graph.removeEdge(source, target)) {
                    System.out.println("Edge " + source + " -> " + target + " removed.");
                } else {
                    System.out.println("Edge does not exist.");
                }
                break;
            case 6:
                System.out.print("Enter source vertex: ");
                int sourceCheck = scanner.nextInt();
                System.out.print("Enter target vertex: ");
                int targetCheck = scanner.nextInt();
                if (graph.isEdge(sourceCheck, targetCheck)) {
                    System.out.println("Edge exists.");
                } else {
                    System.out.println("Edge does not exist.");
                }
                break;
            case 7:
                showVertices();
                break;
            case 8:
                System.out.print("Enter vertex to show outbound edges: ");
                int vertexOut = scanner.nextInt();
                showOutboundEdges(vertexOut);
                break;
            case 9:
                System.out.print("Enter vertex to show inbound edges: ");
                int vertexIn = scanner.nextInt();
                showInboundEdges(vertexIn);
                break;
            case 10:
                saveGraphToFileUI();
                break;
            case 11:
                loadGraphFromFileUI();
                break;
            case 12:
                System.out.print("Enter number of vertices: ");
                int vertices = scanner.nextInt();
                System.out.print("Enter number of edges: ");
                int edges = scanner.nextInt();
                graph.generateRandomGraph(vertices, edges);
                System.out.println("Random graph generated.");
                break;
            case 13:
                System.out.println("Exiting...");
                System.exit(0);
                break;
            default:
                System.out.println("Invalid option. Please try again.");
        }
    }

    public void showGraph() {
        System.out.println("\nGraph:");
        System.out.println("Vertices: " + graph.getVertices());
        for (Graph.Edge edge : graph.edges.values()) {
            System.out.println("Edge " + edge.getSource() + " -> " + edge.getTarget() + " (Weight: " + edge.getWeight() + ")");
        }
    }

    public void showVertices() {
        System.out.println("\nVertices: " + graph.getVertices());
    }

    public void showOutboundEdges(int vertex) {
        List<Graph.Edge> edges = graph.getOutboundEdges(vertex);
        if (edges.isEmpty()) {
            System.out.println("No outbound edges for vertex " + vertex);
        } else {
            System.out.println("Outbound edges for vertex " + vertex + ":");
            for (Graph.Edge edge : edges) {
                System.out.println("Target: " + edge.getTarget() + ", Weight: " + edge.getWeight());
            }
        }
    }

    public void showInboundEdges(int vertex) {
        System.out.println("Inbound edges for vertex " + vertex + ":");
        boolean found = false;
        for (Graph.Edge edge : graph.edges.values()) {
            if (edge.getTarget() == vertex) {
                System.out.println("Source: " + edge.getSource() + ", Edge ID: " + edge.getSource() + "->" + edge.getTarget());
                found = true;
            }
        }
        if (!found) {
            System.out.println("No inbound edges for vertex " + vertex);
        }
    }

    public void run() {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            displayMenu();
            System.out.print("Enter option: ");
            int option = scanner.nextInt();
            handleMenuOption(option);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Graph graph = new Graph(5);  // Create a graph with 5 vertices
        GraphUI ui = new GraphUI(graph);
        ui.run();
    }
}
