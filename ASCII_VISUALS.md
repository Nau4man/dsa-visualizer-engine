# ASCII Visualizations

## Data Structures Overview
```
│
├──▶ Primitive                        │                       │ Worst-case Big(O) for basic operations
│     ├──▶ Integer                    │ 10                    │ access O(1)
│     ├──▶ Float                      │ 3.14                  │ access O(1)
│     ├──▶ Boolean                    │ True                  │ access O(1)
│     ├──▶ Character                  │ 'a'                   │ access O(1)
│     └──▶ String                     │ "hi"                  │ index O(1) | search O(n) | insert O(n) | delete O(n)
│
└──▶ Non-Primitive
      ├──▶ Linear Data Structures     │                       │ Worst-case Big(O) for access/search/insert/delete
      │     ├──▶ Array                │ [10, 22, 7]           │ access O(1) | search O(n) | insert O(n) | delete O(n)
      │     ├──▶ Linked List          │ 10 -> 22 -> 7 -> null │ access O(n) | search O(n) | insert O(n) | delete O(n)
      │     ├──▶ Stack                │ [1, 2, 3] top=3       │ push O(1) | pop O(1) | peek O(1)
      │     └──▶ Queue                │ [1, 2, 3] front=1     │ enqueue O(1) | dequeue O(1) | peek O(1)
      │
      └──▶ Non-Linear Data Structures │                       │ Worst-case Big(O) for search/insert/delete/traverse
            ├──▶ Tree                 │ A(B,C)                │ traverse O(n) | search O(n)
            ├──▶ Binary Search Tree   │ 5(3,7)                │ search O(n) | insert O(n) | delete O(n)
            ├──▶ Heap                 │ [1, 3, 5]             │ insert O(log n) | delete O(log n) | peek O(1)
            └──▶ Graph                │ A->B,C                │ traverse O(V+E) | search O(V+E)
```

## Full annotated primitive value cell Visualization
```
Address: 0x1004

┌────────────────────────┐
│ type: int32            │
├────────────────────────┤
│ size: 4 bytes          │
├────────────────────────┤
│ bits: 00000000 00101010│
├────────────────────────┤
│ value: 42              │
└────────────────────────┘

```

## Pointer cell Visualization
```
Address: 0x2000

┌────────────────────────┐
│ type: pointer          │
├────────────────────────┤
│ size: 8 bytes          │
├────────────────────────┤
│ bits: 00000000 00010000│
├────────────────────────┤
│ points to: 0x1004      │
└────────────────────────┘

0x2000 ──▶ 0x1004

```
## Floating Point (float, double) Visalization

```
Address: 0x1010

┌────────────────────────────────┐
│ type: float32                  │
├────────────────────────────────┤
│ size: 4 bytes                  │
├────────────────────────────────┤
│ sign | exponent | mantissa     │
│   0  | 10000000 | 100100100... │
├────────────────────────────────┤
│ value: 3.1415927               │
└────────────────────────────────┘

```

## Char Visalization

```

Address: 0x1020

┌────────────────────────┐
│ type: char (ASCII)     │
├────────────────────────┤
│ size: 1 byte           │
├────────────────────────┤
│ bits: 01000001         │
├────────────────────────┤
│ value: 'A' (65)        │
└────────────────────────┘


```

## Boolean Visalization

```
Address: 0x1030

┌────────────────────────┐
│ type: bool             │
├────────────────────────┤
│ size: 1 byte           │
├────────────────────────┤
│ bits: 00000001         │
├────────────────────────┤
│ value: true            │
└────────────────────────┘



```


## NULL Visalization

```
┌────────────────────────┐
│ type: NULL             │
├────────────────────────┤
│ size: 0 bytes (logic)  │
├────────────────────────┤
│ meaning: no object     │
└────────────────────────┘



```


## Array (Contiguous, Indexed) Visalization

```
        ┌────┬────┬────┬────┬────┐
Index → │ 0  │ 1  │ 2  │ 3  │ 4  │
        ├────┼────┼────┼────┼────┤
Array → │ A  │ B  │ C  │ D  │ E  │
        └────┴────┴────┴────┴────┘



```


## Singly Linked List Visalization

```
Head ──▶ ┌────┬─────┐ ──▶ ┌────┬─────┐ ──▶ ┌────┬─────┐
         │ A  │  •  │     │ B  │  •  │     │ C  │ NULL│
         └────┴─────┘     └────┴─────┘     └────┴─────┘

  Node Structure       
┌────────┬────────┐
│  data  │  next  │
└────────┴────────┘
    A      0x1004


```## Doubly Linked List Visalization

```
Head ──▶ ┌─────┬────┬─────┐ ⇄ ┌─────┬────┬─────┐ ⇄ ┌─────┬────┬─────┐
         │NULL │ A  │  •  │   │  •  │ B  │  •  │   │  •  │ C  │NULL │
         └─────┴────┴─────┘   └─────┴────┴─────┘   └─────┴────┴─────┘

Node Structure
┌────────┬────────┬────────┐
│  prev  │  data  │  next  │
└────────┴────────┴────────┘
   NULL      A      0x1004


```


## Stack (LIFO) Visalization

```
Top
 │
 ▼
┌─────┐
│  D  │
├─────┤
│  C  │
├─────┤
│  B  │
├─────┤
│  A  │
└─────┘



```


## Queue (FIFO) Visalization

```
Front ──▶ ┌─────┬─────┬─────┬─────┐ ──▶ Rear
          │  A  │  B  │  C  │  D  │
          └─────┴─────┴─────┴─────┘


```


## Hash Table (Separate Chaining) Visalization

```
Index
 0 ──▶ NULL
 1 ──▶ NULL
 2 ──▶ ┌────┬─────┐ ──▶ ┌────┬─────┐ ──▶ ┌────┬─────┐ ──▶ NULL
       │ 12 │  A  │     │ 22 │  B  │     │  7 │  C  │
       └────┴─────┘     └────┴─────┘     └────┴─────┘

 3 ──▶ NULL
 4 ──▶ ┌────┬─────┐ ──▶ NULL
       │ 14 │  D  │
       └────┴─────┘

Node Structure
┌────────┬────────┬────────┐
│  key   │ value  │  next  │
└────────┴────────┴────────┘
    A        12      NULL



```


## Binary Tree Visalization

```
            [A]
             ▼
      ┌─────────────┐
      ▼             ▼
     [B]           [C]
      ▼
   ┌───────┐
   ▼       ▼
  [D]     [E]

```

## Binary Search Tree (BST) Visalization

```
            [8]
             ▼
      ┌─────────────┐
      ▼             ▼
     [3]           [10]
      ▼
   ┌───────┐
   ▼       ▼
  [1]     [6]

Left < Node < Right


```
## Heap (Min Heap) Visalization

```

            [1]
             ▼
      ┌─────────────┐
      ▼             ▼
     [3]           [5]
      ▼
   ┌───────┐
   ▼       ▼
  [7]     [9]

Array view:
  
Index ──▶  0  1  2  3  4
          ┌──┬──┬──┬──┬──┐
Heap  ──▶ │1 │3 │5 │7 │9 │
          └──┴──┴──┴──┴──┘



```
## Undirected Graph Visalization

```
[A] ── [B]
 │      │
 │      │
[C] ── [D]

Edges: AB, AC, AD, BD, CD



Adjacency list:

A ──▶ B, C, D
B ──▶ A, D
C ──▶ A, D
D ──▶ A, B, C


```
## Directed Graph Visalization

```
A ──▶ B ──▶ C
▲       │
│       ▼
└────── D

[A] ── [B]
 │      │
 │      │
[C] ── [D]




```
