# Smartsheet Formula Reference

Generated from `data/formula_requests.csv`.

Total formula patterns: 8

## Cross-Sheet Formula

### RIO Checkbox Logic

**Business rule:** Check a box when a schedule milestone has a matching RIO item in another sheet

**Required columns:** Milestone ID; RIO

**Example formula:**

```text
=IF(COUNTIF({RIO Milestone ID}, [Milestone ID]@row) > 0, 1, 0)
```

**Notes:** Requires a cross-sheet reference to the RIO milestone ID column.

### RIO ID Lookup

**Business rule:** Return the Risk ID from the RIO log when the milestone ID matches

**Required columns:** RIO; Milestone ID; RIO ID

**Example formula:**

```text
=IF(RIO@row = 1, INDEX({RIO Risk ID}, MATCH([Milestone ID]@row, {RIO Milestone ID}, 0)), "")
```

**Notes:** Useful for linking schedule rows back to risk issue or opportunity records.

## Date Formula

### Schedule Moved in Workdays

**Business rule:** Calculate how many workdays a milestone moved between original and new schedule dates

**Required columns:** Original Schedule (Date); New Schedule (Date)

**Example formula:**

```text
=IF(OR(ISBLANK([Original Schedule (Date)]@row), ISBLANK([New Schedule (Date)]@row)), "", IF([New Schedule (Date)]@row >= [Original Schedule (Date)]@row, NETDAYS([Original Schedule (Date)]@row, [New Schedule (Date)]@row) - 1, -(NETDAYS([New Schedule (Date)]@row, [Original Schedule (Date)]@row) - 1)))
```

**Notes:** Positive values indicate delay; negative values indicate acceleration.

## Summary Formula

### Kickoff Total Count

**Business rule:** Count all rows in another sheet that contain kickoff hold checkboxes

**Required columns:** ***Hold Kick-off

**Example formula:**

```text
=COUNT({Hold Kick-off})
```

**Notes:** Counts total checkbox/star values in the referenced column.

### Kickoff Complete Count

**Business rule:** Count only checked/starred kickoff hold items from another sheet

**Required columns:** ***Hold Kick-off

**Example formula:**

```text
=COUNTIF({Hold Kick-off}, 1)
```

**Notes:** For checkbox or star columns, checked usually evaluates as 1.

## Text Formula

### Milestone ID Builder

**Business rule:** Combine milestone number property short name and task name into a readable milestone ID

**Required columns:** Walk Milestone Number; Property; Task Name

**Example formula:**

```text
=IF(ISBLANK([Walk Milestone Number]@row), "", [Walk Milestone Number]@row + " - " + LEFT(Property@row, FIND(" ", Property@row) - 1) + " " + [Task Name]@row)
```

**Notes:** Useful for building unique schedule task labels.

### Property Name Shortener

**Business rule:** Return special short property names for known exceptions and otherwise use the first word

**Required columns:** Property

**Example formula:**

```text
=IF(Property@row = "Waterstone at Big Creek", "Waterstone Big", IF(Property@row = "St. James at Goose Creek", "St. James", LEFT(Property@row, FIND(" ", Property@row) - 1)))
```

**Notes:** Good example of nested IF logic with property-name exceptions.

## Text/Number Formula

### Month Sort Helper

**Business rule:** Create a sortable month number so October November and December appear after earlier months

**Required columns:** First Month Budgeted

**Example formula:**

```text
=IF([First Month Budgeted]@row = "January", 1, IF([First Month Budgeted]@row = "February", 2, IF([First Month Budgeted]@row = "March", 3, IF([First Month Budgeted]@row = "April", 4, IF([First Month Budgeted]@row = "May", 5, IF([First Month Budgeted]@row = "June", 6, IF([First Month Budgeted]@row = "July", 7, IF([First Month Budgeted]@row = "August", 8, IF([First Month Budgeted]@row = "September", 9, IF([First Month Budgeted]@row = "October", 10, IF([First Month Budgeted]@row = "November", 11, IF([First Month Budgeted]@row = "December", 12, ""))))))))))))
```

**Notes:** Helps Smartsheet reports sort months in calendar order instead of alphabetically.
