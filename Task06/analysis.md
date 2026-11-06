# Task 6 - Vehicle rental fleet

## Stage 1: Entities and testable requirements

Vehicle owns registration, daily rate, availability and agreed days. Bicycle has the basic daily charge. MotorVehicle adds fuel/charge percentage and a ServiceRecord member holding the due date. TwoWheeler adds a per-litre price. Car adds seats and a per-litre price. ElectricCar adds battery kWh and a per-kWh price and overrides the fuel charge. ElectricBus is a later extension with an extra daily cleaning charge. This interpretation treats charge level as a percentage and usage supplied at return as litres for combustion vehicles or kWh for electric vehicles.

Testable statements: list every type through Vehicle pointers; rent each available vehicle for positive days; reject a second rent; reject unknown registrations and invalid days; reject a return without an active rental; reject negative usage without changing rental state; return every type and restore availability; calculate an overdue return; and add ElectricBus without editing existing vehicle classes. input.txt is actually consumed by fleet.cpp and exercises these states.

## Stage 2: Hierarchy

Vehicle is abstract through pure virtual charge() and kind(), with a public virtual destructor. Vehicle -> Bicycle and Vehicle -> MotorVehicle form hierarchical inheritance. MotorVehicle -> TwoWheeler and MotorVehicle -> Car branch again. Car -> ElectricCar -> ElectricBus is multilevel inheritance. Each individual edge is public single inheritance; no multiple or virtual inheritance is needed. MotorVehicle has a ServiceRecord member. See report/task06-uml.png.

## Stage 3: Decisions and assumptions

Identity, rental state and transition checks belong to Vehicle so all types follow the same rent/return protocol. charge() varies and is virtual. rent and returnVehicle share fixed validation and billing workflow and call the virtual charge(). kind() supports listing. Data is private, with protected baseCharge() for reuse. Five stack objects own their lifetimes and an array<Vehicle*,5> supplies the required base-pointer collection. Its entries are non-owning and remain valid for the whole processing loop.

Pricing is an explicit demonstration policy because the brief gives no exact formulas: Bicycle=days*daily rate; TwoWheeler and Car add litres*price; ElectricCar adds kWh*price; ElectricBus also adds 50 per day for cleaning. A late return bills actual elapsed days and adds 25% of daily rate for each overdue day. Daily rates are 100,400,1000,1200,3000; litre price is 100 and kWh price is 10. Battery capacity, service date and level are recorded; no automatic physical fuel depletion or date scheduling is assumed. Car's per-litre field is zero in ElectricCar and is unused by its overridden charge, a small reuse tradeoff. A larger system could separate propulsion pricing by composition.

## Stage 4: Classes and pseudocode

fleet.cpp contains full declarations with access specifiers and implementations. Pseudocode follows explicit INPUT/OUTPUT, assignment, selection and iteration blocks:

```text
ALGORITHM RentVehicle
INPUT Fleet, Registration, Days
OUTPUT Success or error
SET V TO the matching pointer found by scanning Fleet
IF V is absent OR Days <= 0 OR V is already rented THEN
    OUTPUT error
ELSE
    SET V.agreedDays TO Days
    SET V.rented TO TRUE
    OUTPUT success
END IF
END ALGORITHM

ALGORITHM ReturnVehicle
INPUT Fleet, Registration, ElapsedDays, Usage
OUTPUT Bill or error
SET V TO the matching pointer found by scanning Fleet
IF V is absent OR V is not rented OR ElapsedDays <= 0
   OR Usage < 0 OR Usage is not finite THEN
    OUTPUT error
ELSE
    SET LateDays TO MAX(0, ElapsedDays - V.agreedDays)
    SET Bill TO V.charge(ElapsedDays, Usage)
                + LateDays * V.dailyRate * 0.25
    SET V.rented TO FALSE
    SET V.agreedDays TO 0
    OUTPUT Bill
END IF
END ALGORITHM
```

## Stage 5: Demonstration and independent results

All five types rent for two agreed days and return after three. Bicycle: 3*100+25=325. TwoWheeler: 3*400+2*100+100=1500. Car: 3*1000+5*100+250=3750. ElectricCar: 3*1200+20*10+300=4100. ElectricBus: 3*3000+50*10+3*50+750=10400. The runner checks all five values and five expected errors. An on-time Bicycle return later bills 100. The final list shows all five available. Invalid negative usage leaves the active rental intact so a valid return can follow.

ElectricBus is implemented as an added subclass overriding charge() and kind(). Only the demo construction and pointer-array registration are expanded; existing classes and processing functions are unchanged. See evidence/fleet.stdout.txt for the complete consumed-input transcript.

## Alternative and complexity

tagged.cpp implements a single TaggedVehicle with an enum and switch. It computes the electric bus charge before the late fee as 9650 and checks it independently. charge is O(1) for both a fixed switch and a virtual call. Search/rent/return takes O(n) due to linear registration lookup, while listing takes O(n); storage is O(n) plus registration/date string lengths. An individual fixed-field object uses O(1) space, excluding dynamic string buffers.

The tagged representation keeps seats, battery, both pricing units, service date and level even in bicycles. The hierarchy stores only fields along a type's base chain, plus implementation-dependent virtual dispatch metadata (commonly one vptr for this single hierarchy). The Car/ElectricCar reuse tradeoff above leaves one unused field, so it is not literally zero wasted space. Actual TaggedVehicle sizeof is in evidence/tagged.stdout.txt; sizeof excludes string heap payloads. Adding a type in the tagged approach changes enum, switch and creation/registration (at least three places); a new data shape may also change common fields. In the hierarchy, add one class and its creation/registration while changing zero existing class definitions and zero generic loops. No claim is made that every application-level factory or serializer needs no registration.
