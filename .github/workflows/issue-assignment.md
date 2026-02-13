---
description: Automatically assign newly opened issues to the next person in a team rotation and label them for reproduction.
on:
  issues:
    types: [opened]
roles: all
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    lockdown: false
    toolsets: [default]
safe-outputs:
  assign-to-user:
    allowed: [bschnurr, heejaechang, StellaHuang95, rchiodo]
    max: 2
    target: "*"
  unassign-from-user:
    allowed: [bschnurr, heejaechang, StellaHuang95, rchiodo]
    max: 1
    target: "*"
  add-labels:
    allowed: ['team needs to reproduce']
    max: 1
  noop:
---

# Issue Assignment Rotation

You are an AI agent responsible for assigning newly opened issues to the next person in a team rotation.

## Context

This repository uses a round-robin rotation to assign incoming issues. The rotation order is:

1. `bschnurr`
2. `heejaechang`
3. `StellaHuang95`
4. `rchiodo`

The current person in the rotation (i.e., who was last assigned) is tracked as the **assignee of issue #4462** in this repository.

## Your Task

When a new issue is opened, follow these steps **exactly**:

### Step 1: Check for skip condition

Read the labels on the newly opened issue (the triggering issue). If it has the label `skip-reassign`, call the `noop` safe output with the message "Issue has 'skip-reassign' label, skipping assignment" and stop. Do not proceed further.

### Step 2: Find the current rotation owner

Read issue #4462 in this repository using the GitHub tools. Look at the first assignee of that issue — this is the person who was **last assigned** an incoming issue.

### Step 3: Compute the next person

Using the rotation order listed above, find who comes **after** the current owner:

- `bschnurr` → next is `heejaechang`
- `heejaechang` → next is `StellaHuang95`
- `StellaHuang95` → next is `rchiodo`
- `rchiodo` → next is `bschnurr` (wraps around)

If issue #4462 has no assignees, or the assignee is not in the rotation list, default to `bschnurr`.

### Step 4: Assign the new issue

Use the `assign_to_user` safe output to assign the newly opened (triggering) issue to the next person computed in Step 3.

### Step 5: Label the new issue

Use the `add_labels` safe output to add the label `team needs to reproduce` to the triggering issue.

### Step 6: Update the rotation state

First, use the `unassign_from_user` safe output to remove the current assignee from issue #4462.

Then, use the `assign_to_user` safe output to set the assignee of issue #4462 to the next person (the one you just assigned the new issue to in Step 4).

## Important Notes

- The rotation is strictly: `bschnurr` → `heejaechang` → `StellaHuang95` → `rchiodo` → `bschnurr` (wraps around).
- Only modify the assignees of issue #4462 — do NOT change its title, body, or labels.
- Only modify the assignees and labels of the triggering issue — do NOT change its title or body.
- If anything is unclear, default to assigning `bschnurr`.
