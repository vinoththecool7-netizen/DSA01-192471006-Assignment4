# Assignment 4 - CO4: Designing Reusable Class Hierarchies

**Name:** S Vinoth Kumar  
**Register number:** 192471006  
**Course:** Object Oriented Programming with C++ (DSA01)  
**Repository:** https://github.com/vinoththecool7-netizen/DSA01-192471006-Assignment4

## Compiler and reproduction

Apple Clang 21.0.0 (clang-2100.4.1.1), arm64-apple-darwin27.2.0, invoked using the installed `g++` alias. This is not GNU GCC. All sources use standard C++17; platform-dependent diagnostics and sizes can differ on another compiler. Full actual version: [compiler.txt](compiler.txt).

From the repository root:

```sh
python3 scripts/validate.py
python3 scripts/evidence_viewer.py
```

The runner creates `.build/`, compiles every listed program, runs it with the declared data, compares required outputs exactly, and writes stdout, stderr, source hashes, flags and exit statuses under each task's `evidence/` directory. Set `CXX` to select another C++ compiler. The two TODO programs are standalone `Task03/complete.cpp` and `Task05/complete.cpp`; surrounding behavior is preserved. Pasted comment line breaks were restored where needed.

Tasks 1-5 use embedded demonstration/test values and consume no input files. Task 6 actually consumes `Task06/input.txt` using stdin. No unused placeholder input files are included.

## Exact compile and run commands

The following are the actual commands recorded for this submission. Run them from the repository root after `mkdir -p .build`. The deliberate compile failure, initializer warning and unsafe account runs are labelled below; they are teaching experiments rather than successful ordinary tests.

```sh
g++ -std=c++17 -Wall -Wextra Task01/payroll.cpp -o .build/_Task01_payroll
.build/_Task01_payroll
```

```sh
g++ -std=c++17 -Wall -Wextra Task02/predict_virtual.cpp -o .build/_Task02_predict_virtual
.build/_Task02_predict_virtual
```

```sh
g++ -std=c++17 -Wall -Wextra Task02/predict_nonvirtual.cpp -o .build/_Task02_predict_nonvirtual
.build/_Task02_predict_nonvirtual
```

```sh
g++ -std=c++17 -Wall -Wextra Task02/relationships.cpp -o .build/_Task02_relationships
.build/_Task02_relationships
```

```sh
g++ -std=c++17 -Wall -Wextra Task03/predict.cpp -o .build/_Task03_predict
.build/_Task03_predict
```

```sh
g++ -std=c++17 -Wall -Wextra Task03/complete.cpp -o .build/_Task03_complete
.build/_Task03_complete
```

```sh
g++ -std=c++17 -Wall -Wextra Task03/hierarchy.cpp -o .build/_Task03_hierarchy
.build/_Task03_hierarchy
```

```sh
g++ -std=c++17 -Wall -Wextra Task03/address_pointer.cpp -o .build/_Task03_address_pointer
.build/_Task03_address_pointer
```

```sh
g++ -std=c++17 -Wall -Wextra Task04/predict.cpp -o .build/_Task04_predict
.build/_Task04_predict
```

```sh
g++ -std=c++17 -Wall -Wextra Task04/repaired.cpp -o .build/_Task04_repaired
.build/_Task04_repaired
```

```sh
g++ -std=c++17 -Wall -Wextra Task05/complete.cpp -o .build/_Task05_complete
.build/_Task05_complete
```

```sh
g++ -std=c++17 -Wall -Wextra Task05/cart_demo.cpp -o .build/_Task05_cart_demo
.build/_Task05_cart_demo
```

```sh
g++ -std=c++17 -Wall -Wextra Task06/tagged.cpp -o .build/_Task06_tagged
.build/_Task06_tagged
```

```sh
g++ -std=c++17 -Wall -Wextra Task06/fleet.cpp -o .build/_Task06_fleet
.build/_Task06_fleet < Task06/input.txt
```

```sh
g++ -std=c++17 -Wall -Wextra -DNONVIRTUAL Task03/hierarchy.cpp -o .build/_Task03_hierarchy_nonvirtual
.build/_Task03_hierarchy_nonvirtual
```

```sh
g++ -std=c++17 -Wall -Wextra -x c++ Task03/diagnostics/reordered.cpp.txt -o .build/Task03_diagnostics_reordered
.build/Task03_diagnostics_reordered
```

```sh
g++ -std=c++17 -Wall -Wextra -x c++ Task02/diagnostics/ambiguous.cpp.txt -o .build/Task02_diagnostics_ambiguous
```

```sh
g++ -std=c++17 -Wall -Wextra -fsanitize=address -g -fno-omit-frame-pointer Task04/broken.cpp -o .build/_Task04_broken_asan
.build/_Task04_broken_asan
```

```sh
g++ -std=c++17 -Wall -Wextra -fsanitize=address -g Task04/broken.cpp -o .build/_Task04_broken_leak_probe
ASAN_OPTIONS=detect_leaks=1 .build/_Task04_broken_leak_probe
```

```sh
g++ -std=c++17 -Wall -Wextra -fsanitize=address -g Task04/repaired.cpp -o .build/_Task04_repaired_asan
.build/_Task04_repaired_asan
```

```sh
g++ -std=c++17 -Wall -Wextra -fsanitize=address -g Task03/address_pointer.cpp -o .build/_Task03_address_pointer_asan
.build/_Task03_address_pointer_asan
```

## Task results and evidence

| Task | Implementation and result |
|---|---|
| [Task01](Task01/analysis.md) | Abstract payroll hierarchy and tagged alternative; independently checked 76000, 28400 and 16000; ABI sizes measured. |
| [Task02](Task02/analysis.md) | University roles, resolved diamond, access table, composition comparison; virtual/nonvirtual predictions match; ambiguous member fixture rejected as expected. |
| [Task03](Task03/analysis.md) | Initializer lists, Address/Course members, construction/destruction traces; TA size 192 virtual versus 264 nonvirtual; completed output matches; deep-copy Address tests pass. |
| [Task04](Task04/analysis.md) | Wrong static dispatch, nonvirtual deletion and slicing demonstrated; virtual/RAII repair passes ASan; local leak detector unavailable. |
| [Task05](Task05/analysis.md) | Four object access methods, this chaining, pointer-array maximum; required output 324.00; empty/null/capacity/discount checks pass. |
| [Task06](Task06/analysis.md) | Abstract fleet, rent/return/list and ElectricBus extension; five independently checked late bills and five expected errors. |

Each task contains actual logs, machine-readable execution metadata, an HTML output-record viewer and `output-screenshot.jpg`, a genuine browser capture of that viewer. These screenshots display captured program output and commands; they do not pretend to be terminal captures. Open the HTML files directly in a browser or serve this folder locally. For long screenshots, open at full resolution. Raw text logs remain the complete, searchable evidence.

## Expected diagnostics and sanitizer limits

- Task02/diagnostics/ambiguous.cpp.txt: compilation exits 1 because id belongs to two Person subobjects. Merely removing virtual from the supplied constructor-only example compiles successfully.
- Task03/diagnostics/reordered.cpp.txt: compilation succeeds with -Wreorder-ctor and still constructs bases/members in declaration order.
- Task04/broken.cpp: deliberately performs undefined deletion through a nonvirtual base. The observed ASan run exits 0 with no diagnostic; its destructor trace skips destruction of the heap SeniorAccount. Zero exit is not a claim of memory correctness.
- Task04 leak probe: `ASAN_OPTIONS=detect_leaks=1` is rejected by this Mac runtime, exits via signal (subprocess status -6), and reports that leak detection is unsupported. No local leak-detector report is claimed. The requested history payload is 800 bytes, excluding allocation overhead.
- Task04/repaired.cpp and Task03/address_pointer.cpp: ASan runs finish with exit 0 and empty stderr. Ordinary successful programs compile without warnings; the reordered experiment is the intended warning.

## Predictions and chronology

The `.prediction.txt` files were saved before first compilation/execution in this workflow. [prediction_record.json](prediction_record.json) preserves their timestamp, hashes and truthful provenance. They are not claimed to be an earlier personal student prediction. Saved predictions match exact stdout, including trailing spaces. The GitHub commits are real task-specific commits made during this preparation session; no earlier dates or artificial development intervals are claimed.

## Report and design figures

- [PDF report](report/Assignment4_Report.pdf): cover, repository link, six analyses, UML figures, access table, construction traces, pseudocode, comparisons and selected observed outputs.
- [Editable Markdown report](report/Assignment4_Report.md).
- [Payroll UML](report/task01-uml.png), [people UML](report/task02-uml.png), [fleet UML](report/task06-uml.png).

To rebuild the report with Python packages `reportlab` and `Pillow` installed:

```sh
python3 scripts/build_report.py
```

The generator uses Arial fonts from the standard macOS supplemental font folder; adjust those font paths when rebuilding on another platform. Body, table, code, footer and diagram labels are at least 11 pt in the generated report. Rental prices and late fees are explicitly stated demonstration assumptions because the brief does not supply exact policies. Complexity discussions include actual sizeof measurements; no universal timing ranking is inferred from those sizes.

The repository is public and can be shared using its link. Faculty submission remains the student's action.
