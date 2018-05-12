# Elevator Search

### Description
A building with 10 floors, 2 elevators, and 20 people placed on the floors is modeled in python. Each person wants to move to a different floor, and the search algorithm finds the solution to moving the people between floors to their goal floor. Each person is either a normal guest or employee, or a VIP. VIPs must be taken to their destination floor before normal guests or employees. Each elevator only moves to a subset of the floors, but all floors are accessible be at least one elevator; floor 5 is the common floor that both elevators service.

The problem is broken down into four parts, taking VIPs without an elevator that services their initial floor and their goal floor to the common floor elevator hub, taking VIPs to their goal floor, taking employees and guests without an elevator that services their initial floor and their goal floor to the common floor elevator hub, and taking employees and guests to their goal floor.

### Youtube Video Demo
[![Elevator Search](https://img.youtube.com/vi/R2M_n5QAbnw/maxresdefault.jpg)](https://youtu.be/R2M_n5QAbnw "Elevator Search")

### How To Run:
```
>python2 hotel.py
```
