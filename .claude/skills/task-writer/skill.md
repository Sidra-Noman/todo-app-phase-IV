# Skill: Task Decomposition (Task Writer)

## When to Use This Skill
- User requests `/sp.tasks`
- Plan is finalized
- Claude Code execution is next

## How This Skill Works
1. Split plan into atomic tasks
2. Ensure single responsibility per task
3. Make tasks independently testable
4. Define clear completion criteria
5. Prevent overlap or scope creep

## Output Format
- Task title
- Task goal
- Completion definition

## Quality Criteria
- Small and focused tasks
- Binary done/not-done
- Fully spec-aligned