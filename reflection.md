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

My scheduler considers priority and time. I decided these mattered the most to creating a functioning/usable schedule and that preferences is a nice to have feature but not an MVP feataure for this case. 

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

I used AI tools for most of the project steps, asking for feedback on my initial design as well as for implementing, debugging, and refactoring. 
The prompt "Ask your AI coding assistant to review your skeleton: attach pawpal_system.py and ask if it notices any missing relationships or potential logic bottlenecks." did reveal some gaps and was a great/necessary question for creating the foundation. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I would constantly verify/evaluate what the AI suggested by asking follow up questions to what it's designed. If it didn't understand something I asked it multiple times step by step, questioning it in the case it might recognize it was wrong. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I created tests for each of the methods I created to ensure everything was covered. Having tests is important because it is diffuclt to test everything manually. When a change was made I could run the tests to make sure everything still runs correctly. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am 90% confident in the current functionality because of the robustness of my tests on my logic. The scheduler c
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am satisfied with how quickly the functionality was put together and how usable the pet scheduler is. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would like to improve both the UI and some functionality. If there is a conflict, I want to provide the user a way to edit the task times to what time works best. This way their schedule no longer keeps the conflict and they can still move the task to another spot on their schedule. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

That it takes a lot of time and thought into designing a system. It also seems like the more simple you start the better. I started with a lot of complexity at first which made it a bit difficult to organize at the start. 