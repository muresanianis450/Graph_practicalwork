from graph import Graph
from greedy_vertex_cover import greedy_vertex_cover
from primal_dual_dual_approximation import *
from local_search_heuristic import *
from vertex_cover_maximal_matching import vertex_cover_maximal_matching
from vertex_cover_lp_relaxation import vertex_cover_lp_relaxation

def run_algorithm(name, func):
    files = ["graph.txt", "graph10.txt", "graph25.txt"]
    print(f"\n=== Running {name} ===")
    for file in files:
        print(f"\n📂 File: {file}")
        graph = Graph(file)
        cover = func(graph)
        print(f"✅ Vertex Cover: {sorted(cover)}")
        print(f"🔢 Size: {len(cover)}")
        print(f"📌 Vertices: {graph.get_number_vertices()}, 📎 Edges: {graph.edge_count}")
        print("-" * 50)
    print("=" * 60)

def main():
    while True:
        print("\nChoose Vertex Cover Algorithm:")
        print("1. Greedy 2-Approximation")
        print("2. Maximal Matching 2-Approximation")
        print("3. LP Relaxation (SciPy)")
        print("4. Primal-Dual 2-Approximation")
        print("5. Local Search Heuristic")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            run_algorithm("Greedy 2-Approximation", greedy_vertex_cover)
        elif choice == '2':
            run_algorithm("Maximal Matching 2-Approximation", vertex_cover_maximal_matching)
        elif choice == '3':
            run_algorithm("LP Relaxation (SciPy)", vertex_cover_lp_relaxation)
        elif choice == '4':
            run_algorithm("Primal-Dual 2-Approximation", primal_dual_vertex_cover)
        elif choice == '5':
            run_algorithm("Local Search Heuristic", local_search_vertex_cover)
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("❌ Invalid input. Try again.")

if __name__ == "__main__":
    main()
