using System;
using System.Collections.Generic;
using System.IO;

public class Graph
{
    private Dictionary<int, List<Tuple<int, int>>> outNeighbours; // Adjacency list (with weights)
    private Dictionary<int, Tuple<int, int, int>> edges;  // Edge ID -> (source, target, weight)
    private int edgeCount;

    public Graph(string filename = "")
    {
        outNeighbours = new Dictionary<int, List<Tuple<int, int>>>();
        edges = new Dictionary<int, Tuple<int, int, int>>();
        edgeCount = 0;

        if (!string.IsNullOrEmpty(filename))
        {
            ReadFromFile(filename);
        }
    }

    private void ReadFromFile(string filename)
    {
        try
        {
            using (StreamReader file = new StreamReader(filename))
            {
                string[] firstLine = file.ReadLine().Split(' ');
                int numVertices = int.Parse(firstLine[0]);
                int numEdges = int.Parse(firstLine[1]);

                for (int i = 0; i < numVertices; i++)
                {
                    outNeighbours[i] = new List<Tuple<int, int>>();
                }

                string line;
                while ((line = file.ReadLine()) != null)
                {
                    var parts = line.Split(' ');
                    int u = int.Parse(parts[0]);
                    int v = int.Parse(parts[1]);
                    int w = int.Parse(parts[2]);
                    AddEdge(u, v, w);
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine($"Error: Could not open file {filename}. {e.Message}");
        }
    }

    public bool AddEdge(int x, int y, int weight)
    {
        foreach (var neighbour in outNeighbours[x])
        {
            if (neighbour.Item1 == y && neighbour.Item2 == weight)
            {
                return false;
            }
        }

        outNeighbours[x].Add(new Tuple<int, int>(y, weight));
        edges[edgeCount] = new Tuple<int, int, int>(x, y, weight);
        edgeCount++;
        return true;
    }

    public bool RemoveEdge(int x, int y)
    {
        var neighbours = outNeighbours[x];
        var edge = neighbours.Find(neighbour => neighbour.Item1 == y);
        if (edge != null)
        {
            neighbours.Remove(edge);
            return true;
        }
        return false;
    }

    public bool RemoveVertex(int x)
    {
        if (outNeighbours.ContainsKey(x))
        {
            outNeighbours.Remove(x);
            return true;
        }
        return false;
    }

    public bool AddVertex(int x)
    {
        if (!outNeighbours.ContainsKey(x))
        {
            outNeighbours[x] = new List<Tuple<int, int>>();
            return true;
        }
        return false;
    }

    public Tuple<int, int, int> GetEdgeById(int edgeId)
    {
        if (edges.ContainsKey(edgeId))
        {
            return edges[edgeId];
        }
        return new Tuple<int, int, int>(-1, -1, -1);  // Return an invalid edge if not found
    }

    public List<Tuple<int, int>> ParseOut(int x)
    {
        return outNeighbours[x];
    }

    public int GetNumberVertices()
    {
        return outNeighbours.Count;
    }

    public List<int> ParseVertices()
    {
        return new List<int>(outNeighbours.Keys);
    }

    public bool IsEdge(int x, int y)
    {
        foreach (var edge in edges.Values)
        {
            if (edge.Item1 == x && edge.Item2 == y)
            {
                return true;
            }
        }
        return false;
    }

    public void GenerateRandomGraph(int numberVertices, int numberEdges)
    {
        Random rand = new Random();
        for (int i = 0; i < numberEdges; i++)
        {
            int x = rand.Next(numberVertices);
            int y = rand.Next(numberVertices);
            int weight = rand.Next(1, 101);  // Random weight between 1 and 100
            if (x != y && !IsEdge(x, y))
            {
                AddEdge(x, y, weight);
            }
        }
    }

    public int GetEdgeCount()
    {
        return edgeCount;
    }

    public static Graph ReadFromFile(string filename)
    {
        return new Graph(filename);
    }

    public static void WriteToFile(Graph graph, string filename)
    {
        using (StreamWriter file = new StreamWriter(filename))
        {
            file.WriteLine($"{graph.GetNumberVertices()} {graph.edges.Count}");
            for (int edgeId = 0; edgeId < graph.GetEdgeCount(); edgeId++)
            {
                var edge = graph.GetEdgeById(edgeId);
                file.WriteLine($"{edge.Item1} {edge.Item2} {edge.Item3}");
            }
        }
    }
}

public class GraphUI
{
    private Graph graph;

    public GraphUI(string filename = "graph.txt")
    {
        graph = new Graph(filename);
    }

    public void LoadGraphFromFileUI()
    {
        Console.Write("Enter file name to load the graph: ");
        string fileName = Console.ReadLine();
        graph = Graph.ReadFromFile(fileName);
        Console.WriteLine($"Graph loaded from {fileName}");
    }

    public void SaveGraphToFileUI()
    {
        Console.Write("Enter file name to save the graph: ");
        string fileName = Console.ReadLine();
        Graph.WriteToFile(graph, fileName);
        Console.WriteLine($"Graph saved to {fileName}");
    }

    public void ShowGraph()
    {
        Console.WriteLine("\nGraph:");
        Console.Write("Vertices: ");
        List<int> vertices = graph.ParseVertices();
        foreach (var vertex in vertices)
        {
            Console.Write($"{vertex} ");
        }
        Console.WriteLine();
        for (int edgeId = 0; edgeId < graph.GetEdgeCount(); edgeId++)
        {
            var edge = graph.GetEdgeById(edgeId);
            Console.WriteLine($"Edge {edgeId}: {edge.Item1} -> {edge.Item2} (Weight: {edge.Item3})");
        }
    }

    public void DisplayMenu()
    {
        Console.WriteLine("\nGraph Menu:");
        Console.WriteLine("1. Show Graph");
        Console.WriteLine("2. Add Vertex");
        Console.WriteLine("3. Remove Vertex");
        Console.WriteLine("4. Add Edge");
        Console.WriteLine("5. Remove Edge");
        Console.WriteLine("6. Check if an Edge Exists");
        Console.WriteLine("7. Show All Vertices");
        Console.WriteLine("8. Show Outbound Edges of a Vertex");
        Console.WriteLine("9. Save Graph to File");
        Console.WriteLine("10. Load Graph from File");
        Console.WriteLine("11. Generate Random Graph");
        Console.WriteLine("12. Exit");
    }

    public void HandleMenuOption(int option)
    {
        switch (option)
        {
            case 1: ShowGraph(); break;
            case 2: AddVertexUI(); break;
            case 3: RemoveVertexUI(); break;
            case 4: AddEdgeUI(); break;
            case 5: RemoveEdgeUI(); break;
            case 6: CheckEdgeUI(); break;
            case 7: ShowVertices(); break;
            case 8: ShowOutboundEdgesUI(); break;
            case 9: SaveGraphToFileUI(); break;
            case 10: LoadGraphFromFileUI(); break;
            case 11: GenerateRandomGraphUI(); break;
            case 12: Console.WriteLine("Exiting..."); Environment.Exit(0); break;
            default: Console.WriteLine("Invalid option. Please try again."); break;
        }
    }

    public void AddVertexUI()
    {
        Console.Write("Enter vertex to add: ");
        int vertex = int.Parse(Console.ReadLine());
        if (graph.AddVertex(vertex))
        {
            Console.WriteLine($"Vertex {vertex} added.");
        }
        else
        {
            Console.WriteLine("Vertex already exists.");
        }
    }

    public void RemoveVertexUI()
    {
        Console.Write("Enter vertex to remove: ");
        int vertex = int.Parse(Console.ReadLine());
        if (graph.RemoveVertex(vertex))
        {
            Console.WriteLine($"Vertex {vertex} removed.");
        }
        else
        {
            Console.WriteLine("Vertex does not exist.");
        }
    }

    public void AddEdgeUI()
    {
        Console.Write("Enter source vertex: ");
        int x = int.Parse(Console.ReadLine());
        Console.Write("Enter target vertex: ");
        int y = int.Parse(Console.ReadLine());
        Console.Write("Enter weight of the edge: ");
        int weight = int.Parse(Console.ReadLine());
        if (graph.AddEdge(x, y, weight))
        {
            Console.WriteLine($"Edge {x} -> {y} with weight {weight} added.");
        }
        else
        {
            Console.WriteLine($"Edge {x} -> {y} already exists.");
        }
    }

    public void RemoveEdgeUI()
    {
        Console.Write("Enter source vertex: ");
        int x = int.Parse(Console.ReadLine());
        Console.Write("Enter target vertex: ");
        int y = int.Parse(Console.ReadLine());
        if (graph.RemoveEdge(x, y))
        {
            Console.WriteLine($"Edge {x} -> {y} removed.");
        }
        else
        {
            Console.WriteLine("Edge does not exist.");
        }
    }

    public void CheckEdgeUI()
    {
        Console.Write("Enter source vertex: ");
        int x = int.Parse(Console.ReadLine());
        Console.Write("Enter target vertex: ");
        int y = int.Parse(Console.ReadLine());
        if (graph.IsEdge(x, y))
        {
            Console.WriteLine($"Edge {x} -> {y} exists.");
        }
        else
        {
            Console.WriteLine("Edge does not exist.");
        }
    }

    public void ShowVertices()
    {
        Console.Write("\nVertices: ");
        List<int> vertices = graph.ParseVertices();
        foreach (var vertex in vertices)
        {
            Console.Write($"{vertex} ");
        }
        Console.WriteLine();
    }

    public void ShowOutboundEdgesUI()
    {
        Console.Write("Enter vertex to show outbound edges: ");
        int vertex = int.Parse(Console.ReadLine());
        List<Tuple<int, int>> edges = graph.ParseOut(vertex);
        Console.WriteLine($"Outbound edges for vertex {vertex}:");
        foreach (var edge in edges)
        {
            Console.WriteLine($"Target: {edge.Item1}, Weight: {edge.Item2}");
        }
    }

    public void GenerateRandomGraphUI()
    {
        Console.Write("Enter number of vertices: ");
        int numberVertices = int.Parse(Console.ReadLine());
        Console.Write("Enter number of edges: ");
        int numberEdges = int.Parse(Console.ReadLine());
        graph.GenerateRandomGraph(numberVertices, numberEdges);
        Console.WriteLine($"Random graph generated with {numberVertices} vertices and {numberEdges} edges.");
    }

    public void Run()
    {
        while (true)
        {
            DisplayMenu();
            Console.Write("Enter option: ");
            int option = int.Parse(Console.ReadLine());
            HandleMenuOption(option);
        }
    }
}

public class Program
{
    public static void Main()
    {
        GraphUI ui = new GraphUI("graph.txt");
        ui.Run();
    }
}
