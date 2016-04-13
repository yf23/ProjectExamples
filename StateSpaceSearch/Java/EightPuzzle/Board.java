import edu.princeton.cs.algs4.Queue;
import edu.princeton.cs.algs4.StdOut;

public class Board {
   private char[][] tiles;
   private int ma;
   private int size;
   
   // construct a board from an N-by-N array of blocks
   // (where blocks[i][j] = block in row i, column j)
   public Board(int[][] blocks) {
      ma = -1;
      size = blocks.length;
      tiles = intArrayToCharArray(blocks, size);
   }

   // board dimension N
   public int dimension() {
      return size;
   }

   // number of blocks out of place
   public int hamming() {
      int ha = 0;
      for (int i = 0; i < size; i++) {
         for (int j = 0; j < size; j++) {
            int number = (int) tiles[i][j];
            if (number != 0) {
               int supposeX = (number - 1) / size;
               int supposeY = (number - 1) % size;
               if (i != supposeX || j != supposeY) {
                  ha++;
               }
            }
         }
      }
      return ha;
   }

   // sum of Manhattan distances between blocks and goal
   public int manhattan() {
      if (ma == -1) {
         ma = 0;
         for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
               int number = (int) tiles[i][j];
               if (number != 0) {
                  int supposeX = (number - 1) / size;
                  int supposeY = (number - 1) % size;
                  ma += (Math.abs(i - supposeX)) + (Math.abs(j - supposeY));
               }
            }
         }     
      }
      return ma;
   }

   // is this board the goal board?
   public boolean isGoal() {
      return manhattan() == 0;
   }

   // a board obtained by exchanging two adjacent blocks in the same row
   public Board twin() {
      int[][] twinTiles = charArrayToIntArray(tiles, size);
      if (twinTiles[0][0] != 0 && twinTiles[0][1] != 0) {
         exc(twinTiles, 0, 0, 0, 1);
      } else {
         exc(twinTiles, 1, 0, 1, 1);
      }
      return new Board(twinTiles);
   }

   // does this board equal y?
   public boolean equals(Object y) {
      if (this == y) {
         return true;
      }
      if (y == null) {
         return false;
      }
      if (this.getClass() != y.getClass()) {
         return false;
      }
      Board that = (Board) y;
      if (this.size != that.size) {
         return false;
      }
      for (int i = 0; i < this.size; i++) {
         for (int j = 0; j < this.size; j++) {
            if (this.tiles[i][j] != that.tiles[i][j]) {
               return false;
            }
         }
      }
      return true;
   }

   // all neighboring boards
   public Iterable<Board> neighbors() {
      Queue<Board> ne = new Queue<Board>();
      int zeroX = -1;
      int zeroY = -1;
      findZero:
      for (int i = 0; i < size; i++) {
         for (int j = 0; j < size; j++) {
            if (tiles[i][j] == (char) 0) {
               zeroX = i;
               zeroY = j;
               break findZero;
            }
         }
      }
      int[][] copyOfTiles = charArrayToIntArray(tiles, size);
      if (zeroX != 0) {
         exc(copyOfTiles, zeroX, zeroY, zeroX - 1, zeroY);
         ne.enqueue(new Board(copyOfTiles));
         exc(copyOfTiles, zeroX, zeroY, zeroX - 1, zeroY);
      }
      if (zeroX != size - 1) {
         exc(copyOfTiles, zeroX, zeroY, zeroX + 1, zeroY);
         ne.enqueue(new Board(copyOfTiles));
         exc(copyOfTiles, zeroX, zeroY, zeroX + 1, zeroY);
      }
      if (zeroY != 0) {
         exc(copyOfTiles, zeroX, zeroY, zeroX, zeroY - 1);
         ne.enqueue(new Board(copyOfTiles));
         exc(copyOfTiles, zeroX, zeroY, zeroX, zeroY - 1);
      }
      if (zeroY != size - 1) {
         exc(copyOfTiles, zeroX, zeroY, zeroX, zeroY + 1);
         ne.enqueue(new Board(copyOfTiles));
         exc(copyOfTiles, zeroX, zeroY, zeroX, zeroY + 1);
      }
      return ne;
   }

   // string representation of the board (in the output format specified below)
   public String toString() {
      StringBuilder s = new StringBuilder();
      s.append(size + "\n");
      for (int i = 0; i < size; i++) {
         for (int j = 0; j < size; j++) {
            s.append(String.format("%2d ", (int) tiles[i][j]));
         }
         s.append("\n");
      }
      return s.toString();
   }

   private void exc(int[][] c, int x1, int y1, int x2, int y2) {
      int a = c[x1][y1];
      c[x1][y1] = c[x2][y2];
      c[x2][y2] = a;
   }

   private char[][] intArrayToCharArray(int[][] a, int N) {
      char[][] b = new char[N][N];
      for (int i = 0; i < N; i++) {
         for (int j = 0; j < N; j++) {
            b[i][j] = (char) a[i][j];
         }
      }
      return b;
   }

   private int[][] charArrayToIntArray(char[][] a, int N) {
      int[][] b = new int[N][N];
      for (int i = 0; i < N; i++) {
         for (int j = 0; j < N; j++) {
            b[i][j] = (int) a[i][j];
         }
      }
      return b;
   }

  /* 
   public static void main(String[] args) {
      int[][] testIn = {{1, 2, 3}, {4, 5, 6}, {7, 8, 0}};
      Board test = new Board(testIn);
      StdOut.println(test.toString());
      StdOut.println(test.dimension());
      StdOut.println(test.hamming());
      StdOut.println(test.manhattan());
      StdOut.println(test.isGoal());
      StdOut.println(test.twin().toString());
      Iterable<Board> neigh = test.neighbors();
      for (Board b : neigh) {
         StdOut.print(b);
      }
   }
   */
   
}