import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.Stack;
import java.util.Queue;
import java.util.function.Function;

/**
 * Yu Fu, Ziming Li
 *
 * Extra Credit One included, change NUMBER_OF_PEGS to create Honoi Tower with different number of pegs.
 * 
 * The main purpose of this assignemnt is finding the shortest and retreive path of Honoi Tower.
 * DFS and BFS are implemented in the assignment, and BFS is used to retreive the shorrtest path.
 *
 * Solution to Assignment 5 in CSE 373, Autumn 2014
 * University of Washington.
 * This assignment requires Java 8 JDK
 *  
 * Starter code provided by Steve Tanimoto and Si J. Liu, Nov. 21, 2014.
 *
 */

public class ExploredGraph {
    public final int NUMBER_OF_PEGS = 3; // number of pegs in this game
    private Set<Vertex> Ve; // collection of explored vertices
    private Set<Edge> Ee; // collection of explored edges
    private int VeSize; // size of collection of explored vertices
    private int EeSize; // size of collection of explored edges
    private List<Operator> operators; // collection of operators.
    private HashMap<Vertex, LinkedList<Edge>> map; // map of successor vertex with its edges

    public ExploredGraph() { 
        initialize();
    }

    public void initialize() {
        Ve = new LinkedHashSet<Vertex>();
        Ee = new LinkedHashSet<Edge>();
        map = new HashMap<Vertex, LinkedList<Edge>>();
        VeSize = 0;
        EeSize = 0;
        setOperators();
    }

    // Initialize the field operators with n * (n-1) Operators, n is the number of pegs
    // (i, j) = {(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)}
    private void setOperators() {
        operators = new ArrayList<Operator>();
        for (int i = 0; i < NUMBER_OF_PEGS; i++) {
            for (int j = 0; j < NUMBER_OF_PEGS; j++) {
                if (i != j) {
                    operators.add(new Operator(i, j));
                }
            }
        }
    }

    // Return size of collection of explored vertices
    public int nvertices() {
        return VeSize;
    }

    // Return size of collection of explored edges
    public int nedges() {
        return EeSize;
    }

    // Reset all private fields and implement depth first search algorithm using recursion (implicitly using stack).
    public void dfs(Vertex vi, Vertex vj) {
        initialize(); // Reset private field
        Ve.add(vi); // Add the start vertex to the set of explored vertexes.
        map.put(vi, new LinkedList<Edge>()); // Add the start vertex to the map of vertexes and corresponding edges
        VeSize = 1; // Set the size of Vertex set to be 1
        try {
            dfsHelper(vi, vj); // Use recursion to implement DFS
        } catch (StackOverflowError|OutOfMemoryError e) {  // Catch running out of resources error
        }
    }
    
    // Recursive helper method to implement DFS.
    private void dfsHelper(Vertex vi, Vertex vj) {
        if (!vi.equals(vj)) {  // Compared two vertexes vi and vj
            for (Operator o : operators) { // For all possible neighbor vertexes
                if ((boolean)o.getPrecondition().apply(vi)) { // Test the precondition of operator if vertexes not equal
                    Vertex vNext = (Vertex)o.getTransition().apply(vi);  // Create another vertex equal to the result of transition if the operator's transition function is applicable
                    // If the neighbor vertex is not already explored, or the result has not been found, continue the search.
                    if (!Ve.contains(vNext) && !Ve.contains(vj)) {
                        Ve.add(vNext); // Add the new vertex to set of explored vertex
                        VeSize++; // Increase the size of set of explored vertex by 1
                        map.put(vNext, new LinkedList<Edge>()); // Add the vertex to the map of vertexes and corresponding edges
                        Edge eNext = new Edge(vi, vNext); // Create a edge between vi and vNext
                        Ee.add(eNext); // Add the new edge to the set of explored edge
                        EeSize++; // Increase the size of the set of explorede edges by 1
                        map.get(vNext).add(eNext); // Add the edge to the map of vertexes and corresponding edges
                        dfsHelper(vNext, vj); // using recursion until reaching vj
                    }
                }
            }           
        }
    }

    // Reset all private fields and implement breath first search algorithm using queue.
    public void bfs(Vertex vi, Vertex vj) {
        initialize(); // Reset all private fields.
        Queue<Vertex> bfsQueue = new LinkedList<Vertex>(); // Use queue to implement BFS.
        bfsQueue.add(vi); // Add the start vertex to BFS queue.
        Ve.add(vi); // Add the start vertex to the set of explored vertexes.
        map.put(vi, new LinkedList<Edge>()); // Add the start vertex to the map of vertexes and corresponding edges.
        VeSize = 1; // Set the size of Vertex set to be 1.
        
        // If two given vertexes are not the same
        if (!vi.equals(vj)) {
            // Search when the queue is not empty.
            // If the goal is not found when the queue is empty,
            // There does not exists a path from the start vertex to the goal vertex.
            while (!bfsQueue.isEmpty()) {
                
                Vertex vNext = bfsQueue.remove(); // Dequeue a vertex from bfs queue.
                // Apply all the operators to the vertex to find the adjacent vertexes.
                for (Operator o : operators) {
                    // If the operator can be applied to the vertex (fit the precondition),
                    if ((boolean)o.getPrecondition().apply(vNext)) {
                        // Apply the operator to get adjacent vertex.
                        Vertex vNextAdjacent = (Vertex)o.getTransition().apply(vNext);
                        // If the adjacent vertex is not already explored,
                        if (!Ve.contains(vNextAdjacent)) {
                            Ve.add(vNextAdjacent); // Add adjacent vertex to the set of explored vertexes.
                            VeSize++; // Update size of vertex set.
                            
                            // Create an edge between dequeued vertex and its adjacent vertex.
                            Edge eNextAdjacent = new Edge(vNext, vNextAdjacent); 
                            Ee.add(eNextAdjacent); // Add edge to edges set.
                            EeSize++; // Update the size of edges set.
                            
                            map.put(vNextAdjacent, new LinkedList<Edge>()); // Put adjacent vertex in map.
                            map.get(vNextAdjacent).add(eNextAdjacent); // Put edge in the map.
                            
                            bfsQueue.add(vNextAdjacent); // Add adjacent vertex in BFS queue
                            
                            // When the goal is found, quit BFS search.
                            if (vNextAdjacent.equals(vj)) {
                                bfsQueue.clear();
                            }
                        }
                    }
                }
            }
        }
    }

    // Return an arraylist storing the path to given Vertex.
    public ArrayList<Vertex> retrievePath(Vertex vj) {
        ArrayList<Vertex> path = new ArrayList<Vertex>(); // Create a new arraylist of vertex
        path.add(vj); // Add vj into this arraylist
        if (map.get(vj).size() != 0) {  // If there is an edge connected to vj
            Vertex previousVertex = map.get(vj).get(0).vi; // Get the Vertex connected to vj
            // Keep searching the path while there is a connection
            while(map.get(previousVertex).size() != 0) {  
                Edge previousEdge = map.get(previousVertex).get(0); // Get previous edge
                path.add(previousVertex);  // Get previous vertex and add it to the path
                previousVertex = previousEdge.vi; // Set pointer to previous vertex.
            }
            path.add(previousVertex); // Add the last vertex into the path
            Collections.reverse(path); // Reserve the order of elements in path 
        }
        return path;  // Return the path
    }

    // Return the shorrtest path from given start Vertex and given goal Vertex.
    // Using BFS.
    public ArrayList<Vertex> shortestPath(Vertex vi, Vertex vj) {
        bfs(vi, vj); // Using bfs with vi, vj for the shortest path
        if (!Ve.contains(vj)) {  // if the set of explored vertex does not contain vj
            System.out.println("No path is found."); // print out no path
            return null;
        } else {
            ArrayList<Vertex> path = retrievePath(vj); // Else use retrievePath to find the path to vj.
            return path; // return the path
        }
    }

    // Return the set of explorede Vertices.
    public Set<Vertex> getVertices() {
        return Ve;
    }

    // Return the set of explored Edges.
    public Set<Edge> getEdges() {
        return Ee;
    }

    public static void main(String[] args) {
        ExploredGraph eg = new ExploredGraph();
        // Test the vertex constructor:
        Vertex v0 = eg.new Vertex("[[4,3,2,1],[],[]]");
        System.out.println(v0);
  
        Vertex vf = eg.new Vertex("[[],[],[4,3,2,1]]");

        ArrayList<Vertex> sp = eg.shortestPath(v0, vf);
        
        if (sp != null) {
            System.out.println("The path is:");
            for (Vertex x: sp) {
                System.out.println(x);
            }
            System.out.println("The length of path is: " + (sp.size() - 1));
        }
        System.out.println(eg.VeSize);
        // System.out.println(eg.VeSize);
        // System.out.println(eg.Ve.size());
        // System.out.println("BFS Trace:");
        // System.out.println(eg.Ve);
        // System.out.println("BFS path length: " + eg.nedges());
    }

    class Vertex {
        Stack<Integer>[] pegs; // Each vertex will hold a Towers-of-Hanoi state.
        int hash; // Stores the hashCode of Vertex

        // There will be 3 pegs in the standard version, but more if you do
        // extra credit option A5E1.
        
        // Constructor that takes a string such as "[[4,3,2,1],[],[]]":
        @SuppressWarnings("unchecked")
        public Vertex(String vString) {
            hash = -1;
            String[] parts = vString.split("\\],\\[");
            pegs = new Stack[NUMBER_OF_PEGS];
            for (int i = 0; i < NUMBER_OF_PEGS; i++) {
                pegs[i] = new Stack<Integer>();
                try {
                    parts[i] = parts[i].replaceAll("\\[", "");
                    parts[i] = parts[i].replaceAll("\\]", "");
                    ArrayList<String> al = new ArrayList<String>(
                            Arrays.asList(parts[i].split(",")));
                    // System.out.println("ArrayList al is: " + al);
                    Iterator<String> it = al.iterator();
                    while (it.hasNext()) {
                        Object item = it.next();
                        // System.out.println("item is: " + item);
                        Integer diskInteger = new Integer((String) item);
                        pegs[i].push(diskInteger);
                    }
                } catch (Exception e) {
                }
            }
        }

        public String toString() {
            String ans = "[";
            for (int i = 0; i < NUMBER_OF_PEGS; i++) {
                ans += pegs[i].toString().replace(" ", "");
                if (i < NUMBER_OF_PEGS - 1) {
                    ans += ",";
                }
            }
            ans += "]";
         
            if (hash == -1) {
                hash = ans.hashCode();
            }
        
            return ans;
        }

        // Implement equals method by using hashCode
        @Override
        public boolean equals(Object v) {
            if (this == v) {
                return true;
            }
            if (v == null) {
                return false;
            }
            if (getClass() != v.getClass()) {
                return false;
            }
            Vertex otherVertex = (Vertex) v;
            return this.hashCode() == otherVertex.hashCode();
        }

        // Use the hashCode by toString() to avoid duplicated hashCode of different Vertex.
        @Override
        public int hashCode() {
            if (hash == -1) {
                this.toString();
            }
            return hash;
        }
    }

    class Edge {
        public Vertex vi;
        public Vertex vj;

        public Edge(Vertex vi, Vertex vj) {
            this.vi = vi;
            this.vj = vj;
        }

        public String toString() {
            return vi.toString() + " -> " + vj.toString();
        }

        // Implement equals method by using hashCode
        @Override
        public boolean equals(Object e) {
            if (this == e) {
                return true;
            }
            if (e == null) {
                return false;
            }
            if (getClass() != e.getClass()) {
                return false;
            }
            Edge otherEdge = (Edge) e;
            return this.hashCode() == otherEdge.hashCode();
        }

        // Use the hashCode by toString() to avoid duplicated hashCode of different edges.
        @Override
        public int hashCode() {
            return this.toString().hashCode();
        }
    }

    class Operator {
        private int i, j;

        public Operator(int i, int j) {
            this.i = i;
            this.j = j;
        }

        // Additional explanation of what to do here will be given in GoPost or
        // as extra text in the spec.
        @SuppressWarnings("rawtypes")
        Function getPrecondition() {
            // Return a function that can be applied to a vertex to get whether
            // the operator's transition function can be applied to the vertex.
            // Returns true iff it is permissible to apply this operator's 
            // transition function to the vertex.
            return new Function() {
                // Return true iff peg i is not empty,
                // and the top disk in peg i has a smaller diameter
                // than the top disk in peg j.
                @Override
                public Object apply(Object vertex) {
                    if (vertex instanceof Vertex) {
                        Vertex v = (Vertex) vertex;
                        Stack<Integer> pegi = v.pegs[i];
                        Stack<Integer> pegj = v.pegs[j];
                        if (!pegi.isEmpty()) {
                            if (!pegj.isEmpty()) {
                                return pegi.peek() < pegj.peek();
                            } else {
                                return true;
                            }
                        }
                    }
                    return false;
                }
            };
        }

        @SuppressWarnings("rawtypes")
        Function getTransition() {
            // Return a function that can be applied to a vertex
            // (provided that the precondition is true) to get a "successor"
            // vertex -- the result of making the move.
            return new Function() {
                // Move the top disk of peg i to the top of peg j.
                // Return the result vertex.
                @Override
                public Object apply(Object vertex) {
                    if (vertex instanceof Vertex) {
                        Vertex v = (Vertex) vertex;
                        Vertex newVertex = new Vertex(v.toString());
                        Stack<Integer>[] newVertexPegs = newVertex.pegs;
                        Stack<Integer> pegi = newVertexPegs[i];
                        Stack<Integer> pegj = newVertexPegs[j];
                        pegj.push(pegi.pop());
                        return newVertex;
                    }
                    return null;
                }
            };
        }

        // Return a string good enough to distinguish different operators
        public String toString() {
            return "Try to move a disk from peg " + i + " to peg " + j + ".";
        }
    }
}
