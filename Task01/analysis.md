# Task 1 - Class design review

The original classes repeat name, ID and basic salary, repeat the DA rule, expose mutable payroll data, use inconsistent names (name/nm and id/code), retain an unused da field, and hide the allowance policy in 0.42. There is no common pay contract, so adding a category requires edits to each processing loop. Inconsistent representations also invite invalid states.

Staff owns private name and ID and declares pure virtual pay() and a virtual destructor. SalariedStaff owns basic and supplies the protected salaryWithDA() helper with a named DA_RATE. Professor adds research, LabAssistant uses salaryWithDA(), and GuestFaculty owns hours and rate. All inheritance is public: each derived object is substitutable for Staff. See payroll.cpp for complete declarations and report/task01-uml.png for UML.

## Design defence (57 words)

The abstract Staff interface lets one loop calculate every payment through a base pointer. Shared identity belongs to Staff, while the salaried helper keeps the allowance rule in one place. A new category implements pay() and is registered in the collection. Existing payroll classes and the processing loop stay unchanged. Private data prevents unrelated code from silently changing payroll fields.

## Alternative and complexity

TaggedStaff in payroll.cpp stores a type enum and all possible fields, then switches in pay(). Both implementations take O(1) time per call with three fixed types, O(n) for n staff, and O(1) per-object space under a fixed-size name abstraction (otherwise add name length). The tagged class wastes hours/rate in salaried records and basic/research in guest records. The hierarchy has dynamic-dispatch metadata, commonly one vptr, whose size is ABI-dependent. Actual sizeof results are in evidence/payroll.stdout.txt; sizeof excludes string heap allocations and container storage.

Adding a new tagged category changes at least three places: the enum, switch, and creation/registration site; adding new data may also change the common field declaration (four places). With inheritance, add one new class and update one creation site; zero existing payroll classes and zero processing loops change. Counts exclude serialization and user interfaces, which would require registration in either design. Assertions independently check 76000, 28400, 16000 and zero hours.
