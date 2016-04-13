import edu.princeton.cs.algs4.MinPQ;
import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.StdOut;

public class Solver {
   private Node result;

   private class Node implements Comparable<Node> {
      private final Board current;
      private final Node previous;
      private final int ma;
      private final int steps;
      private final int priority;

      private Node(Node p, Board c) {
         previous = p;
         current = c;
         ma = c.manhattan();
         if (previous == null) {
            steps = 0;
         } else {
            steps = previous.steps + 1;
         }
         priority = ma + steps;
      }

      public int compareTo(Node that) {
         return this.priority - that.priority;
      }
      
      public String toString() {
         StringBuilder s = new StringBuilder();
         s.append("priority  =" + priority + "\n");
         s.append("moves     =" + steps + "\n");
         s.append("manhattan =" + ma + "\n");
         s.append(current.toString());
         s.append("\n");
         return s.toString();
      }
   }
   
   // find a solution to the initial board (using the A* algorithm)
   public Solver(Board initial) {
      if (initial.isGoal()) {
         result = new Node(null, initial);
      } else {
         result = solve(initial, initial.twin());
      }
   }

   private Node solve(Board b, Board bTwin) {
      MinPQ<Node> pq = new MinPQ<Node>();
      MinPQ<Node> twinpq = new MinPQ<Node>();
      pq.insert(new Node(null, b));
      twinpq.insert(new Node(null, bTwin));
      while (true) {
         Node last = pq.delMin();
         for (Board n : last.current.neighbors()) {
            if (last.previous == null || !n.equals(last.previous.current)) {
               pq.insert(new Node(last, n));
            }
         }
         if (last.current.isGoal()) {
            return last;
         }

         Node lastTwin = twinpq.delMin();
         for (Board n : lastTwin.current.neighbors()) {
            if (lastTwin.previous == null || !n.equals(lastTwin.previous.current)) {
               twinpq.insert(new Node(lastTwin, n));
            }
         }
         if (lastTwin.current.isGoal()) {
            return null;
         }
      }
   }
   
   // is the initial board solvable?
   public boolean isSolvable() {
      return result != null;
   }

   // min number of moves to solve initial board; -1 if no solution
   public int moves() {
      if (result != null) {
         return result.steps;
      }
      return -1;
   }

   // sequence of boards in a shortest solution; null if no solution
   public Iterable<Board> solution() {
      if (result == null) {
         return null;
      }
      Stack<Board> s = new Stack<Board>();
      for (Node n = result; n != null; n = n.previous) {
         s.push(n.current);
      }
      return s;
   }

   // solve a slider puzzle (given below)
   public static void main(String[] args) {
      // create initial board from file
      long startTime = System.currentTimeMillis();
      In in = new In(args[0]);
      int N = in.readInt();
      int[][] blocks = new int[N][N];
      for (int i = 0; i < N; i++) {
         for (int j = 0; j < N; j++) {
            blocks[i][j] = in.readInt();
         }
      }
      Board initial = new Board(blocks);
      // solve the puzzle
      Solver solver = new Solver(initial);
      // print solution to standard output
      if (!solver.isSolvable()) {
         StdOut.println("No solution possible");
      } else {
         StdOut.println("Minimum number of moves = " + solver.moves());
         for (Board board : solver.solution()) {
            StdOut.println(board);
         }
      }
      long endTime = System.currentTimeMillis();
      System.out.println("That took " + (endTime - startTime) + " milliseconds");
   }
}