from dsa_visualizer.data_structures.ui.overview import DATA_STRUCTURES_HEADING, render_overview
from dsa_visualizer.ui.text_constants import BANNER, INPUT_PLACEHOLDER


def test_banner_string() -> None:
    expected = (
        "╺┳┓┏━┓┏━┓   ╻ ╻╻┏━┓╻ ╻┏━┓╻  ╻╺━┓┏━╸┏━┓   ┏━╸┏┓╻┏━╸╻┏┓╻┏━╸\n"
        " ┃┃┗━┓┣━┫   ┃┏┛┃┗━┓┃ ┃┣━┫┃  ┃┏━┛┣╸ ┣┳┛   ┣╸ ┃┗┫┃╺┓┃┃┗┫┣╸ \n"
        "╺┻┛┗━┛╹ ╹   ┗┛ ╹┗━┛┗━┛╹ ╹┗━╸╹┗━╸┗━╸╹┗╸   ┗━╸╹ ╹┗━┛╹╹ ╹┗━╸"
    )
    assert BANNER == expected


def test_overview_string() -> None:
    expected = (
        "│\n"
        "├──▶ Primitive                        │                       │ Worst-case Big(O) for basic operations\n"
        "│     ├──▶ Integer                    │ 10                    │ access O(1)\n"
        "│     ├──▶ Float                      │ 3.14                  │ access O(1)\n"
        "│     ├──▶ Boolean                    │ True                  │ access O(1)\n"
        "│     ├──▶ Character                  │ 'a'                   │ access O(1)\n"
        "│     └──▶ String                     │ \"hi\"                  │ index O(1) | search O(n) | insert O(n) | delete O(n)\n"
        "│\n"
        "└──▶ Non-Primitive\n"
        "      ├──▶ Linear Data Structures     │                       │ Worst-case Big(O) for access/search/insert/delete\n"
        "      │     ├──▶ Array                │ [10, 22, 7]           │ access O(1) | search O(n) | insert O(n) | delete O(n)\n"
        "      │     ├──▶ Linked List          │ 10 -> 22 -> 7 -> null │ access O(n) | search O(n) | insert O(n) | delete O(n)\n"
        "      │     ├──▶ Stack                │ [1, 2, 3] top=3       │ push O(1) | pop O(1) | peek O(1)\n"
        "      │     └──▶ Queue                │ [1, 2, 3] front=1     │ enqueue O(1) | dequeue O(1) | peek O(1)\n"
        "      │\n"
        "      └──▶ Non-Linear Data Structures │                       │ Worst-case Big(O) for search/insert/delete/traverse\n"
        "            ├──▶ Tree                 │ A(B,C)                │ traverse O(n) | search O(n)\n"
        "            ├──▶ Binary Search Tree   │ 5(3,7)                │ search O(n) | insert O(n) | delete O(n)\n"
        "            ├──▶ Heap                 │ [1, 3, 5]             │ insert O(log n) | delete O(log n) | peek O(1)\n"
        "            └──▶ Graph                │ A->B,C                │ traverse O(V+E) | search O(V+E)"
    )
    assert render_overview().plain == expected


def test_heading_string() -> None:
    assert DATA_STRUCTURES_HEADING == "Data Structures"




def test_input_placeholder_string() -> None:
    assert INPUT_PLACEHOLDER == "Type Python code here. Press {Enter} to run."
