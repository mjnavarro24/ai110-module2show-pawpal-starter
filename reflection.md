# PawPal+ Project Reflection

## 1. System Design


3 core actions: add tasks, see today's plan, input time constraints.  

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The classes I chose were Pet, Owner, Task, Plan, and ToDoList. An Owner can add/edit their availability. A TodoList can generate a plan and add, edit, or remove a Task. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes I changed it so that a Task holds a Pet attribute for the case when we have multiple Pets. 

I also changed it so that Owner holds both the todo list and the schedule. I made this change because the todolist and schedule would be associated with an owner, and in order to generate a schedule, the method will also need access to the todolist and the owner's availability. It makes more sense to have all the data stored in one place. Because of this change I also moved the generateSchedule method to the Owner. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Tradeoff: I optimized find_conflicts by sorting tasks by start time and breaking out of the inner loop as soon as a later task begins after the current one ends — since nothing after it can overlap either. It's faster than comparing every pair, but harder to read: the early break depends on a non-obvious invariant a reader has to reason through. For a small pet-care list the plain double loop would've been fast enough, so the speed isn't strictly necessary — but the code documents its own logic and shows the optimization intentionally.


Why it's reasonable: A pet owner's daily task list is small — a handful of items, not thousands — so the performance win is negligible in practice. But the same sort-and-short-circuit pattern is what makes conflict detection scale if PawPal ever tracks many pets or a full week of recurring tasks. Since the extra logic is contained in one well-commented function and doesn't leak complexity elsewhere, paying a small readability cost now for a design that won't need rewriting later is a sensible trade.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
