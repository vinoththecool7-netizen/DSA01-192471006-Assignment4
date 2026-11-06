# Task 2 - University people management

## 2.1 Relationships and inheritance

Student is a Person and Staff is a Person: public, virtual single inheritance in each branch. Together these form hierarchical inheritance. TeachingAssistant is both Student and Staff: public multiple inheritance, forming a hybrid diamond with the shared Person. ResearchScholar is a Student: public single inheritance, and Person -> Student -> ResearchScholar is multilevel inheritance. Person has an Address; Student has a Course: composition. A phone is a Person value, and a fellowship is a ResearchScholar value. A teaching assistant's two roles represent one university identity.

## 2.2 Diamond resolution

Without virtual inheritance, TA contains two Person subobjects. Student::Person and Staff::Person can disagree on name and ID, and unqualified Person member access and conversion to Person* are ambiguous. Virtual inheritance shares one Person. TA, as the most-derived class, initializes it. A Student or Staff constructed by itself initializes its own virtual Person. The deliberately ambiguous id expression is isolated in diagnostics/ambiguous.cpp.txt; its actual compiler error is retained.

## 2.3 Class design and access

relationships.cpp contains the complete independent declarations and executable demonstration. All identity fields, Address, programme, CGPA, Course, department, salary and fellowship are private; public accessors expose selected identity fields. All is-a edges are public, so external code can use a Person interface. Protected or private inheritance would restrict this substitutability. Constructors pass values through initializer lists. Person has a virtual destructor, and derived destructors use override. The UML is report/task02-uml.png.

## 2.4 Visibility of Person members in Student

| Person member | public inheritance | protected inheritance | private inheritance |
|---|---|---|---|
| public | public | protected | private |
| protected | protected | protected | private |
| private | inaccessible directly | inaccessible directly | inaccessible directly |

Private members remain present and can be reached through permitted Person functions; inheritance never makes them directly accessible to Student. Only the public result is exposed to ordinary callers. Protected members are available to Student and eligible descendants, subject to the C++ protected access rules.

## Prediction and verification

The saved prediction for the supplied virtual program is `Person Student Staff TA ` followed by newline. For the nonvirtual variant it is `Person Student Person Staff TA ` followed by newline, with no required compiler diagnostic for construction alone. Both exact stdout comparisons passed, including the trailing space. No differences occurred. Person prints once in the virtual version because the most-derived TA owns one shared virtual base; it prints twice in the nonvirtual version because each branch has a separate base. Removing virtual alone does not cause a compiler error. The separate ambiguous-member fixture does cause an error.

## Composition alternative and complexity

`struct ComposedTA { Student student; Staff staff; };` contains two Person subobjects, even though Student and Staff each inherit Person virtually: virtual sharing does not cross complete member objects. Read names with `ta.student.getName()` and `ta.staff.getName()` and define a synchronization policy, or move the common identity into a separate shared owner. The inheritance version uses `ta.getName()` unambiguously. Both accesses are O(1) for references; virtual-base adjustment can add a constant ABI-dependent load. Copying a name costs O(L) in its length. Both designs are O(1) object space under fixed-length fields, but the measured virtual TA is 192 bytes versus ComposedTA 280 bytes; Person is 88 bytes. These sizes include the Task 3 Address/Course members, not string heap allocations. A pair of nonvirtual role members totals 264 bytes. Virtual-base metadata can offset some savings; these numbers are specific to the tested ABI.
