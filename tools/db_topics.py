# -*- coding: utf-8 -*-
"""Content for the generated database modules.

The track had twenty-two modules and almost all of them were about writing a
query. Joins, CTEs, window functions and execution order were covered well;
schema design, constraints and concurrency were not covered at all. That is the
wrong half to be missing, because a query that is merely slow gets rewritten
and a schema that permits bad data does not get noticed until it has.

Every page runs real SQLite in the browser, seeded with tables built for the
module. The error messages are the database's own - a foreign key violation
here is the message a reader will meet again in a real connection, not a
paraphrase of it.
"""

TOPICS = []


def topic(slug, title, cat, lead, svg, notes, article, check,
          seed=None, starter=None, variants=None, variants_label=None,
          timeline=None):
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "seed": seed, "starter": starter, "variants": variants,
        "variants_label": variants_label, "timeline": timeline,
        "notes": notes, "article": article, "check": check,
    })


A = "var(--accent-primary)"
M = "var(--text-muted)"
B = "var(--border-subtle)"
S = "var(--bg-surface)"


def _svg(body):
    return '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">%s</svg>' % body


def _box(x, y, w, h, fill="none", stroke=B, sw=2, rx=3):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, fill, stroke, sw))


def _txt(x, y, s, fill=M, size=9, anchor="middle", weight="normal"):
    return ('<text x="%s" y="%s" fill="%s" font-size="%s" font-family="monospace" '
            'text-anchor="%s" font-weight="%s">%s</text>'
            % (x, y, fill, size, anchor, weight, s))


def _line(x1, y1, x2, y2, stroke=A, sw=1.4, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, stroke, sw, d))


def _grid_rows(x, y, w, h, n, accent=A):
    """Stacked horizontal bands - a row store, where a row is contiguous."""
    return "".join(_box(x, y + i * (h + 3), w, h,
                        fill=(S if i else "none"),
                        stroke=(accent if i == 0 else B), sw=1.4, rx=2)
                   for i in range(n))


def _grid_cols(x, y, w, h, n, accent=A):
    """Side-by-side vertical bands - a column store, where a column is."""
    return "".join(_box(x + i * (w + 3), y, w, h,
                        fill=(S if i else "none"),
                        stroke=(accent if i == 0 else B), sw=1.4, rx=2)
                   for i in range(n))


def _table_icon(x, y, w=44, rows=3):
    out = [_box(x, y, w, 10 + rows * 9, fill=S)]
    out.append(_box(x, y, w, 10, fill=A, stroke=B, sw=1))
    for r in range(rows):
        out.append(_line(x, y + 10 + r * 9, x + w, y + 10 + r * 9, B, 0.8))
    return "".join(out)


# ---------------------------------------------------------------------------
# 1. Primary and foreign keys
# ---------------------------------------------------------------------------
topic(
    "primary_and_foreign_keys",
    "Primary and Foreign Keys",
    "Schema Design",
    "The two constraints that stop a database from holding rows that cannot be "
    "true. Try to break them and watch the insert be refused.",
    _svg(_table_icon(14, 22) + _txt(36, 82, "customers", M, 8)
         + _line(58, 40, 100, 40) + _txt(79, 34, "FK", A, 8)
         + _table_icon(100, 22) + _txt(122, 82, "orders", M, 8)),
    seed="""
CREATE TABLE customers (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL
);

CREATE TABLE orders (
    id           INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(id),
    total        REAL NOT NULL
);

INSERT INTO customers (id, name) VALUES (1, 'Ada'), (2, 'Grace'), (3, 'Alan');
INSERT INTO orders (id, customer_id, total) VALUES
    (1, 1, 42.00), (2, 1, 18.50), (3, 2, 99.99);

PRAGMA foreign_keys = ON;
""",
    starter="""-- Try each of these in turn.

-- 1. A duplicate primary key.
INSERT INTO orders (id, customer_id, total) VALUES (1, 2, 5.00);

-- 2. An order for a customer who does not exist.
-- INSERT INTO orders (id, customer_id, total) VALUES (9, 77, 5.00);

-- 3. Deleting a customer who still has orders.
-- DELETE FROM customers WHERE id = 1;
""",
    notes=[
        "A primary key is two promises in one: the value is unique, and it is "
        "never NULL.",
        "A foreign key says this column's value must already exist in another "
        "table's key column.",
        "The database enforces both on every write. Application code that "
        "checks first still has a race; the constraint does not.",
        "SQLite needs <code class='mono-font'>PRAGMA foreign_keys = ON</code>. "
        "Most engines enforce them by default.",
    ],
    article="""
title: Primary and Foreign Keys
intro: The two constraints that make a row hopeless to write if it couldn't be true.

## A key is a promise about identity

A **main key** is the column, or set of columns, whose value spots a
row uniquely and permanently. Declaring one asks the DB for two
ensures at once: no two rows share this value, and no row leaves it NULL.

That second half is easy to overlook and does real work. NULL means unknown. A
row whose identity is unknown can't be referred to, updated with trust,
or joined against, so a nullable identifier isn't an identifier at all.

Run the first statement in the editor. The insert is refused, and the message
comes from SQLite rather than from any of it on this page:
`UNIQUE constraint failed: orders.id`. Nothing in the use had to check
first, and no amount of concurrent traffic can slip a duplicate past it.

## A foreign key is a promise about reference

A **foreign key** says: what value sits in this column must already exist
in that column of that table. `orders.customer_id` refs `customers.id`,
so an order can only belong to a customer who is really there.

Uncomment the second statement and run it. Order 9 claims customer 77, and
customer 77 doesn't exist, so the write fails. Without the constraint the row
would be accepted and the problem would surface much later, as a join that
silently returns fewer rows than expected or a report whose totals don't
merge.

This is the value of the constraint and it's worth stating plainly: it turns a
data-quality problem, which is found weeks later by a human, into a write
error, which is found right away by a machine.

## What happens to the other side

Uncomment the third statement. Deleting customer 1 is refused, because orders 1
and 2 point at that customer and dropping it would leave them pointing at
nothing. The DB won't create the orphan.

Refusing is one of a few available answers, chosen with `ON DELETE`:

| Clause | Behaviour |
|---|---|
| `RESTRICT` / `NO ACTION` | refuse the delete while children exist (the default) |
| `CASCADE` | delete the children too |
| `SET NULL` | keep the children, blank the reference |
| `SET DEFAULT` | point the children at a default row |

`CASCADE` is convenient and worth respecting. Deleting one customer can silently
drop thousands of orders, and a cascade that runs through a few tables can
drop a great deal more than the person pressing the button expected.

## Natural against surrogate

Given a table of people, is the main key the email address or an int
that means nothing?

An email address is a **natural key**: it comes from the domain and carries
meaning. It's also mutable, at times shared, at times absent, and awkward
to index. each row that refs it stores a whole string, and a person
changing their address means updating each one of them.

A meaningless int is a **surrogate key**. It's stable because nothing in
the world can force it to change, compact to store and to index, and safe to
scatter across a dozen referencing tables.

The usual practice is a surrogate main key plus a `UNIQUE` constraint on the
natural one, which buys stable identity and still refuses two accounts on the
same address.

## Composite keys

A key can span a few columns. A table recording which student is enrolled on
which course has a main key of `(student_id, course_id)`: neither column
alone spots a row, and the pair does. That declaration also states a
business rule &mdash; a student can enrol on a course once &mdash; which the
DB will now enforce for free.

## Why the child side needs its own index

The parent side of a foreign key is indexed for free. It's a main key.
The child side often isn't, and that omission turns cheap ops into full
scans, because each referential action has to ask "are there children?" and
answer it by looking.

Delete a customer with 5,000,000 orders in the child table. With no index on
`orders.customer_id`:

|operation|with no index on the child FK|with the index|
|---|---|---|
|`ON DELETE RESTRICT` check|scan up to 5,000,000 rows|a single index seek|
|`ON DELETE CASCADE`|scan to find the children|seek straight to them|
|a join `customers &#8904; orders`|scan the child table|indexed lookup|

The DB enforces the constraint right either way. The difference is
whether each check is a seek or a scan of the whole child table. This is the
quiet reason a schema "with foreign keys" can still be slow: the constraint was
declared, the supporting index on the referencing column wasn't, and each
delete or cascade pays for it.

## Why the surrogate key is usually smaller too

The natural-versus-surrogate choice has a storage side that compounds with each
referencing table. A natural key. An email, a UUID string &mdash; is copied
into each child row that refs it. So Its width is paid once per ref,
not once per person:

|key in 5 child tables, 10M rows each|storage in the children|
|---|---|
|email as the foreign key (~30 bytes)|~1,500 MB|
|surrogate integer (4 bytes)|~200 MB|

The surrogate isn't just stable against change. It's seven times smaller
across the refs, and a smaller key means more index entries per page, so the
indexes that use it are smaller and shallower too. The natural key still earns a
`UNIQUE` constraint so the real-world rule ("one account per email") is enforced;
it simply doesn't also have to be the value scattered across a dozen tables. That
is the thinking behind "surrogate main key plus a unique natural key" &mdash;
stable, compact identity for the machine, and the business rule kept as well.

## Questions people ask

<strong>Can a table have more than one primary key?</strong> No. A table has exactly one primary key, though it can span several columns. Other columns that must be unique can use a UNIQUE constraint instead.

<strong>Can a foreign key be NULL?</strong> Yes. A NULL foreign key means no reference, and the database skips the check for that row. Add NOT NULL to the column if every child must have a parent.

<strong>Does a foreign key create an index?</strong> Not on the child side. The parent key is indexed because it is a primary or unique key, but the referencing column needs its own index if you join or cascade on it.

<strong>Should I use an auto-increment integer or a UUID as the primary key?</strong> An integer is smaller and sorts in insert order, which keeps the index compact. A UUID is useful when ids are generated in many places, at the cost of larger keys and scattered inserts.

<strong>What happens if I delete a parent row that has children?</strong> By default the delete is refused. You can choose ON DELETE CASCADE to remove the children, or SET NULL to keep them with no parent.

<strong>Why does my foreign key not stop bad inserts in SQLite?</strong> SQLite leaves enforcement off unless you run PRAGMA foreign_keys = ON on each connection. Without it the REFERENCES clause is accepted and ignored.

## Where it goes wrong

**Turning foreign keys off for speed.** They cost a thing on write. The
cost of not having them is found in production, in data that no longer
makes sense, and it's much harder to pay.

**Losing the pragma.** SQLite ships with foreign key enforcement off for
backwards compatibility. A schema full of `Refs` clauses that were never
enforced looks correct and ensures nothing.

**Making the main key real.** any of it that carries meaning can change,
and a main key that changes has to be chased through each table that
refs it.

**Leaving the foreign key column unindexed.** The parent side is indexed by its
main key automatically. The child side often isn't, and each cascade or
referential check then scans the whole child table.
""",
    check=[
        {"q": "What two guarantees does declaring a primary key give you?",
         "options": ["Uniqueness and an index", "Uniqueness and NOT NULL",
                     "NOT NULL and a default", "Uniqueness and sort order"],
         "answer": 1,
         "why": "No two rows may share the value, and no row may leave it NULL. A row whose identity is unknown cannot be referred to at all."},
        {"q": "Why is a surrogate integer usually preferred over an email address as a primary key?",
         "options": ["Integers sort faster",
                     "Nothing in the world can force it to change, so referencing rows never need updating",
                     "Emails cannot be indexed",
                     "It uses less disk"],
         "answer": 1,
         "why": "A natural key carries meaning and meaning changes. A person changing their email would mean updating every referencing row; a meaningless integer is stable by construction."},
        {"q": "Why does SQLite in particular need `PRAGMA foreign_keys = ON`?",
         "options": ["It has no foreign keys",
                     "Enforcement is off by default for backwards compatibility, so REFERENCES clauses are accepted but ignored",
                     "It only enforces them on DELETE",
                     "The pragma creates the index"],
         "answer": 1,
         "why": "The schema parses and looks correct while guaranteeing nothing, which is worse than having no constraint at all because it invites trust."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Constraints
# ---------------------------------------------------------------------------
topic(
    "constraints_in_sql",
    "Constraints: UNIQUE, CHECK and NOT NULL",
    "Schema Design",
    "Rules the database refuses to break, written once in the schema instead "
    "of everywhere in the application.",
    _svg(_box(20, 26, 120, 40, fill=S)
         + _txt(80, 42, "CHECK (age &gt;= 18)", A, 10)
         + _txt(80, 58, "refused on write", M, 8)
         + _txt(80, 80, "one rule, every client", M, 7)),
    seed="""
CREATE TABLE staff (
    id      INTEGER PRIMARY KEY,
    email   TEXT    NOT NULL UNIQUE,
    age     INTEGER NOT NULL CHECK (age >= 18),
    salary  REAL    NOT NULL CHECK (salary > 0),
    grade   TEXT    NOT NULL DEFAULT 'junior'
                    CHECK (grade IN ('junior', 'mid', 'senior'))
);

INSERT INTO staff (id, email, age, salary, grade) VALUES
    (1, 'ada@example.com',   36, 62000, 'senior'),
    (2, 'grace@example.com', 41, 71000, 'senior'),
    (3, 'alan@example.com',  28, 48000, 'mid');
""",
    starter="""-- Each of these violates exactly one constraint.
-- Run them one at a time and read which one fires.

INSERT INTO staff (id, email, age, salary) VALUES (4, 'ada@example.com', 30, 50000);

-- INSERT INTO staff (id, email, age, salary) VALUES (5, 'new@example.com', 15, 50000);
-- INSERT INTO staff (id, email, age, salary) VALUES (6, 'x@example.com', 30, -1);
-- INSERT INTO staff (id, email, age, salary, grade) VALUES (7, 'y@example.com', 30, 1, 'boss');
-- INSERT INTO staff (id, email, age) VALUES (8, 'z@example.com', 30);
""",
    notes=[
        "<code class='mono-font'>NOT NULL</code> says the value must be known. "
        "<code class='mono-font'>UNIQUE</code> says no other row may hold it.",
        "<code class='mono-font'>CHECK</code> takes an expression that must be "
        "true for every row. It is the general case the others specialise.",
        "A constraint holds regardless of which client wrote the row. "
        "Application validation only holds for the clients that run it.",
        "<code class='mono-font'>UNIQUE</code> permits multiple NULLs in most "
        "engines, because two unknowns are not known to be equal.",
    ],
    article="""
title: Constraints: UNIQUE, CHECK and NOT NULL
intro: Rules written once in the schema, enforced against each client, forever.

## Where a rule should live

"Age must be at least 18" can be written in three places: the form in the
browser, the service that handles the request, or the table itself.

The first two are worth having and neither is enough. A browser check is a
courtesy to the user and is bypassed by any of it that isn't a browser. A
service check holds until someone writes a second service, a migration script,
a bulk import or a manual fix at the console. And each one of those is
written by someone who wasn't thinking about the rule at the time.

A constraint in the schema holds for all of them, including the ones that do
not exist yet. It's checked on each write, by the one component each path
must go through.

## The three, and what each says

**NOT NULL** &mdash; the value must be known. NULL isn't a value. It's the
lack of one. Allowing it means allowing rows where the question was never
answered, and each query that touches the column then has to decide what to do
about that.

**UNIQUE** &mdash; no other row may hold this value. It's what stops two
accounts sharing an email address without needing a read-then-write in the
use, which is a race rule even when it looks correct.

**CHECK** &mdash; this formula must be true for each row. It's the general
case that the other two are special instances of, and it takes plain SQL:

```
CHECK (age >= 18)
CHECK (salary > 0)
CHECK (grade IN ('junior', 'mid', 'senior'))
CHECK (end_date IS NULL OR end_date > start_date)
```

That last one is worth noticing. A constraint can relate two columns of the same
row, so "an end date, if present, must come after the start date" is enforceable
&mdash; a rule that is or else checked nowhere and violated eventually.

## Read the error, not the row count

Run each commented statement in turn. The value of doing so is that each one
fails differently, and the message names the constraint that stopped it:

| Attempt | Message |
|---|---|
| Duplicate email | `UNIQUE constraint failed: staff.email` |
| Age 15 | `CHECK constraint failed` |
| Negative salary | `CHECK constraint failed` |
| Grade `'boss'` | `CHECK constraint failed` |
| Missing salary | `NOT NULL constraint failed: staff.salary` |

Naming constraints by name &mdash; `CONSTRAINT staff_age_adult CHECK (...)`
&mdash; makes those messages far more handy, because "CHECK constraint failed"
tells you nothing when a table has six of them.

## The NULL subtlety in UNIQUE

`UNIQUE` allows more than one NULL in almost each engine, and people are
surprised by this until they see the thinking.

`UNIQUE` forbids two rows being *equal*. Checking NULL to NULL doesn't
give true. It makes NULL, because two unknown values aren't known to be
the same. So two NULLs aren't equal, and the constraint has nothing to object
to.

The hands-on consequence is that `UNIQUE` on a nullable column doesn't
ensure one row per real-world thing. It ensures one row per *known*
value. If that isn't what you meant, add `NOT NULL`.

## DEFAULT is not a constraint

`DEFAULT 'junior'` supplies a value when the insert omits the column. It
constrains nothing: an insert that by name passes NULL gets NULL, not the
default, unless `NOT NULL` refuses it.

Defaults and constraints are often paired for this reason. The default
handles the common case, and the constraint handles the case where someone was
clear about a thing they shouldn't have been.

## The NULL count that surprises people, measured

`UNIQUE` allowing many NULLs isn't a quirk to store but a consequence to see.
Because NULL = NULL is *unknown* rather than true, two NULLs are never "equal" and
the constraint has nothing to reject. In the SQLite this page runs, a `UNIQUE`
column happily accepts row after row of NULL:

```
CREATE TABLE t (email TEXT UNIQUE);
INSERT INTO t VALUES (NULL), (NULL), (NULL);   -- all three succeed
INSERT INTO t VALUES ('a@x.com');
INSERT INTO t VALUES ('a@x.com');              -- THIS one fails
```

Three unknown emails coexist. The first repeated *known* value is refused. This is
not even steady across engines. SQL Server permits just one NULL in a
unique column, while PostgreSQL, MySQL and SQLite permit many &mdash; so a schema
that leans on either action isn't portable. If the rule you meant was "one row
per real address", `UNIQUE` alone doesn't say it. `UNIQUE` plus `NOT NULL` does.

## Adding one to a large table is not free

A constraint added at `CREATE TABLE` costs nothing. One added later has to be
*proved* against each existing row before the DB will accept it. Adding
`CHECK (age >= 18)` or a `NOT NULL` to a 50-million-row table means the engine
reads all 50 million rows to confirm none already violates it, and in most engines
it holds a lock on the table while it does:

|constraint added|what the database must do|
|---|---|
|at table creation|nothing; no rows exist yet|
|to a 50M-row table|read all 50M rows, usually under a lock|

So the same declaration is instant on an empty table and an outage on a full one.
This is why constraints should encode what is *structurally* true &mdash; a
salary is plus, an end date follows a start date &mdash; rather than current
policy. A `CHECK` on this year's VAT rate has to be dropped and re-verified across
each row each time the rate changes. Re-verifying a large table is the
costly op above, paid on a schedule set by the tax authority rather
than by you.

## Questions people ask

<strong>What is the difference between NOT NULL and a CHECK constraint?</strong> NOT NULL rejects missing values. CHECK evaluates any condition on the row, such as price greater than zero, and rejects the row if it is false.

<strong>Does UNIQUE allow multiple NULLs?</strong> In most databases, yes, because NULL is not equal to NULL. SQL Server is a notable exception that allows only one, so check your engine.

<strong>Is DEFAULT a constraint?</strong> No. DEFAULT only fills in a value when none is given. It does not stop someone inserting a different value or an explicit NULL.

<strong>Why not validate everything in application code?</strong> Application checks can be bypassed by another service, a script, or a bug. A constraint is enforced for every writer, so the rule holds no matter who connects.

<strong>Will adding a constraint to a big table lock it?</strong> It can. The database has to check every existing row, and some engines hold a lock while doing so. Many support adding the constraint as not validated first, then validating later.

<strong>What error do I get when a constraint fails?</strong> The statement is rejected with an error naming the constraint, and no row from that statement is written. Read the message, because it tells you which rule was broken.

## Where it goes wrong

**Unnamed constraints.** Six `CHECK`s on a table and an error that says only
"CHECK constraint failed" wastes real time. Name them.

**Constraints that encode volatile policy.** A `CHECK` on a VAT rate has to be
migrated when the rate changes, and migrating a constraint on a large table is
not free. Constrain what is structurally true, not what is currently true.

**given UNIQUE means one per thing.** With NULLs allowed it means one per
known value.

**Adding a constraint to a large live table without thinking.** The DB has
to verify each existing row before it can accept the constraint, and in most
engines that takes a lock while it does. Plan the migration during a low-traffic
window so it does not block other writes.
""",
    check=[
        {"q": "Why does UNIQUE usually permit several NULLs?",
         "options": ["NULLs are stored separately",
                     "UNIQUE forbids equal values, and two NULLs are not known to be equal",
                     "It is a bug retained for compatibility",
                     "NULL is treated as zero"],
         "answer": 1,
         "why": "Comparing NULL to NULL yields NULL, not true. The constraint only rejects rows it can prove equal, so unknown values slip through - add NOT NULL if that is not what you meant."},
        {"q": "What can a CHECK constraint do that NOT NULL and UNIQUE cannot?",
         "options": ["Run on delete",
                     "Relate two columns of the same row, such as end_date > start_date",
                     "Reference another table",
                     "Supply a default value"],
         "answer": 1,
         "why": "CHECK takes an arbitrary expression over the row, so multi-column rules are enforceable. They are otherwise checked nowhere and violated eventually."},
        {"q": "Why is a constraint stronger than the same rule in application code?",
         "options": ["It runs faster",
                     "It holds for every client, including migrations, imports and consoles that were never written yet",
                     "It cannot be dropped",
                     "It produces better error messages"],
         "answer": 1,
         "why": "Application validation holds only for the code paths that run it. The database is the one component every write must pass through."},
    ],
)


# ---------------------------------------------------------------------------
# 3. Aggregate functions
# ---------------------------------------------------------------------------
topic(
    "aggregate_functions_in_sql",
    "Aggregate Functions and the NULL Trap",
    "Querying",
    "COUNT, SUM, AVG, MIN and MAX over a live table, and the one thing they "
    "all do with NULL that catches people out.",
    _svg("".join(_box(18 + i * 15, 30, 11, 26, fill=S) for i in range(5))
         + _txt(80, 70, "many rows &#8594; one value", M, 8)
         + _txt(80, 22, "SUM  AVG  COUNT", A, 9)),
    seed="""
CREATE TABLE readings (
    id       INTEGER PRIMARY KEY,
    station  TEXT NOT NULL,
    temp_c   REAL          -- deliberately nullable: the sensor sometimes fails
);

INSERT INTO readings (id, station, temp_c) VALUES
    (1, 'north', 12.0), (2, 'north', 14.0), (3, 'north', NULL),
    (4, 'south', 21.5), (5, 'south', NULL),  (6, 'south', 18.5),
    (7, 'west',  NULL),  (8, 'west',  NULL), (9, 'west', 9.0);
""",
    starter="""SELECT COUNT(*)        AS rows_total,
       COUNT(temp_c)   AS rows_with_a_reading,
       SUM(temp_c)     AS total,
       AVG(temp_c)     AS mean,
       MIN(temp_c)     AS coldest,
       MAX(temp_c)     AS warmest
FROM   readings;
""",
    variants_label="Same table, four questions",
    variants=[
        {"label": "The NULL trap",
         "sql": """-- COUNT(*) counts rows. COUNT(col) counts non-NULL values.
-- The gap between them is your missing data, for free.
SELECT COUNT(*) AS rows_total,
       COUNT(temp_c) AS have_reading,
       COUNT(*) - COUNT(temp_c) AS missing
FROM   readings;"""},
        {"label": "AVG ignores NULL",
         "sql": """-- AVG skips NULLs entirely. It is SUM/COUNT(col), not SUM/COUNT(*).
-- Substituting zero for a missing reading gives a different, wrong answer.
SELECT AVG(temp_c)                  AS avg_skipping_nulls,
       AVG(COALESCE(temp_c, 0))     AS avg_treating_null_as_zero,
       SUM(temp_c) / COUNT(*)       AS sum_over_all_rows
FROM   readings;"""},
        {"label": "Per group",
         "sql": """SELECT station,
       COUNT(*)      AS readings,
       COUNT(temp_c) AS usable,
       ROUND(AVG(temp_c), 2) AS mean_c
FROM   readings
GROUP  BY station
ORDER  BY station;"""},
        {"label": "Aggregating over no values at all",
         "sql": """-- Restrict to the rows that have no reading. COUNT(*) is 3, COUNT of
-- the column is 0, and SUM, AVG, MIN and MAX all come back NULL --
-- not zero, and not an error. Only COUNT returns a number.
SELECT COUNT(*)      AS rows_seen,
       COUNT(temp_c) AS values_seen,
       SUM(temp_c)   AS sum_c,
       AVG(temp_c)   AS avg_c,
       MIN(temp_c)   AS min_c,
       MAX(temp_c)   AS max_c
FROM   readings
WHERE  temp_c IS NULL;"""},
    ],
    notes=[
        "An aggregate collapses many rows into one value. Without "
        "<code class='mono-font'>GROUP BY</code> the whole table is one group.",
        "<code class='mono-font'>COUNT(*)</code> counts rows. "
        "<code class='mono-font'>COUNT(col)</code> counts rows where col is not "
        "NULL. The difference is your missing data.",
        "Every other aggregate skips NULL silently. "
        "<code class='mono-font'>AVG</code> divides by the number of values it "
        "actually saw, not by the number of rows.",
        "An aggregate over zero values is NULL, not zero &mdash; except "
        "<code class='mono-font'>COUNT</code>, which is 0.",
    ],
    article="""
title: Aggregate Functions and the NULL Trap
intro: Five functions that collapse many rows into one. The one action they share that quietly changes your answers.

## Many rows in, one value out

An aggregate function takes a set of rows and returns a single value. With no
`GROUP BY`, the set is the whole table. With one, it's each group in turn.

The five that matter are `COUNT`, `SUM`, `AVG`, `MIN` and `MAX`. Run the
starter query and all five appear side by side over the same nine rows. The
numbers don't agree with each other in the way you might expect, and the reason
is NULL.

## COUNT(*) and COUNT(col) are different functions

This is the single most handy gap on the page.

`COUNT(*)` counts **rows**. It doesn't look at any column, can't be affected
by NULL, and answers "how many records are there".

`COUNT(temp_c)` counts **non-NULL values in that column**. It answers "how many
records really have a reading".

The table has nine rows and four of them have no temperature. So `COUNT(*)` is
9 and `COUNT(temp_c)` is 5, and the gap between them is a free measure of
missing data:

```
SELECT COUNT(*) - COUNT(temp_c) AS missing FROM readings;
```

That one line is worth reaching for when a column's quality is in question.
It needs no subquery, no `IS NULL` filter and no second pass.

## Everything else skips NULL silently

`SUM`, `AVG`, `MIN` and `MAX` all skip NULL. They don't fail, warn, or
return NULL because a NULL was present. They behave as though those rows
weren't there.

For `SUM`, `MIN` and `MAX` this is almost always what you want. For `AVG` it's
the thing that catches people. **AVG cuts by the count of values, not
the count of rows**:

```
AVG(temp_c)  =  SUM(temp_c) / COUNT(temp_c)
```

Run the second variant. Three numbers appear that all have a claim to being
"the mean temperature", and they differ a lot:

| Expression | What it means |
|---|---|
| `AVG(temp_c)` | mean of the readings that exist |
| `AVG(COALESCE(temp_c, 0))` | mean if a broken sensor means zero degrees |
| `SUM(temp_c) / COUNT(*)` | total spread across all rows including the broken ones |

Which is correct depends fully on what NULL means in your data. If the sensor
failed, the first is right and the others are nonsense &mdash; a broken sensor
isn't a reading of zero. If NULL means "no sales that day", the second may well
be right. The DB can't decide this for you, and it won't ask.

## The empty group

Run the fourth variant. It restricts to the rows that have no reading at all,
so there are four rows and zero values. Each aggregate has to say what it
does with nothing.

`COUNT(*)` is 4 and `COUNT(temp_c)` is 0, as expected. `SUM`, `AVG`, `MIN` and
`MAX` all come back **NULL**. Not zero, and not an error. The rule is
that an aggregate over zero values returns NULL, and the single exception is
`COUNT`, which returns 0 because counting nothing truly is zero.

This matters when an aggregate feeds math. `SUM(amount) * 1.2` over a
group with no rows is NULL, and NULL passes through each op it
touches until a thing wraps it in `COALESCE`.

## GROUP BY and the shape of the result

Adding `GROUP BY station` changes the result from one row to one row per
station. The rule that follows is the one beginners trip on: each column in the
`SELECT` list must either be aggregated or appear in the `GROUP BY`.

the query has to give just one value per group. Given
three readings for `north`, there's no answer to "what is the id" &mdash;
there are three, and the DB won't choose one. Some engines once
allowed it and returned an any row. This Is worse than an error because
it works until it doesn't.

## Three averages of the same column

The "AVG cuts by the count of values, not rows" rule is best seen as three
numbers that all claim to be the mean. Five rows, two of them with a NULL
reading, the three present values being 10, 20 and 30 (sum 60):

|expression|value|what it computed|
|---|---|---|
|`AVG(t)`|**20**|60 / 3, the mean of the readings that exist|
|`SUM(t) / COUNT(*)`|**12**|60 / 5, the total spread across all rows|
|`AVG(COALESCE(t, 0))`|**12**|same, treating a missing reading as zero|

Confirmed in the SQLite this page runs. The gap between 20 and 12 isn't rounding
&mdash; it's the two NULLs, counted by `COUNT(*)` and skipped by `AVG`. Which one
is correct is a question about the data, not the SQL: if a NULL means a sensor
failed, 20 is right and 12 invents readings of zero. If it means "no sales that
day", 12 is right and 20 overstates the common day. The DB will find
whichever you write and warn you about neither.

## The empty group returns NULL, not zero

There's one more NULL action that breaks math downstream: an aggregate
over *no values* returns NULL, and only `COUNT` returns 0. Restrict to rows that
have no reading at all. A real group with zero values &mdash; and:

|aggregate|over an empty group|
|---|---|
|`COUNT(*)`|0|
|`COUNT(t)`|0|
|`SUM`, `AVG`, `MIN`, `MAX`|**NULL**|

`SUM` of nothing being NULL rather than 0 is the one that bites, because NULL then
passes: `SUM(amount) * 1.2` over an empty group is NULL, and it stays NULL
through each op until a thing wraps it in `COALESCE`. A report that
subtotals by group and then does math on the subtotals will show blanks, not
zeros, for the empty groups. And a blank where a number was expected is how
this surfaces, often in front of someone who trusts the report.

## Questions people ask

<strong>What is the difference between COUNT(*) and COUNT(column)?</strong> COUNT(*) counts rows. COUNT(column) counts only rows where that column is not NULL, so the two can differ.

<strong>Do aggregate functions ignore NULL?</strong> Yes, SUM, AVG, MIN, MAX and COUNT(column) all skip NULLs. That is why AVG of a column can differ from the sum divided by the row count.

<strong>What does SUM return on an empty set?</strong> NULL, not zero. Wrap it in COALESCE(SUM(x), 0) if you want a zero.

<strong>Why can I not use an aggregate in WHERE?</strong> WHERE filters rows before grouping, so the aggregate does not exist yet. Use HAVING to filter on aggregate results.

<strong>Why does SQL complain about columns not in GROUP BY?</strong> Each output row represents a group, so every selected column must be either grouped or aggregated. Otherwise the database has no single value to show.

<strong>How do I count distinct values?</strong> Use COUNT(DISTINCT column). It counts each different non-NULL value once, though it is slower than a plain count on large tables.

## Where it goes wrong

**Using AVG on data where NULL means zero.** The mean silently rises. Use
`COALESCE` when lack really is a zero.

**given COUNT(col) is a faster COUNT(*).** They answer different questions.
On a nullable column they return different numbers.

**Filtering aggregates in WHERE.** `WHERE COUNT(*) > 5` is an error &mdash;
`WHERE` runs before grouping, so no counts exist yet. That is what
[HAVING](having_in_sql.html) is for.

**Losing that NULL breaks math.** One NULL anywhere in an formula
makes the whole formula NULL.
""",
    check=[
        {"q": "What is the difference between COUNT(*) and COUNT(temp_c)?",
         "options": ["None, they are aliases",
                     "COUNT(*) counts rows; COUNT(temp_c) counts rows where that column is not NULL",
                     "COUNT(*) is slower",
                     "COUNT(temp_c) counts distinct values"],
         "answer": 1,
         "why": "The gap between them is exactly the number of missing values in the column, which makes it a one-line data-quality check."},
        {"q": "AVG(temp_c) over nine rows, four of them NULL, divides the sum by what?",
         "options": ["9", "5", "4", "It returns NULL"],
         "answer": 1,
         "why": "AVG skips NULLs entirely - it is SUM(col)/COUNT(col). Whether that is the answer you want depends on what NULL means in your data."},
        {"q": "What does SUM return over a group containing no non-NULL values?",
         "options": ["0", "NULL", "An error", "The row count"],
         "answer": 1,
         "why": "Every aggregate except COUNT returns NULL over nothing. That NULL then propagates through any arithmetic it feeds, which is why COALESCE turns up around aggregates so often."},
    ],
)


# ---------------------------------------------------------------------------
# 4. EXISTS vs IN vs JOIN
# ---------------------------------------------------------------------------
topic(
    "exists_vs_in_vs_join",
    "EXISTS, IN and JOIN",
    "Querying",
    "One question written three ways. Two give the same answer, one does not, "
    "and NULL decides which.",
    _svg(_txt(80, 24, "customers who ordered", M, 8)
         + _box(12, 34, 42, 24, fill=S) + _txt(33, 49, "EXISTS", A, 9)
         + _box(59, 34, 42, 24, fill=S) + _txt(80, 49, "IN", A, 9)
         + _box(106, 34, 42, 24, fill=S) + _txt(127, 49, "JOIN", A, 9)
         + _txt(80, 76, "same rows, different traps", M, 7)),
    seed="""
CREATE TABLE customers (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER,       -- nullable on purpose: some orders are anonymous
    total       REAL NOT NULL
);

INSERT INTO customers (id, name) VALUES
    (1, 'Ada'), (2, 'Grace'), (3, 'Alan'), (4, 'Edsger');

INSERT INTO orders (id, customer_id, total) VALUES
    (1, 1, 42.00), (2, 1, 18.50), (3, 2, 99.99), (4, NULL, 7.25);
""",
    starter="""-- Customers who have placed at least one order.
SELECT name
FROM   customers c
WHERE  EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)
ORDER  BY name;
""",
    variants_label="One question, four ways",
    variants=[
        {"label": "EXISTS",
         "sql": """-- Stops at the first matching row. Correct with NULLs present.
SELECT name
FROM   customers c
WHERE  EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)
ORDER  BY name;"""},
        {"label": "IN",
         "sql": """-- Same answer here. Fine, because we are asking for a match.
SELECT name
FROM   customers c
WHERE  c.id IN (SELECT customer_id FROM orders)
ORDER  BY name;"""},
        {"label": "JOIN",
         "sql": """-- Careful: a customer with two orders appears twice unless
-- you add DISTINCT. Compare this with the EXISTS version.
SELECT c.name
FROM   customers c
JOIN   orders o ON o.customer_id = c.id
ORDER  BY c.name;"""},
        {"label": "NOT IN - the broken one",
         "sql": """-- The point of the page. NOT IN returns NO ROWS, because the
-- subquery contains a NULL and 'x <> NULL' is unknown, never true.
-- NOT EXISTS gets it right. Run both.
SELECT 'NOT IN' AS form, name FROM customers c
WHERE  c.id NOT IN (SELECT customer_id FROM orders)

UNION ALL

SELECT 'NOT EXISTS', name FROM customers c
WHERE  NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);"""},
    ],
    notes=[
        "<code class='mono-font'>EXISTS</code> asks whether any row matches and "
        "stops at the first one. It never returns the row itself.",
        "<code class='mono-font'>IN</code> compares a value against a list. With "
        "a NULL in that list, <code class='mono-font'>NOT IN</code> can never be "
        "true.",
        "<code class='mono-font'>JOIN</code> multiplies rows: one customer with "
        "three orders becomes three rows unless you aggregate or add "
        "<code class='mono-font'>DISTINCT</code>.",
        "Modern planners often compile all three to the same plan. Correctness "
        "is the reason to choose, not speed.",
    ],
    article="""
title: EXISTS, IN and JOIN
intro: Three ways to ask whether a related row exists. The one that is quietly wrong.

## The same question

"Which customers have placed an order?" can be written with `EXISTS`, with `IN`,
or as a `JOIN`. Run the first three variants above and all three return Ada and
Grace &mdash; except that the JOIN returns Ada twice.

That difference is the first thing to understand, and the NULL action of the
fourth is the second.

## JOIN multiplies rows

A join doesn't filter the left table. It pairs each row on the left with each
matching row on the right. So A customer with three orders makes three
result rows.

When you want the orders, that is just right. When you want the customers,
it's a bug, and the usual patch is `DISTINCT`. That works, but it's worth
knowing what it costs: the DB made the duplicate rows and then sorted
or hashed them away. `EXISTS` never makes them in the first place.

The rule of thumb: **join when you want columns from the other table, use
EXISTS when you only want to know whether it's there**.

## EXISTS stops early

`EXISTS (subquery)` is true if the subquery returns at least one row. Not how
many, not which &mdash; just whether. That is why `SELECT 1` is the conventional
body: nothing in the select list is ever read. There's no reason to name a
column.

Because only existence matters, the engine can stop scanning the moment it finds
one match. For a customer with ten thousand orders, `EXISTS` looks at one.

`EXISTS` is also *linked*: the subquery refs `c.id` from the outer
query, so it's conceptually re-tested per outer row. Planners rarely execute
it that truly, but writing it that way is what makes the early exit
available.

## Where NOT IN breaks

Run the fourth variant. `NOT IN` returns **no rows at all**, and `NOT EXISTS`
returns Alan and Edsger, which is the correct answer.

Nothing is wrong with the data. Order 4 is anonymous, so its `customer_id` is
NULL, and the subquery returns the list `(1, 1, 2, NULL)`.

`c.id NOT IN (1, 1, 2, NULL)` expands to:

```
c.id <> 1  AND  c.id <> 1  AND  c.id <> 2  AND  c.id <> NULL
```

The final check isn't false. It's **unknown**. Alan's id is 3, and
whether 3 differs from an unknown value can't be found. `AND` with unknown
gives unknown, `WHERE` keeps only rows that are definitely true, and so nothing
lives. each row is filtered out, for each customer, silently and without an
error.

`NOT EXISTS` is unaffected because it never checks any of it to NULL. It asks
whether a matching row was found. The answer to that is always yes or no.

This is the hands-on rule, and it's worth committing to memory:

> **`NOT IN` with a nullable subquery column is a bug.** Use `NOT EXISTS`, or
> add `WHERE customer_id Isn't NULL` to the subquery.

The plus forms don't have this problem. `IN` returns true as soon as it
finds a real match, and an unknown among the left checks can't take
that away.

## What about performance

Twenty years ago these three had truly different costs and the advice was
elaborate. Modern planners in PostgreSQL, SQL Server and Oracle recognise all
three shapes and often compile them to the same physical plan &mdash;
often a semi-join, which is just "find whether a match exists, don't
duplicate rows".

So speed is rarely the reason to choose. The reasons that live are:

| Want | Use | Because |
|---|---|---|
| Columns from the other table | `JOIN` | it is the only one that gives them |
| Just to know it exists | `EXISTS` | no duplicates, early exit |
| Absence, nullable column | `NOT EXISTS` | `NOT IN` returns nothing |
| A short literal list | `IN` | `IN (1, 2, 3)` reads better than anything else |

Check the plan when it matters. [EXPLAIN](explain_and_query_plans.html) settles
in ten seconds what a rule of thumb argues about indefinitely.

## The NOT IN failure, run in this engine

The `NOT IN` trap is worth seeing execute rather than thinking about, because it
makes no error &mdash; only a wrong answer. Three customers, an orders table
where one order is anonymous (a NULL `customer_id`), asked which customers never
sorted:

|query|result|
|---|---|
|`... WHERE id NOT IN (SELECT customer_id FROM orders)`|**zero rows**|
|`... WHERE NOT EXISTS (SELECT 1 ...)`|**customer 3** (correct)|

The single NULL in the subquery poisons the whole `NOT IN`: `3 <> NULL` is
unknown, `AND` with unknown is unknown, and `WHERE` keeps only rows that are
definitely true, so each customer is filtered out. `NOT EXISTS` never checks
any of it to NULL. It asks whether a matching row was found &mdash; so it
returns the right answer on the same data. This isn't a corner case to file away;
a nullable column is the normal situation. This Is why `NOT EXISTS` is the safe
default and `NOT IN` earns its place only on a column that is provably `NOT NULL`.

## EXISTS stops at the first match

The early exit is the other reason to prefer `EXISTS`, and it's a real difference
in work done. `EXISTS` is true the moment one matching row is found, so for a
customer with ten thousand orders it checks one. `COUNT(*) > 0`, the common
option, counts all ten thousand before checking:

|test|rows the subquery examines|
|---|---|
|`EXISTS (SELECT 1 ...)`|1 (stops at the first)|
|`(SELECT COUNT(*) ...) > 0`|all of them|

The two return the same answer and do wildly different amounts of work, and the
gap grows with how many matches there are. Just the case where you least
want to count them. So the habit worth forming is `EXISTS` for "is there at least
one", never `COUNT(*) > 0`: the question is existence, and existence is answered
by the first row, not the last.

## Questions people ask

<strong>Is EXISTS faster than IN?</strong> Not always. Modern optimisers often turn both into the same plan. EXISTS can stop at the first match, which helps when the subquery is large.

<strong>Why does NOT IN return no rows when the subquery has a NULL?</strong> Because x NOT IN (1, NULL) evaluates to unknown, never true. Use NOT EXISTS, or filter NULLs out of the subquery.

<strong>When should I use a JOIN instead of EXISTS?</strong> Use a JOIN when you need columns from the other table. Use EXISTS when you only need to know whether a match exists.

<strong>Can a JOIN return duplicate rows where EXISTS does not?</strong> Yes. If one parent matches many children, a JOIN returns the parent once per child. EXISTS returns each parent once.

<strong>What does SELECT 1 inside EXISTS mean?</strong> Nothing special. EXISTS only checks whether any row comes back, so the selected columns are ignored.

<strong>How do I find rows with no match?</strong> Use NOT EXISTS, or a LEFT JOIN with a WHERE clause that checks the right side is NULL. Both are safe with NULLs.

## Where it goes wrong

**`NOT IN` on any of it nullable.** The query returns zero rows and looks like a
data problem.

**`SELECT *` inside `EXISTS`.** Harmless but misleading &mdash; it suggests the
columns are read, and they never are.

**`DISTINCT` as a reflex.** If a join is making duplicates, ask whether you
wanted the join at all. `DISTINCT` hides the symptom and pays for the rows twice.
""",
    check=[
        {"q": "Why does NOT IN return no rows when the subquery contains a NULL?",
         "options": ["NULL is treated as zero",
                     "The comparison against NULL is unknown rather than false, and WHERE keeps only definitely-true rows",
                     "NOT IN does not support subqueries",
                     "The subquery fails silently"],
         "answer": 1,
         "why": "NOT IN expands to a chain of <> comparisons joined by AND. One unknown makes the whole chain unknown for every row, so nothing survives the WHERE."},
        {"q": "Why does a JOIN sometimes return a customer twice when EXISTS does not?",
         "options": ["JOIN ignores the primary key",
                     "A join pairs each left row with every match, so two orders give two rows",
                     "EXISTS deduplicates automatically",
                     "The join is missing a condition"],
         "answer": 1,
         "why": "That multiplication is what a join is for when you want the other table's columns. EXISTS asks only whether a match is there, so it never produces the extra rows."},
        {"q": "Why is `SELECT 1` conventional inside EXISTS?",
         "options": ["It is faster than SELECT *",
                     "The select list is never read, so naming a column would be misleading",
                     "EXISTS requires a literal",
                     "It avoids a NULL check"],
         "answer": 1,
         "why": "EXISTS tests only whether a row was returned. Writing SELECT * suggests the columns matter, and they do not."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Self-joins
# ---------------------------------------------------------------------------
topic(
    "self_joins_in_sql",
    "Self-Joins",
    "Querying",
    "A table joined to itself, so a row can be compared against another row of "
    "the same kind. Employees and their managers, twice over.",
    _svg(_table_icon(20, 24, 40) + _txt(40, 82, "employees e", M, 7)
         + _table_icon(100, 24, 40) + _txt(120, 82, "employees m", M, 7)
         + _line(60, 40, 100, 40) + _txt(80, 34, "manager_id = id", A, 7)),
    seed="""
CREATE TABLE employees (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    manager_id INTEGER REFERENCES employees(id),
    salary     REAL NOT NULL
);

INSERT INTO employees (id, name, manager_id, salary) VALUES
    (1, 'Ada',    NULL, 120000),
    (2, 'Grace',  1,     98000),
    (3, 'Alan',   1,     95000),
    (4, 'Edsger', 2,     88000),
    (5, 'Barbara',2,    101000),
    (6, 'Donald', 3,     72000);
""",
    starter="""-- Two aliases for one table. e is the employee, m is the manager.
SELECT e.name AS employee,
       m.name AS manager
FROM   employees e
JOIN   employees m ON e.manager_id = m.id
ORDER  BY e.name;
""",
    variants_label="What a self-join can answer",
    variants=[
        {"label": "Employee and manager",
         "sql": """SELECT e.name AS employee, m.name AS manager
FROM   employees e
JOIN   employees m ON e.manager_id = m.id
ORDER  BY e.name;"""},
        {"label": "Keep the one with no manager",
         "sql": """-- Ada reports to nobody. An inner join drops her; LEFT JOIN keeps her
-- with a NULL manager, which is usually what you meant.
SELECT e.name AS employee, m.name AS manager
FROM   employees e
LEFT   JOIN employees m ON e.manager_id = m.id
ORDER  BY e.name;"""},
        {"label": "Paid more than their manager",
         "sql": """-- The comparison a self-join exists for: row against row.
SELECT e.name AS employee, e.salary, m.name AS manager, m.salary AS manager_salary
FROM   employees e
JOIN   employees m ON e.manager_id = m.id
WHERE  e.salary > m.salary;"""},
        {"label": "Pairs, without duplicates",
         "sql": """-- Every pair of colleagues under the same manager. The < in the
-- join condition is what stops (Alan, Grace) and (Grace, Alan) both
-- appearing, and stops anyone pairing with themselves.
SELECT a.name AS one, b.name AS other, a.manager_id AS under
FROM   employees a
JOIN   employees b ON a.manager_id = b.manager_id AND a.id < b.id
ORDER  BY under, one;"""},
    ],
    notes=[
        "There is nothing special about the syntax. It is an ordinary join "
        "where both sides happen to name the same table.",
        "Aliases stop being optional. Without <code class='mono-font'>e</code> "
        "and <code class='mono-font'>m</code> there is no way to say which "
        "<code class='mono-font'>name</code> you mean.",
        "An inner self-join silently drops the top of a hierarchy, because the "
        "root's parent is NULL. <code class='mono-font'>LEFT JOIN</code> keeps it.",
        "<code class='mono-font'>a.id &lt; b.id</code> in the join condition "
        "turns every unordered pair from two rows into one.",
    ],
    article="""
title: Self-Joins
intro: A table joined to itself, and the three questions that need one.

## Nothing new, except the alias

A self-join is an plain join in which both sides are the same table. There
is no special keyword and no special run. The only thing that changes is
that aliases become mandatory.

```
FROM  employees e
JOIN  employees m ON e.manager_id = m.id
```

`e` and `m` are two free views of the same rows. Without them, `name`
would be ambiguous &mdash; the DB has two columns with that name in scope
and no way to guess which was meant.

The mental move that makes this click is to stop thinking of `e` and `m` as one
table used twice, and start thinking of them as two tables that happen to
hold the same data. All else about joins then applies unchanged.

## When you need one

Self-joins answer questions that involve **checking a row to another row of the
same kind**, which SQL or else makes awkward.

**Hierarchies stored in one table.** An employee's manager is another employee.
A category's parent is another category. A reply's target is another comment.
Joining the table to itself resolves the ref into real columns.

**Row-to-row checks.** "Who earns more than their manager" needs both
salaries available at once. Run the third variant: Barbara earns 101,000 and
reports to Grace on 98,000, and the join is what puts those two numbers in one
row so a `WHERE` can compare them.

**Pairing rows within a group.** "Which colleagues share a manager" pairs the
table with itself on `manager_id`.

## The two conditions that keep pairs sane

The fourth variant holds a detail that looks small and isn't:

```
ON a.manager_id = b.manager_id AND a.id < b.id
```

Without `a.id < b.id`, two things go wrong. each row pairs with **itself**,
because a row trivially shares its own manager. And each genuine pair appears
**twice**, once as (Alan, Grace) and once as (Grace, Alan).

Writing `a.id <> b.id` fixes the first problem and not the second. Writing
`a.id < b.id` fixes both at once. For any two distinct rows just one
sorting meets it. That is the standard idiom for "each unordered pair once"
and it's worth recognising on sight.

## The top of the hierarchy disappears

Run the first variant and count the rows: five, not six. Ada is missing.

Ada is the root &mdash; her `manager_id` is NULL &mdash; and an inner join
needs a match on both sides. NULL matches nothing. So Her row is dropped
without comment.

The second variant uses `LEFT JOIN` and Ada reappears with a NULL manager. This
is nearly always what was intended, and the failure is quiet enough to reach
production: the query works, returns plausible rows, and is missing just the
most senior person in the organisation.

## Depth is where it stops

A self-join resolves **one** level. Employee to manager is one join. Employee to
manager's manager is two, written out by hand:

```
FROM employees e
JOIN employees m  ON e.manager_id = m.id
JOIN employees mm ON m.manager_id = mm.id
```

Three levels needs three, and an any depth can't be written this way at
all, because the number of joins would have to depend on the data.

That is the boundary where the technique runs out and
[recursive CTEs](recursive_ctes_in_sql.html) take over. A recursive CTE walks
down as many levels as exist. It's the correct tool the moment the depth is
not known in advance.

## Why the pair condition is not optional

The `a.id < b.id` line is easy to read past. It's worth seeing what its
lack does to the row count. Pairing a group against itself is a Cartesian
product within the group: `n` colleagues under one manager give `n &times; n`
sorted pairs before any rule trims them.

|colleagues under a manager|no condition (n&sup2;)|`a.id <> b.id`|`a.id < b.id`|
|---|---|---|---|
|5|25|20|10|
|10|100|90|45|
|50|2,500|2,450|1,225|

The middle column still counts each pair twice. Only `a.id < b.id` gives the
`n(n-1)/2` unordered pairs you meant. And the gap is quadratic, so on a manager
with fifty reports the wrong rule doesn't return a few extra rows &mdash; it
returns 2,500 where 1,225 were wanted, and any total found over them comes out
roughly doubled. That is why the idiom is worth recognising on sight rather than
rediscovering after a report reads twice what it should.

## A self-join reads the table twice

The other cost hides in the plan. A self-join names the table twice, so the engine
reads it twice, and if the join column is unindexed each read is a full scan with
a hash build in between. On `employees` self-joined on `manager_id`:

|`manager_id`|plan|
|---|---|
|indexed|SEARCH the second copy per row &mdash; a seek|
|unindexed|SCAN both copies, hash-join in memory|

On a hundred employees no one notices. On a hundred thousand, the unindexed
version builds a hash table of each row and probes it with each row &mdash; the
work grows with the square of the table where the indexed plan grows with its
logarithm. A hundred thousand employees joined without that index is on the order of ten
billion row checks. With it, a hundred thousand seeks of about seventeen
steps each &mdash; the difference between a query that returns and one that does
not. The index on the parent column that a foreign key would give you is on
the *referenced* side. The self-join reads the *referencing* column, which is the
one that often lacks an index. This is easy to miss until the table grows.

## Questions people ask

<strong>What is a self join?</strong> It is a join of a table to itself, using two different aliases so each copy can be referred to separately.

<strong>Why do I need aliases in a self join?</strong> Without aliases the column names are ambiguous, because both copies share the same names. Aliases such as e and m let you say which copy you mean.

<strong>How do I stop a self join pairing a row with itself?</strong> Add a condition such as a.id <> b.id. For unordered pairs use a.id < b.id, which also removes mirrored duplicates.

<strong>Why does the top of my hierarchy vanish from the result?</strong> An inner join drops rows with no match, and the top manager has no manager. Use a LEFT JOIN to keep them.

<strong>How many levels can a self join walk?</strong> One level per join. For a hierarchy of unknown depth, use a recursive CTE instead.

<strong>Are self joins slow?</strong> They are as fast as the join condition allows. Index the column you join on, such as manager_id, and they stay quick.

## Where it goes wrong

**Inner join on a nullable parent.** The root vanishes. This is the single most
common self-join bug.

**Losing the anti-self rule.** Without `a.id < b.id` each row pairs
with itself, and totals come out roughly double.

**Using one for any depth.** If the query has four copies of the same
table and someone is about to add a fifth, it wants to be recursive.

**Leaving the join column unindexed.** A self-join reads the table twice. On a
large table with no index on `manager_id`, that is two full scans and a hash in
between. Add the index before the table grows.
""",
    check=[
        {"q": "Why does an inner self-join drop the top of a hierarchy?",
         "options": ["The root has no id",
                     "The root's parent reference is NULL and NULL matches nothing",
                     "Inner joins skip the first row",
                     "The alias is missing"],
         "answer": 1,
         "why": "An inner join needs a match on both sides. The root's manager_id is NULL, so no row matches and it is dropped silently - LEFT JOIN keeps it with a NULL manager."},
        {"q": "Why is `a.id < b.id` preferred over `a.id <> b.id` when pairing rows?",
         "options": ["It is faster",
                     "It stops self-pairing and also returns each unordered pair once instead of twice",
                     "<> does not work on integers",
                     "It handles NULLs"],
         "answer": 1,
         "why": "<> removes self-pairs but still returns both (A, B) and (B, A). For two distinct rows exactly one ordering satisfies <, so each pair appears once."},
        {"q": "When does a self-join stop being the right tool?",
         "options": ["When the table is large",
                     "When the depth of the hierarchy is not known in advance",
                     "When the parent column is nullable",
                     "When more than two columns are selected"],
         "answer": 1,
         "why": "Each level costs one written join, so an unknown depth cannot be expressed. That is exactly what a recursive CTE is for."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Recursive CTEs
# ---------------------------------------------------------------------------
topic(
    "recursive_ctes_in_sql",
    "Recursive CTEs",
    "Querying",
    "A query that feeds its own output back in, one level at a time, until "
    "nothing new comes back.",
    _svg(_box(58, 18, 44, 16, fill=S) + _txt(80, 29, "anchor", A, 8)
         + _line(80, 34, 80, 44) + _box(58, 44, 44, 16, fill=S) + _txt(80, 55, "level 2", M, 8)
         + _line(80, 60, 80, 70) + _box(58, 70, 44, 16, fill=S) + _txt(80, 81, "level 3", M, 8)
         + '<path d="M104 52 q18 -14 0 -28" fill="none" stroke="%s" stroke-width="1.2"/>' % A),
    seed="""
CREATE TABLE employees (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    manager_id INTEGER REFERENCES employees(id)
);

INSERT INTO employees (id, name, manager_id) VALUES
    (1, 'Ada',     NULL),
    (2, 'Grace',   1),
    (3, 'Alan',    1),
    (4, 'Edsger',  2),
    (5, 'Barbara', 2),
    (6, 'Donald',  3),
    (7, 'Tony',    4),
    (8, 'Niklaus', 7);
""",
    starter="""WITH RECURSIVE chain(id, name, manager_id, level) AS (
    -- Anchor: where the walk starts.
    SELECT id, name, manager_id, 1
    FROM   employees
    WHERE  manager_id IS NULL

    UNION ALL

    -- Recursive step: everyone reporting to someone already found.
    SELECT e.id, e.name, e.manager_id, c.level + 1
    FROM   employees e
    JOIN   chain c ON e.manager_id = c.id
)
SELECT level, name FROM chain ORDER BY level, name;
""",
    variants_label="Walking a hierarchy",
    variants=[
        {"label": "Down from the top",
         "sql": """WITH RECURSIVE chain(id, name, manager_id, level) AS (
    SELECT id, name, manager_id, 1
    FROM   employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, c.level + 1
    FROM   employees e JOIN chain c ON e.manager_id = c.id
)
SELECT level, name FROM chain ORDER BY level, name;"""},
        {"label": "Up from one person",
         "sql": """-- The same machinery pointed the other way: start at Niklaus and
-- follow manager_id upwards until it runs out.
WITH RECURSIVE up(id, name, manager_id, step) AS (
    SELECT id, name, manager_id, 0
    FROM   employees WHERE name = 'Niklaus'
    UNION ALL
    SELECT m.id, m.name, m.manager_id, u.step + 1
    FROM   employees m JOIN up u ON u.manager_id = m.id
)
SELECT step, name FROM up ORDER BY step;"""},
        {"label": "With the full path",
         "sql": """-- Building a breadcrumb as you go is the usual reason to carry an
-- extra column through the recursion.
WITH RECURSIVE tree(id, name, path, level) AS (
    SELECT id, name, name, 1
    FROM   employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, t.path || ' > ' || e.name, t.level + 1
    FROM   employees e JOIN tree t ON e.manager_id = t.id
)
SELECT level, path FROM tree ORDER BY path;"""},
        {"label": "Counting, not walking",
         "sql": """-- No table involved. The recursion generates its own rows, which is
-- how you produce a series of dates or numbers without a helper table.
WITH RECURSIVE nums(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 10
)
SELECT n, n * n AS squared FROM nums;"""},
    ],
    notes=[
        "A recursive CTE has two halves joined by "
        "<code class='mono-font'>UNION ALL</code>: an anchor that runs once, and "
        "a step that runs against what the last round produced.",
        "It stops when the step returns no rows. Nothing else stops it.",
        "The step reads only the <em>previous</em> round's rows, not the whole "
        "accumulated set. That is what makes it a level-by-level walk.",
        "A cycle in the data means the step never comes back empty. Carry a "
        "depth column and cap it.",
    ],
    article="""
title: Recursive CTEs
intro: The one make in SQL that can follow a chain of unknown length.

## Why plain SQL cannot do this

A self-join resolves one level of a hierarchy. Two joins resolve two. To resolve
five you write five, and to resolve "but many there are" you can't write
any of it at all. The number of joins would have to depend on data the
query hasn't read yet.

A **recursive CTE** drops that limit. It runs a query, feeds the result back
into itself, and keeps going until a round makes nothing new.

## The two halves

```
WITH RECURSIVE chain(...) AS (
    <anchor>                -- runs once
    UNION ALL
    <recursive step>        -- runs repeatedly, reads `chain`
)
SELECT ... FROM chain;
```

The **anchor** is an plain query. It runs once and makes the starting
rows. In the first variant it selects the employee whose `manager_id` is NULL
&mdash; the root.

The **recursive step** is a query that refers to the CTE by name. It runs against
the rows the previous round made, not against all built up so far.
That gap is what makes the walk proceed one level at a time.

Run goes: anchor makes Ada. Step runs against {Ada} and makes Grace
and Alan. Step runs against {Grace, Alan} and makes Edsger, Barbara, Donald.
Step runs against those and makes Tony. Then Niklaus. Then the step finds
no one reporting to Niklaus, returns no rows, and the recursion halts.

**The empty result is the only stopping rule.** There's no iteration limit
and no depth check unless you write one.

## Carrying state through

The `level` column in the starter query isn't special syntax. It's an plain
column: the anchor sets it to 1. The step sets it to `c.level + 1`. any of it
found the same way rides along with the recursion.

The third variant builds a text path this way, concatenating each name onto the
one before to give `Ada > Grace > Edsger > Tony`. Sorting by that string
gives a right nested listing. This Is a small trick worth knowing: sorting
by path sorts a tree into doc order.

## Direction is just the join condition

Run the second variant. It starts at Niklaus and walks *up*, and the only thing
that changed is which side of the join rule is which:

```
down:  JOIN chain c ON e.manager_id = c.id
up:    JOIN up    u ON u.manager_id = m.id
```

Same make, opposite direction. Ancestors and descendants are the same
problem with the arrow reversed.

## Generating rows from nothing

The fourth variant has no table in it. The anchor is `SELECT 1` and the step
adds one until it reaches ten.

This is how you give a sequence without a helper table: a row per day across
a date range so a report shows zeros for days with no sales, a row per bucket
for a histogram, a numbers table for splitting strings. It's one of the most
handy uses and the one people find last.

## Cycles

All above assumes the data is a tree. If someone turns their own
manager's manager, the step never returns empty and the query runs until the
server stops it.

Real data acquires cycles. The defences, in growing order of strength:

- Carry a depth column and add `WHERE level < 50` to the step.
- Carry the path and add `WHERE instr(path, e.name) = 0` to refuse revisiting.
- Use `UNION` instead of `UNION ALL`. This Deduplicates &mdash; this stops a
  cycle but costs a check against the whole built up set each round.
- In PostgreSQL, use the `CYCLE` clause. This Does this properly.

A depth cap costs almost nothing and turns a hung query into a wrong-but-finite
answer, which is far easier to notice.

## Filling gaps: the row-per-day spine

The sequence trick earns its own worked case. It solves a problem each
reporting query hits: a `GROUP BY day` over a table with no sales on some days
simply has no row for those days. The chart skips them and a week with a
zero-sales Tuesday looks like a six-day week.

The fix is to make each day in the range and `LEFT JOIN` the data onto it:

```
WITH RECURSIVE days(d) AS (
    SELECT date('2026-01-01')
    UNION ALL
    SELECT date(d, '+1 day') FROM days WHERE d < '2026-01-31'
)
SELECT days.d, COALESCE(SUM(s.amount), 0) AS sales
FROM days LEFT JOIN sales s ON s.day = days.d
GROUP BY days.d;
```

The anchor is one date, the step adds a day until it reaches the end, and 31 rows
come out of no table at all. The `LEFT JOIN` then keeps each day, and
`COALESCE` turns the missing matches into zeros. A gap in the data turns a
visible zero rather than an invisible skip. The difference between a chart
that lies by omission and one that doesn't.

## What a cycle actually does

"Runs forever" understates it. With `UNION ALL` and a cycle, each round feeds the
next, and if the cycle doubles the frontier the row count explodes geometrically
before the server kills it:

|round|rows produced|
|---|---|
|1|1|
|5|16|
|10|512|
|20|524,288|

That isn't a slow query. It's a query trying to build a billion-row
mid from a handful of cyclic rows. A `WHERE level < 50` guard turns it
into a wrong-but-finite answer that returns at once and is obvious in the output,
which is far easier to notice than a link that simply never comes back.
`UNION` instead of `UNION ALL` stops it too, by deduplicating &mdash; but that
checks each new row against all found so far, each round, so on
acyclic data it makes a correct query needlessly quadratic. The depth cap costs
one int check per row. Reach for it first. A path-based guard. Refusing to revisit a name already on the built up
path &mdash; is stricter and costs a substring check per row, and it's the right
choice when the data is a graph rather than a tree and genuine repeats are
expected.

## Questions people ask

<strong>What are the two parts of a recursive CTE?</strong> An anchor query that supplies the starting rows, and a recursive query that refers to the CTE itself. They are joined with UNION or UNION ALL.

<strong>How does a recursive CTE know when to stop?</strong> It stops when the recursive part returns no new rows. If it never does, you need your own limit.

<strong>What causes infinite recursion?</strong> A cycle in the data, such as A pointing to B and B pointing to A. Track visited ids or add a depth limit.

<strong>Should I use UNION or UNION ALL in a recursive CTE?</strong> UNION ALL is faster. UNION removes duplicates each round, which can break cycles but costs more.

<strong>Can a recursive CTE generate rows from nothing?</strong> Yes. Start with a single row and add one each step, for example to build a row for every date in a range.

<strong>What is the difference between a recursive CTE and a self join?</strong> A self join walks a fixed number of levels. A recursive CTE repeats until there is nothing left, so it handles any depth.

## Where it goes wrong

**No termination guard.** Cyclic data plus `UNION ALL` runs forever.

**An anchor that matches too much.** If the anchor selects each row rather than
the roots, each row is a starting point and the result is huge.

**Expecting the step to see all found so far.** It sees the previous
round only. Aggregating across all levels has to happen in the outer query.

**Recursing over a large table without an index on the join column.** Each round
is a join. Without an index each round is a scan.
""",
    check=[
        {"q": "What stops a recursive CTE?",
         "options": ["A fixed iteration limit",
                     "The recursive step returning no rows",
                     "The anchor running out",
                     "A depth column reaching zero"],
         "answer": 1,
         "why": "Nothing else halts it. With cyclic data the step keeps producing rows forever, which is why a depth cap or a path check is worth adding."},
        {"q": "What does the recursive step read on each round?",
         "options": ["The whole accumulated result so far",
                     "Only the rows produced by the previous round",
                     "Only the anchor's rows",
                     "The base table only"],
         "answer": 1,
         "why": "That is exactly what makes it a level-by-level walk. Aggregating across all levels has to happen in the outer query instead."},
        {"q": "How do you turn a descendants query into an ancestors query?",
         "options": ["Add ORDER BY DESC",
                     "Swap which side of the join condition the CTE is on, and start from a different anchor",
                     "Use UNION instead of UNION ALL",
                     "It cannot be done"],
         "answer": 1,
         "why": "Ancestors and descendants are the same walk with the arrow reversed. The construct is unchanged; only the anchor and the join condition move."},
    ],
)


# ---------------------------------------------------------------------------
# 7. EXPLAIN and query plans
# ---------------------------------------------------------------------------
topic(
    "explain_and_query_plans",
    "EXPLAIN and Query Plans",
    "Performance",
    "Ask the database what it intends to do before blaming it for being slow. "
    "Add an index and watch the plan change.",
    _svg(_txt(80, 22, "EXPLAIN QUERY PLAN", A, 9)
         + _box(16, 32, 128, 18, fill=S) + _txt(80, 44, "SCAN orders", M, 8)
         + _txt(80, 60, "&#8594; add an index &#8594;", A, 8)
         + _box(16, 66, 128, 18, fill=S) + _txt(80, 78, "SEARCH orders USING INDEX", M, 8)),
    seed="""
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    status      TEXT NOT NULL,
    total       REAL NOT NULL
);

-- Enough rows that a scan and a seek are genuinely different work.
WITH RECURSIVE gen(n) AS (
    SELECT 1 UNION ALL SELECT n + 1 FROM gen WHERE n < 5000
)
INSERT INTO orders (id, customer_id, status, total)
SELECT n,
       (n * 7) % 400,
       CASE n % 3 WHEN 0 THEN 'paid' WHEN 1 THEN 'pending' ELSE 'shipped' END,
       (n % 97) + 1.5
FROM   gen;
""",
    starter="""-- No index on customer_id yet, so this has to look at every row.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 42;
""",
    variants_label="Watch the plan change",
    variants=[
        {"label": "1. Before the index",
         "sql": """EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 42;"""},
        {"label": "2. Create the index",
         "sql": """CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
SELECT 'index created - now run step 3' AS note;"""},
        {"label": "3. After the index",
         "sql": """-- SCAN has become SEARCH ... USING INDEX. That word is the whole
-- difference between reading 5000 rows and reading about 13.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 42;"""},
        {"label": "4. The index it cannot use",
         "sql": """-- Wrapping the column in a function hides it from the index.
-- Back to SCAN, on the same index, for a query that means the same thing.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id + 0 = 42;"""},
    ],
    notes=[
        "<code class='mono-font'>EXPLAIN</code> reports the plan the optimiser "
        "chose. It is the database's own account, not a guess.",
        "<code class='mono-font'>SCAN</code> means every row is read. "
        "<code class='mono-font'>SEARCH ... USING INDEX</code> means it jumped "
        "straight to the matching ones.",
        "The plan depends on statistics as well as indexes. On a tiny table a "
        "scan can genuinely be the better choice.",
        "An index on a column is invisible to a query that wraps that column in "
        "a function.",
    ],
    article="""
title: EXPLAIN and Query Plans
intro: The DB will tell you what it plans to do. Very few people ask.

## SQL says what, not how

A query states the result you want. It says nothing about how to get it: which
table to read first, whether to use an index, whether to sort or hash for a
join. All of that is chosen by the **query tuner**, at runtime, from the
statistics it holds about your data.

Which means that two queries returning the same results can differ by orders of
magnitude in cost, and nothing about the SQL text tells you which is which.
`EXPLAIN` is how you find out, and it takes about ten seconds.

## SCAN against SEARCH

Run the first variant. The plan reads:

```
SCAN orders
```

`SCAN` means the DB intends to read **each row** and test each one. Five
thousand rows here. Five million in production, at which point the query is a
problem.

Run the second variant to create an index on `customer_id`, then the third. The
plan now reads:

```
SEARCH orders USING INDEX idx_orders_customer (customer_id=?)
```

`SEARCH` means it can jump right to the matching rows. The query text didn't
change. The result doesn't change. The work changed from thousands of row reads
to a handful.

That contrast is the whole skill: **look for SCAN on a large table where you
expected a lookup.** Other engines use different words. PostgreSQL says
`Seq Scan` against `Index Scan`, MySQL fills in a `type` column with `ALL`
against `ref`. The gap is the same all over.

## The index it will not use

Run the fourth variant. The index still exists, the query means just the same
thing, and the plan is back to `SCAN`.

The difference is `customer_id + 0` instead of `customer_id`. An index stores
values of the column, in order. It doesn't store values of *expressions over*
the column, so the moment the column is wrapped in any of it, the sorting the
index gives no longer matches to what the query is asking about.

This is the most common way a good index goes unused, and it hides
inside plain-looking SQL.

| Written | Problem | Instead |
|---|---|---|
| `WHERE YEAR(created) = 2026` | function on the column | `WHERE created >= '2026-01-01' AND created < '2027-01-01'` |
| `WHERE LOWER(email) = ?` | function on the column | index on `LOWER(email)`, or store it folded |
| `WHERE id + 0 = 42` | arithmetic on the column | `WHERE id = 42` |
| `WHERE status LIKE '%paid'` | leading wildcard | no index can help; a B-tree is ordered by prefix |

The rule: **keep the indexed column bare on one side of the check.**

## A scan is not always wrong

On a table of fifty rows, reading all fifty is cheaper than consulting an index
and then fetching rows one at a time. Tuners know this and will right
skip an index on a small table.

The same applies to selectivity. A query matching 60% of the rows is often
better served by a scan. An index gives a list of row locations that
then have to be fetched on their own. And fetching most of the table one
row at a time costs more than reading it in order.

This is why plans change as tables grow. Why a query that was fast in staging
can be slow in production with the same schema and different statistics.

## Estimated against actual

`EXPLAIN` alone shows what the tuner *intends*, using row-count guesses.
Those guesses come from statistics that can be stale or simply wrong.

Most engines offer a form that runs the query and reports what really happened
&mdash; `EXPLAIN ANALYZE` in PostgreSQL, `EXPLAIN ANALYZE` in MySQL 8.0.18 and
later. Checking guessed rows against actual rows is the fastest way to find
out that the tuner expected 10 rows and got 400,000. This Is almost always
the reason a plan is bad.

Two habits follow: run `ANALYZE` after a bulk load so the statistics reflect the
data, and be suspicious of any plan step whose estimate is off by more than an
order of magnitude.

## What SCAN against SEARCH costs, in row reads

The `SCAN` / `SEARCH` gap is easy to nod at and worth turning into
numbers, because that is what makes it urgent on a growing table. `SCAN` reads
each row and tests it. `SEARCH` through a B-tree index descends a sorted
structure, so it does on the order of `log2(rows)` steps to reach the block it
wants:

|table size|`SCAN` reads|`SEARCH` (index steps)|
|---|---|---|
|5,000 rows|5,000|~13|
|5,000,000 rows|5,000,000|~23|

Two things follow. The gap isn't constant. It widens as the table grows,
because the scan is linear and the search is logarithmic. So The query that was
"fine in staging" on 5,000 rows is a thousandfold worse in production on five
million while the indexed version barely moved from 13 steps to 23. And it's why
`SCAN` on a large table where you expected a lookup is the single most valuable
thing to spot in a plan: it's the difference between reading a handful of pages
and reading the whole table.

## Why a scan can beat the index

"A scan isn't always wrong" deserves the reason, because it shows why the
tuner at times skips an index you built for it. An index gives a list of
row locations, which then have to be fetched one at a time &mdash; random access.
A scan reads the table in order. Sequential access. This Is far cheaper per
row. So there's a crossover in selectivity:

|query matches|index path|better plan|
|---|---|---|
|0.1% of rows|a few random fetches|**index**|
|60% of rows|0.6N random fetches|**scan**|

Fetching 60% of a table one row at a time through an index costs more than reading
the whole table sequentially and discarding 40%, because random reads dominate the
bill. This is why the tuner's choice depends on the *statistics*, not just the
SQL. A query that used the index in staging, against a few hundred
rows, can right switch to a scan in production against millions with a
different spread. The plan changing under you is the tuner doing its
job, not misbehaving.

## Questions people ask

<strong>What does EXPLAIN actually show?</strong> The plan the database intends to follow: which tables it reads, which indexes it uses, and in what order. It does not run the query unless you ask for ANALYZE.

<strong>What is the difference between SCAN and SEARCH?</strong> SCAN reads every row in the table. SEARCH uses an index to jump to matching rows.

<strong>Why is my index not being used?</strong> Common causes are a function wrapped around the column, a leading wildcard in LIKE, a mismatched type, or a filter that matches most of the table.

<strong>Is a table scan always bad?</strong> No. On a small table, or when you need most of the rows, a scan is cheaper than going through an index.

<strong>What is the difference between EXPLAIN and EXPLAIN ANALYZE?</strong> EXPLAIN shows estimates. EXPLAIN ANALYZE runs the query and shows actual row counts and timings, so you can spot bad estimates.

<strong>Why does the plan change when the data grows?</strong> The optimiser picks plans from table statistics. As row counts and value spread change, a different plan can become cheaper.

## Where it goes wrong

**Guessing instead of asking.** The plan is one command away and settles the
arg.

**Reading a plan for a query with no data.** Plans on an empty or tiny table
tell you nothing about production.

**Adding indexes until it's fast.** each index costs write time and space, and
an unused index costs both for nothing. Add the one the plan asks for, then
check the plan again.

**given the plan is stable.** It's recomputed as statistics change. Today's
plan isn't a ensure.
""",
    check=[
        {"q": "In a plan, what does SCAN tell you?",
         "options": ["The query failed",
                     "Every row will be read and tested",
                     "An index is being used",
                     "The table is sorted"],
         "answer": 1,
         "why": "SEARCH ... USING INDEX means it can jump straight to the matches. SCAN on a large table where you expected a lookup is the thing to look for."},
        {"q": "Why does `WHERE customer_id + 0 = 42` stop using an index on customer_id?",
         "options": ["Adding zero changes the value",
                     "The index stores column values, not values of expressions over the column",
                     "Arithmetic is not allowed in WHERE",
                     "The index needs rebuilding"],
         "answer": 1,
         "why": "The index's ordering is on the bare column. Wrap it in anything - a function, arithmetic, a cast - and that ordering no longer corresponds to what is being asked."},
        {"q": "When is a full scan the better plan?",
         "options": ["Never",
                     "On a small table, or when the query matches a large fraction of the rows",
                     "Only when no index exists",
                     "When the table is sorted"],
         "answer": 1,
         "why": "An index yields row locations that must then be fetched individually. Fetching most of a table one row at a time costs more than reading it in order."},
    ],
)


# ---------------------------------------------------------------------------
# 8. Composite and covering indexes
# ---------------------------------------------------------------------------
topic(
    "composite_and_covering_indexes",
    "Composite and Covering Indexes",
    "Performance",
    "Column order in a multi-column index decides which queries can use it. "
    "Watch one query take the index and an almost identical one refuse it.",
    _svg(_box(14, 26, 132, 16, fill=S)
         + _txt(80, 37, "INDEX (status, customer_id)", A, 8)
         + _txt(46, 58, "status = ?", M, 8) + _txt(46, 70, "usable", A, 8)
         + _txt(116, 58, "customer_id = ?", M, 8) + _txt(116, 70, "not usable", M, 8)),
    seed="""
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    status      TEXT NOT NULL,
    total       REAL NOT NULL
);

WITH RECURSIVE gen(n) AS (
    SELECT 1 UNION ALL SELECT n + 1 FROM gen WHERE n < 5000
)
INSERT INTO orders (id, customer_id, status, total)
SELECT n,
       (n * 7) % 400,
       CASE n % 3 WHEN 0 THEN 'paid' WHEN 1 THEN 'pending' ELSE 'shipped' END,
       (n % 97) + 1.5
FROM   gen;

CREATE INDEX idx_status_customer ON orders(status, customer_id);
""",
    starter="""-- The index is on (status, customer_id), in that order.
-- This query leads with status, so it can use it.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE status = 'paid' AND customer_id = 42;
""",
    variants_label="Which queries can use INDEX (status, customer_id)",
    variants=[
        {"label": "Both columns",
         "sql": """EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE status = 'paid' AND customer_id = 42;"""},
        {"label": "Leading column only",
         "sql": """-- Still usable. A prefix of the index is an index.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE status = 'paid';"""},
        {"label": "Second column only",
         "sql": """-- Not usable as a seek. The index is sorted by status first, so
-- rows for customer 42 are scattered across the whole of it.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 42;"""},
        {"label": "Covering: never touch the table",
         "sql": """-- Every column this query needs is in the index, so the plan says
-- COVERING INDEX and the table itself is never read.
EXPLAIN QUERY PLAN
SELECT status, customer_id FROM orders WHERE status = 'paid';"""},
    ],
    notes=[
        "A composite index is sorted by its first column, then by its second "
        "within each value of the first, and so on.",
        "That makes any <em>leading prefix</em> of the columns usable, and "
        "nothing else. <code class='mono-font'>(a, b)</code> serves "
        "<code class='mono-font'>a</code> and <code class='mono-font'>a, b</code> "
        "&mdash; never <code class='mono-font'>b</code> alone.",
        "A covering index contains every column the query needs, so the table "
        "is never visited at all.",
        "Two single-column indexes are not equivalent to one composite index "
        "over the same columns.",
    ],
    article="""
title: Composite and Covering Indexes
intro: Why column order decides which queries an index can serve. Why one query never touches the table.

## An index is a sorted copy

A single-column index is a sorted list of that column's values, each paired with
a pointer to its row. Sorted means the DB can binary-search it instead of
reading all.

A **composite index** on `(status, customer_id)` is a sorted list too, sorted by
`status` first and, within each status, by `customer_id`. That is the whole
mechanism, and each rule about composite indexes falls out of it.

Think of a phone book sorted by surname then first name. Finding everyone
called Hopper is easy. Finding Grace Hopper is easy. Finding everyone whose
first name is Grace isn't. The Graces are scattered throughout, one per
surname, and you'd have to read the lot.

## The leftmost prefix rule

Run the four variants in order and watch the plan.

**Both columns** &mdash; `SEARCH ... USING INDEX`. The index leads with `status`,
narrows to `customer_id` within it, and lands on the rows.

**Leading column only** &mdash; still `SEARCH`. All the `paid` rows are
contiguous, so the index finds the block and reads it. A prefix of the index is
itself a usable index.

**Second column only** &mdash; `SCAN`. This is the key one. The index
exists, `customer_id` is in it, and the query can't use it for a seek, because
rows for customer 42 are spread across each status value. There's no
contiguous block to find.

**Covering** &mdash; `USING COVERING INDEX`, discussed below.

So an index on `(a, b, c)` can serve queries filtering on `a`, on `a, b`, or on
`a, b, c`. It can't serve `b`, `c`, or `b, c`. **Leading prefixes only.**

## The ordering rule that follows

Given that, the column order in a composite index is a design choice, not a
detail. Two guidelines:

**Equality before range.** An index on `(status, created_at)` serves
`WHERE status = 'paid' AND created_at > ?` well: the equality picks a block and
the range narrows inside it. Reversed, the range comes first and all
after it's scattered, so only the range column is really used.

**Order for the queries you really run.** If most queries filter by customer
and only some also filter by status, lead with customer. Reading the workload is
the only way to decide.

## Covering indexes

The fourth variant selects only `status` and `customer_id` &mdash; both of which
are already stored in the index. The plan says `USING COVERING INDEX`, and the
table is never read at all.

This is worth understanding because of what an index most times costs. An plain
index lookup happens in two stages: find the entries in the index, then fetch
each matching row from the table. That second stage is random access, and
on a large table it dominates. Returning a thousand rows can mean a thousand
scattered reads.

A covering index drops the second stage fully. All the query needs is
already in the sorted structure it just searched.

Some engines let you add columns purely for coverage without making them part of
the sort key &mdash; PostgreSQL's `INCLUDE`, SQL Server's `INCLUDE`. That keeps
the index narrow where it matters for searching while still avoiding the table.

## Two indexes are not one index

A common mistake is to assume that indexes on `(a)` and `(b)` do the work of an
index on `(a, b)`.

They don't. Given both, a DB can search each apart and intersect the
row sets, which some engines will do. But that means two searches and a
merge, against one search on a composite index. It's materially worse, and for
`ORDER BY a, b` the separate indexes provide no handy sorting at all.

The reverse substitution does work: `(a, b)` covers all `(a)` alone would
have, so having both is often redundant.

## The cost side

Indexes aren't free. each one must be updated on each insert, update and
delete of an indexed column. So A table with eight indexes does roughly nine
units of write work instead of one. They take space, they take memory in cache
that data pages could have used, and an index no one queries costs all of that
for nothing.

The hands-on loop is: find the slow query, read its
[plan](explain_and_query_plans.html), add the one index the plan asks for, read
the plan again. Not: add indexes and hope.

## Why two single indexes are not one composite

The claim that `(a)` and `(b)` can't replace `(a, b)` is worth making concrete,
because it's where "but I indexed both columns" goes wrong. An index on
`(status, customer_id)` is sorted by status first. So `customer_id` values for any
one customer are scattered one per status &mdash; the phone-book-by-first-name
problem. That decides which queries get a seek:

|query|`(status, customer_id)`|
|---|---|
|`WHERE status = ? AND customer_id = ?`|SEARCH (both used)|
|`WHERE status = ?`|SEARCH (leading prefix)|
|`WHERE customer_id = ?`|**SCAN** (not a prefix)|

Given instead two separate indexes, `(status)` and `(customer_id)`, the engine can
search each and intersect the results. Two lookups and a merge, against one
lookup on the composite &mdash; and neither gives the sorting for
`ORDER BY status, customer_id`, so that still sorts. The composite is strictly
more capable for queries that lead with `status`. This Is why column order is a
design choice: it's chosen for the queries you really run, and it's the
leading column that a second query can borrow, never the trailing one.

## Questions people ask

<strong>What is the leftmost prefix rule?</strong> A composite index on (a, b, c) can serve queries filtering on a, on a and b, or on all three. It cannot efficiently serve a query filtering only on b.

<strong>Does column order in a composite index matter?</strong> Yes. Put equality filters first, then the range or sort column. The order decides which queries the index can help.

<strong>What is a covering index?</strong> An index that holds every column the query needs, so the database never reads the table rows. It is often shown as a covering index in the plan.

<strong>Are two single-column indexes the same as one composite index?</strong> No. The database can usually use only one of them well, while a composite index narrows on both columns together.

<strong>What is the cost of adding more indexes?</strong> Each index slows inserts, updates and deletes, and takes disk space. Add them for queries that run often.

<strong>Can a composite index help ORDER BY?</strong> Yes, if the index order matches the sort order after the equality columns, the database can read rows already sorted and skip the sort.

## Where it goes wrong

**Indexing each column apart.** costly on write, and none of them
serves a multi-column filter well.

**Putting the range column first.** All after it turns unusable.

**Losing the sort.** `ORDER BY` can use an index too, and a composite index
that matches the sorting drops the sort step fully.

**Leaving redundant indexes in place.** If `(a, b)` exists, `(a)` is almost
certainly dead weight. Drop it and reclaim the write cost.
""",
    check=[
        {"q": "An index on (status, customer_id) exists. Which query can use it for a seek?",
         "options": ["WHERE customer_id = 42",
                     "WHERE status = 'paid'",
                     "Neither",
                     "Only queries naming both columns"],
         "answer": 1,
         "why": "The index is sorted by status first, so all the 'paid' rows are contiguous. Rows for customer 42 are scattered across every status, so there is no block to find."},
        {"q": "What does a covering index avoid?",
         "options": ["The sort step",
                     "Fetching rows from the table, because every column needed is already in the index",
                     "Updating on insert",
                     "The index search itself"],
         "answer": 1,
         "why": "An ordinary lookup searches the index and then fetches each row from the table by random access, which usually dominates. A covering index removes that second stage."},
        {"q": "Why should equality columns come before range columns in a composite index?",
         "options": ["Equality is faster to compare",
                     "A range makes everything after it scattered, so only the range column is really used",
                     "Ranges cannot be indexed",
                     "It reduces index size"],
         "answer": 1,
         "why": "An equality narrows to a contiguous block that the next column is sorted within. Once a range opens up, the following columns are no longer in a single ordered run."},
    ],
)


# ---------------------------------------------------------------------------
# 9. Isolation levels
# ---------------------------------------------------------------------------
topic(
    "isolation_levels",
    "Isolation Levels",
    "Concurrency",
    "Two transactions, one schedule, four levels. Step through and watch the "
    "same read return different answers.",
    _svg(_txt(46, 22, "A", A, 10) + _txt(114, 22, "B", A, 10)
         + _line(46, 28, 46, 80, B, 1.2) + _line(114, 28, 114, 80, B, 1.2)
         + "".join(_box(30, 34 + i * 15, 32, 9, fill=S, sw=1) for i in range(3))
         + "".join(_box(98, 41 + i * 15, 32, 9, fill=S, sw=1) for i in range(2))
         + _txt(80, 88, "who sees what, and when", M, 7)),
    timeline={
        "a": "Transaction A (a report)",
        "b": "Transaction B (a payment)",
        "intro": "Pick an isolation level, then step through. The note under "
                 "each step says what A actually sees at that moment.",
        "levels": [
            {"label": "READ UNCOMMITTED", "value": "ru"},
            {"label": "READ COMMITTED", "value": "rc"},
            {"label": "REPEATABLE READ", "value": "rr"},
            {"label": "SERIALIZABLE", "value": "ser"},
        ],
        "steps": [
            {"who": "a", "sql": "BEGIN;",
             "says": {"*": "A opens a transaction. Nothing has been read yet."}},
            {"who": "a", "sql": "SELECT SUM(total) FROM orders;  -- 1000",
             "says": {"*": "A reads 1000. Under every level this first read is the same: it is the committed state of the database."}},
            {"who": "b", "sql": "BEGIN;",
             "says": {"*": "B opens its own transaction alongside A's."}},
            {"who": "b", "sql": "UPDATE orders SET total = total + 500 WHERE id = 1;",
             "says": {"*": "B has changed a row but has NOT committed. The change exists only inside B's transaction."}},
            {"who": "a", "sql": "SELECT SUM(total) FROM orders;",
             "says": {
                 "ru": "A reads 1500. This is a DIRTY READ: A can see a change B has not committed and may still roll back. No mainstream engine defaults to this.",
                 "rc": "A reads 1000. B's change is uncommitted, so A cannot see it. Dirty reads are prevented at this level and above.",
                 "rr": "A reads 1000, for two reasons now: the change is uncommitted, and A is pinned to the snapshot it started with.",
                 "ser": "A reads 1000. The engine is also tracking that A depends on these rows, which matters at the end."}},
            {"who": "b", "sql": "COMMIT;",
             "says": {"*": "B's change is now durable and visible to anything that starts afterwards. The question is whether A sees it."}},
            {"who": "a", "sql": "SELECT SUM(total) FROM orders;",
             "says": {
                 "ru": "A reads 1500.",
                 "rc": "A reads 1500. Its two reads inside one transaction disagree - this is a NON-REPEATABLE READ. Each statement sees the latest committed data.",
                 "rr": "A reads 1000, the same as before. A is pinned to the snapshot taken at its first read, so a committed change elsewhere cannot alter what it sees.",
                 "ser": "A reads 1000, same snapshot as REPEATABLE READ."}},
            {"who": "b", "sql": "INSERT INTO orders VALUES (99, 250); COMMIT;",
             "says": {"*": "B commits a brand new row. This is the case that separates REPEATABLE READ from SERIALIZABLE in the classical definitions."}},
            {"who": "a", "sql": "SELECT COUNT(*) FROM orders;",
             "says": {
                 "ru": "A sees the new row.",
                 "rc": "A sees the new row. Its count has changed mid-transaction.",
                 "rr": "In the SQL standard this is where a PHANTOM READ is permitted: rows matching a condition may appear. PostgreSQL's snapshot prevents it; MySQL's InnoDB uses gap locks to prevent it. The standard allows it, so portable code cannot assume either way.",
                 "ser": "A does not see it, and the engine has recorded a conflict between A and B. Whichever commits second may be rejected and told to retry."}},
            {"who": "a", "sql": "COMMIT;",
             "says": {
                 "ru": "A commits. Anything it decided was based on data that may never have been committed.",
                 "rc": "A commits. Its own reads were inconsistent with each other, and no error was raised.",
                 "rr": "A commits on a consistent snapshot of the moment it began.",
                 "ser": "A may get a serialization failure here instead of a commit. That is not a bug - it is the engine telling you to retry, which is the price of the guarantee."}},
        ],
    },
    notes=[
        "Isolation is a dial between correctness and concurrency. Higher levels "
        "forbid more anomalies and permit less parallelism.",
        "<strong>Dirty read</strong>: seeing uncommitted data. "
        "<strong>Non-repeatable read</strong>: the same row changing mid-"
        "transaction. <strong>Phantom</strong>: new rows appearing.",
        "Defaults differ. PostgreSQL and Oracle default to READ COMMITTED; "
        "MySQL's InnoDB defaults to REPEATABLE READ.",
        "SERIALIZABLE does not queue everything. It detects conflicts and asks "
        "you to retry &mdash; so code using it must handle that error.",
    ],
    article="""
title: Isolation Levels
intro: What one transaction is allowed to see while another is still running.

## The dial

The I in ACID is alone: the degree to which concurrent transactions are kept
from seeing each other's work in progress.

Perfect alone is easy to define. Run each transaction one after
another &mdash; and unacceptable because a DB serving one
transaction at a time serves almost no one. So the standard defines a dial with
four settings, given not by what they do but by which **outliers** they
permit.

Step through the timeline above at each of the four levels. The schedule never
changes. What A sees changes at nearly each step.

## The three anomalies

**Dirty read.** Transaction A reads a row that B has changed but not committed.
If B rolls back, A acted on data that never existed. Step 5 at READ UNCOMMITTED
shows this: A reads 1500 from a change that is still draft.

**Non-repeatable read.** A reads a row, B updates it and commits, A reads the
same row again and gets a different value. Step 7 at READ COMMITTED shows it: A
reads 1000 and then 1500 inside one transaction, with no error and no warning.

**Phantom read.** A runs a query, B inserts a row matching its rule and
commits, A runs the same query and gets an extra row. Step 9. The gap
from a non-repeatable read is that no row A saw has changed &mdash; a new one
has arrived.

## The four levels

| Level | Dirty | Non-repeatable | Phantom |
|---|---|---|---|
| READ UNCOMMITTED | allowed | allowed | allowed |
| READ COMMITTED | prevented | allowed | allowed |
| REPEATABLE READ | prevented | prevented | allowed by the standard |
| SERIALIZABLE | prevented | prevented | prevented |

**READ UNCOMMITTED** is unused. PostgreSQL accepts the syntax and
silently gives you READ COMMITTED instead, because its architecture has no way
to expose uncommitted data.

**READ COMMITTED** is the default in PostgreSQL, Oracle and SQL Server. Each
*statement* sees a fresh view of committed data. It's a sensible default and
the outlier it permits is real: two queries in one transaction can disagree, so
a report that reads the same table twice can give inside inconsistent
totals.

**REPEATABLE READ** pins the transaction to a snapshot taken at its first read.
All it sees is steady as of that moment, no matter what commits
elsewhere. It's MySQL InnoDB's default.

**SERIALIZABLE** ensures the result is equal to some serial order.
Modern setups achieve this without locking all, by tracking
which transactions read which rows and aborting one when a genuine conflict is
found.

## The thing about SERIALIZABLE that surprises people

It doesn't make your code wait. It makes your code **fail**.

At step 10 under SERIALIZABLE, A may get a serialization failure instead of a
good commit. That isn't a malfunction. It's how the ensure is
delivered. The engine allowed both transactions to proceed optimistically,
found afterwards that no serial order shows what happened, and rejected one.

So any code running at SERIALIZABLE must catch that error and retry the whole
transaction. Code that assumes commit succeeds will fail intermittently under
load, which is the worst kind of bug to diagnose.

## Where the standard stops helping

The standard defines levels by which outliers are *permitted*, not which are
blocked. An engine is free to prevent more than needed, and they do.

PostgreSQL's REPEATABLE READ uses a full snapshot and so blocks
phantoms, which the standard doesn't need. MySQL's InnoDB blocks them at
that level too, by a different mechanism (gap locks). So code that leans on
phantoms being blocked at REPEATABLE READ works on both and isn't portable by
the standard, and code that leans on phantoms *appearing* is wrong on both.

This is why "we use REPEATABLE READ" is an incomplete statement about a system's
action. The engine matters.

## Choosing

Most uses should stay on the engine's default and reach for a thing
stronger where a exact rule demands it. The pattern that most often
needs it's read-then-write: check a balance, then deduct from it. Between the
check and the write, another transaction can change the balance, and no
alone level below SERIALIZABLE stops that on its own.

The options are clear locking (`SELECT ... FOR UPDATE`) or letting the
DB enforce the rule with a constraint. This Needs no alone
thinking at all.

## The lost update the levels do not stop

The read-then-write hazard is best seen as one math. Two transactions both
withdraw 100 from an account holding 1,000, each reading before either writes:

|step|transaction A|transaction B|
|---|---|---|
|1|read balance = 1000|read balance = 1000|
|2|compute 1000 &minus; 100 = 900||
|3||compute 1000 &minus; 100 = 900|
|4|write 900||
|5||write 900|

Two withdrawals of 100 leave the balance at **900, not 800** &mdash; one
withdrawal has vanished. Nothing here is a dirty or non-repeatable read, so
READ COMMITTED and even REPEATABLE READ permit it: both transactions read
committed data and each is inside steady. Only SERIALIZABLE stops it on
its own, by aborting one at commit. Which is why this pattern needs either
that level with a retry, an clear `SELECT ... FOR UPDATE`, or a single
`UPDATE ... SET balance = balance - 100` that never reads into the use at
all. Thinking about alone is the hard way. Letting one statement do the
math is the safe one.

## READ UNCOMMITTED is often a no-op

One level on the dial often does nothing, and given or else is a portable
source of confusion. `READ UNCOMMITTED` is meant to permit dirty reads &mdash;
seeing another transaction's uncommitted changes &mdash; but a
[snapshot-based](mvcc_in_databases.html) engine has no uncommitted version to
show. PostgreSQL accepts the syntax and silently gives you `READ COMMITTED`
instead:

|engine|`SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED`|
|---|---|
|PostgreSQL|accepted, runs as READ COMMITTED|
|MySQL InnoDB|honoured; dirty reads are possible|

So the same statement means two different things on two DBs, and a
"speed" alone level chosen on one has no effect on the other. This is a
given case of the general rule already stated. The standard names the
outliers a level *permits*, and an engine may prevent more &mdash; and it's why
the level a system runs at is a fact about the engine as much as about the
`SET` statement.

## Questions people ask

<strong>What are the four standard isolation levels?</strong> READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ and SERIALIZABLE. Each one blocks more anomalies than the one before.

<strong>What is a dirty read?</strong> Reading data another transaction has written but not yet committed. If that transaction rolls back, you acted on data that never existed.

<strong>What is the difference between a non-repeatable read and a phantom?</strong> A non-repeatable read sees an existing row change between two reads. A phantom sees new rows appear that match your filter.

<strong>Which isolation level should I use by default?</strong> READ COMMITTED is the default in PostgreSQL and many others, and it is fine for most work. Raise it only where a specific anomaly would hurt.

<strong>Does SERIALIZABLE mean transactions run one at a time?</strong> No. It means the result is the same as if they had, but the database may run them together and abort one with a serialization error. Your code must retry.

<strong>Do isolation levels prevent lost updates?</strong> Not always. A read-then-write pattern can lose updates even under READ COMMITTED. Use SELECT FOR UPDATE, an atomic UPDATE, or a version column.

## Where it goes wrong

**given a default.** They differ between engines, and code written against
one silently changes action on the other.

**Using SERIALIZABLE without retry logic.** Intermittent failures under load.

**Long-running read transactions.** A snapshot held open forces the engine to
retain old row versions. This Bloats storage and slows all.

**Thinking about alone instead of using a constraint.** A `UNIQUE`
constraint settles "no two of these" even so of what any transaction sees.
""",
    check=[
        {"q": "What is a non-repeatable read?",
         "options": ["Reading uncommitted data",
                     "Reading the same row twice in one transaction and getting different values",
                     "A new row appearing between two queries",
                     "A transaction being rolled back"],
         "answer": 1,
         "why": "It is permitted at READ COMMITTED, where each statement sees the latest committed data - so a report reading a table twice can produce internally inconsistent totals."},
        {"q": "How does SERIALIZABLE typically deliver its guarantee in a modern engine?",
         "options": ["By running transactions one at a time",
                     "By detecting conflicts and aborting a transaction, which the application must retry",
                     "By locking every table it touches",
                     "By disabling concurrent writes"],
         "answer": 1,
         "why": "It lets transactions proceed optimistically and rejects one when no serial order explains the outcome. Code that assumes commit always succeeds fails intermittently under load."},
        {"q": "Why is 'we use REPEATABLE READ' an incomplete description of behaviour?",
         "options": ["The level does not exist in all engines",
                     "The standard permits phantoms there, but PostgreSQL and MySQL each prevent them by different mechanisms",
                     "It is the same as SERIALIZABLE",
                     "It only applies to reads"],
         "answer": 1,
         "why": "The standard says which anomalies are permitted, not which are prevented, and engines prevent more than required in different ways. The engine matters as much as the level."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Deadlocks
# ---------------------------------------------------------------------------
topic(
    "deadlocks_in_sql",
    "Deadlocks",
    "Concurrency",
    "Two transactions taking the same two locks in opposite orders. Step "
    "through it and watch the cycle close.",
    _svg(_box(20, 28, 40, 20, fill=S) + _txt(40, 41, "A", A, 10)
         + _box(100, 28, 40, 20, fill=S) + _txt(120, 41, "B", A, 10)
         + '<path d="M60 34 h40" stroke="%s" stroke-width="1.4" fill="none"/>' % A
         + '<path d="M100 44 h-40" stroke="%s" stroke-width="1.4" fill="none"/>' % A
         + _txt(80, 70, "each waits on the other", M, 8)),
    timeline={
        "a": "Transaction A",
        "b": "Transaction B",
        "intro": "Two transactions updating the same two rows. Step through and "
                 "watch which statement blocks.",
        "levels": [
            {"label": "Opposite order (deadlocks)", "value": "bad"},
            {"label": "Same order (safe)", "value": "good"},
        ],
        "steps": [
            {"who": "a", "sql": "BEGIN;",
             "says": {"*": "A starts."}},
            {"who": "b", "sql": "BEGIN;",
             "says": {"*": "B starts, concurrently."}},
            {"who": "a", "sql": "UPDATE accounts SET bal = bal - 100 WHERE id = 1;",
             "says": {"*": "A now holds an exclusive lock on row 1. It keeps it until it commits or rolls back - locks are never released early."}},
            {"who": "b", "sql": "UPDATE accounts SET bal = bal - 50 WHERE id = 2;",
             "says": {
                 "bad": "B locks row 2. So far nothing is wrong: two transactions holding different rows is ordinary concurrency.",
                 "good": "B wants row 1 as well, but under the same-order discipline it asks for row 1 first - and A already holds it. B blocks here, harmlessly."}},
            {"who": "a", "sql": "UPDATE accounts SET bal = bal + 100 WHERE id = 2;",
             "says": {
                 "bad": "A needs row 2, which B holds. A blocks and waits for B to finish.",
                 "good": "A proceeds. It holds both locks, because nobody could overtake it."}},
            {"who": "b", "sql": "UPDATE accounts SET bal = bal + 50 WHERE id = 1;",
             "says": {
                 "bad": "B needs row 1, which A holds. Now A waits on B and B waits on A. The wait-for graph has a cycle, and neither will ever proceed.",
                 "good": "Still blocked, waiting for A. This is a wait, not a deadlock: A is running and will finish."}},
            {"who": "a", "sql": "COMMIT;",
             "says": {
                 "bad": "This never runs. The engine's deadlock detector has already found the cycle and killed one of the two - typically the one that has done less work - with a deadlock error.",
                 "good": "A commits and releases both locks. B unblocks immediately and carries on."}},
            {"who": "b", "sql": "COMMIT;",
             "says": {
                 "bad": "The survivor commits. The victim got an error and must retry its whole transaction from the beginning.",
                 "good": "B commits. Both transactions succeeded, one after the other, with no error and no lost work."}},
        ],
    },
    notes=[
        "A deadlock is a cycle in the wait-for graph: A waits on B, B waits on "
        "A. Waiting alone is not a deadlock.",
        "Locks are held until the transaction ends. There is no way to release "
        "one early.",
        "The database detects the cycle and kills one transaction. It cannot "
        "avoid the cycle for you.",
        "The fix is discipline, not configuration: always take locks in the "
        "same order, everywhere.",
    ],
    article="""
title: Deadlocks
intro: Two transactions, two rows, and the one detail that decides whether they finish.

## Waiting is normal; a cycle is not

When a transaction updates a row it takes an exclusive lock and holds it until
it commits or rolls back. any of it else wanting that row waits.

Waiting is plain and self-resolving: the holder finishes, the waiter
proceeds. A **deadlock** is different. It's a *cycle* in who is waiting for
whom, and a cycle can't resolve itself, because each participant is waiting
for another participant that will never move.

Step through the timeline with "opposite order" selected. Nothing is wrong at
step 4 &mdash; two transactions holding different rows is just concurrency. The
problem appears at step 6, when the second edge closes the loop: A holds row 1
and wants row 2. B holds row 2 and wants row 1. Neither can proceed and neither
will give up what it has.

## The database will break it, badly

Engines run a deadlock finder that now and then looks for cycles in the
wait-for graph. When it finds one it picks a **victim** &mdash; often the
transaction that has done the least work. So The least is lost &mdash; and kills
it with a deadlock error. The survivor continues.

That detail is needed and it isn't a fix. The victim's work is gone. If
the use doesn't catch the error and retry, a user's action simply
failed, and it failed intermittently, under load, in a way that is very hard to
copy.

## The fix is ordering

Switch the timeline to "same order" and step through again. The schedule is
almost the same. The only change is that B asks for row 1 before row 2, just
as A does.

Now B blocks at step 4 and stays blocked. A proceeds, finishes and releases both
locks. B unblocks and ends. Both transactions succeed, no error is raised,
and nothing is retried.

This is the whole technique: **acquire locks in a steady order all over in
the use.** A cycle needs two transactions to disagree about the order,
so if no one disagrees, no cycle can form. Sorting by main key is the usual
choice because it's total, any and easy to apply mechanically.

The classic case is a transfer between two accounts. Written naively it locks
the source then the destination, and two transfers in opposite directions
deadlock right away. Written as "lock the lower id first, then the higher" they
queue instead.

## What makes it more likely

**Long transactions.** Locks are held to the end. So The longer a transaction
runs the wider the window in which someone can interleave with it. Don't open a
transaction and then call an external API inside it.

**Broad locks.** A statement without an index may lock far more rows than it
needs, because rows it checks and rejects can still be locked. Adding the index
narrows the query and the locking together. This Is why an index at times
fixes a deadlock no one thought was an index problem.

**Escalation.** Some engines convert many row locks into one table lock past a
threshold, turning a narrow conflict into a broad one.

**Mixed access patterns.** Different code paths touching the same tables in
different orders is the underlying cause of most production deadlocks, and it
tends to appear when two features written months apart meet under load.

## Retry properly

Even with good discipline, deadlocks happen. The handling is a small amount of
code and it has to be right:

1. Catch the deadlock error in detail, not each error.
2. Retry the **whole transaction** from the beginning. Re-running the failed
   statement alone is wrong &mdash; the transaction was rolled back fully.
3. Back off before retrying, with some noise, so two victims don't
   collide again on the same schedule.
4. Cap the attempts and log what happened. So A genuine design problem doesn't
   hide behind a retry loop that quietly succeeds on the fourth attempt.

## The transfer, in both lock orders

The fix is one worked example away. Two transfers run at once &mdash; A moves money
from account 1 to 2, B from account 2 to 1. And the only thing that differs
is the order each takes its locks.

|step|naive (lock source first)|ordered (lock lower id first)|
|---|---|---|
|1|A locks 1|A locks 1|
|2|B locks 2|B waits for 1|
|3|A wants 2 &rarr; **blocked**|A locks 2, works, commits|
|4|B wants 1 &rarr; **deadlock**|B proceeds, commits|

Naively, A holds 1 and wants 2 while B holds 2 and wants 1. A cycle, and the
finder kills one of them. Sorted by account id, B simply waits at step 2 for a
lock A already holds, A finishes, and B continues. Same two transfers, same rows,
no error &mdash; because a cycle needs the two to disagree about order, and
"always lock the lower id first" drops the disagreement. That is the entire
technique, and it's code discipline, not a DB setting.

## Retry with backoff, not in lockstep

The retry after a deadlock has one detail that decides whether it helps: the wait
before retrying must be *randomised*. Both victims of a deadlock were doing similar
work also, so if both retry right away. Or both after just
100 ms &mdash; they collide again on the same schedule, and again after that:

|retry strategy|outcome under contention|
|---|---|
|immediate|the two collide again at once|
|fixed delay|they collide again after the delay|
|exponential backoff with jitter|the two drift apart and one wins|

Exponential backoff spreads successive attempts (100 ms, 200 ms, 400 ms), and the
jitter &mdash; a random fraction added to each &mdash; breaks the symmetry so the
two transactions stop arriving together. Without the noise a deadlock can
become a livelock: no cycle in the wait graph. But Two transactions retrying in
step and failing each other forever. The fix for a deadlock and the fix for the
retry storm it can cause are different, and both are needed.

## Questions people ask

<strong>What is a deadlock?</strong> Two or more transactions each hold a lock the other needs, so none can proceed. The database detects the cycle and aborts one.

<strong>Is a deadlock the same as a slow lock wait?</strong> No. A wait ends when the holder commits. A deadlock is a cycle that can never resolve without intervention.

<strong>How do I prevent deadlocks?</strong> Make every transaction take locks in the same order, keep transactions short, and avoid waiting on user input while holding locks.

<strong>What should my code do after a deadlock error?</strong> Roll back and retry the whole transaction, ideally with a short random delay so the two sides do not collide again.

<strong>Which transaction does the database kill?</strong> Usually the one that is cheapest to roll back, though the rule differs between engines. You cannot rely on being the survivor.

<strong>Can an index help avoid deadlocks?</strong> Yes. Without a good index, a statement may lock many more rows than it needs, which raises the chance of overlap.

## Where it goes wrong

**Treating it as a DB configuration problem.** No setting blocks
deadlocks. The order in which your code takes locks does.

**Retrying the statement instead of the transaction.** The rollback undid
all, so the retry starts from a state that no longer exists.

**given reads are safe.** `SELECT ... FOR UPDATE` takes locks and
participates in cycles just like an update.

**Silently swallowing the retry.** A rising deadlock rate is a signal about the
system's design. Log it.
""",
    check=[
        {"q": "What distinguishes a deadlock from ordinary lock waiting?",
         "options": ["The number of rows involved",
                     "A cycle - each transaction waits for another that is itself waiting",
                     "The isolation level",
                     "How long the wait lasts"],
         "answer": 1,
         "why": "Ordinary waiting resolves itself when the holder commits. A cycle cannot, because every participant is blocked on another participant that will never move."},
        {"q": "What is the reliable way to prevent deadlocks?",
         "options": ["Raise the lock timeout",
                     "Acquire locks in a consistent order everywhere in the application",
                     "Use a lower isolation level",
                     "Add more indexes"],
         "answer": 1,
         "why": "A cycle requires two transactions to disagree about the order. Ordering by primary key is the usual choice because it is total and can be applied mechanically."},
        {"q": "After a deadlock error, what must the application retry?",
         "options": ["The failed statement",
                     "The whole transaction from the beginning",
                     "Nothing, the engine retries it",
                     "The connection"],
         "answer": 1,
         "why": "The victim's transaction was rolled back entirely, so re-running one statement starts from a state that no longer exists."},
    ],
)

# ---------------------------------------------------------------------------
# 11. MVCC
# ---------------------------------------------------------------------------
topic(
    "mvcc_in_databases",
    "MVCC: How Readers Avoid Blocking Writers",
    "Concurrency",
    "Keep the old version of a row alongside the new one, and a reader never "
    "has to wait for a writer.",
    _svg(_box(14, 22, 44, 20, fill=S) + _txt(36, 36, "v1", M, 8)
         + _box(14, 48, 44, 20, fill=S, stroke=A) + _txt(36, 62, "v2", A, 8)
         + _line(64, 44, 88, 44, B, 1.2)
         + _txt(112, 34, "reader sees v1", M, 7)
         + _txt(112, 54, "writer made v2", M, 7)),
    [
        "A write does not overwrite. It writes a new version of the row and "
        "leaves the old one for whoever is still reading it.",
        "Each transaction gets a snapshot: a rule for which versions it is "
        "allowed to see, fixed at the moment it started.",
        "Readers never block writers and writers never block readers. Two "
        "writers to the <em>same row</em> still conflict.",
        "The cost is garbage: dead versions accumulate and something has to "
        "clean them up. In PostgreSQL that is <code class='mono-font'>VACUUM</code>.",
    ],
    """
title: MVCC: How Readers Avoid Blocking Writers
intro: The idea that lets a long report run while the DB keeps taking writes.

## The problem with locks

The simple way to keep transactions from interfering is locking: a reader takes
a shared lock, a writer takes an exclusive one. The two can't be held at
once.

It's correct, and on a busy system it's miserable. A report that scans a large
table holds read locks for its whole run. So Each write to that table waits.
Meanwhile a long write transaction blocks each reader. The DB spends its
time queueing rather than working, and the symptom is an use that is fast
until it's inexplicably not.

## Versions instead of locks

**Multi-version concurrency control** drops the conflict by refusing to destroy
any of it. A write doesn't overwrite a row. It creates a *new version* of it, and
the old version stays until no one can still need it.

each transaction is given a **snapshot**. In effect a rule saying which
versions count as visible &mdash; fixed at the moment it starts, or at the moment
each statement starts, based on the
[alone level](isolation_levels.html).

A reader that began before a write simply continues to see the older version.
Nothing waits.

## What each version carries

Conceptually each row version records which transaction created it and which
transaction deleted it:

```
id  | balance | created_by | deleted_by
----+---------+------------+-----------
7   |   1000  |    100     |    142
7   |    850  |    142     |    NULL
```

Transaction 142 changed the balance. It didn't edit the first line. It marked it
deleted and appended the second. A transaction with a snapshot older than 142 is
shown the first version, a newer one the second. Visibility turns an math
check of transaction ids rather than a queue.

## What MVCC does not solve

This is the part that gets missed. MVCC removes reader/writer conflicts. It
does **not** remove writer/writer conflicts.

Two transactions updating the same row still contend: the second must wait for
the first to commit or roll back. They would or else both give a new
version from the same old one and one update would vanish. That is the
[lost update](isolation_levels.html) problem, and MVCC's answer to it's either a
lock on that row or a serialisation failure at commit.

So the rule is: **readers never wait, writers to the same row still do.**

## The cost: garbage

Old versions build up. a thing has to decide when a version can no longer be
seen by any live snapshot and reclaim the space.

In PostgreSQL that job is `VACUUM`, often run by autovacuum. When it can't
keep up &mdash; often because a very old transaction is still open and
pinning each version created since. Tables **bloat**: the row count is
unchanged while the file grows, and each scan reads more pages for the same
data.

The hands-on consequence is worth stating plainly: **a transaction left open
does damage even when it's doing nothing**, because it holds back cleanup for
the whole DB. An idle-in-transaction link is a bug, not a small
waste.

Different engines pay this differently. PostgreSQL keeps old versions in the
table itself and vacuums them. MySQL's InnoDB keeps them in a separate undo log
and purges it. Oracle uses undo segments, and the same open-transaction problem
appears as `ORA-01555 snapshot too old`. The old version needed was
already discarded.

## What an open transaction actually costs

"Does damage even when it's doing nothing" is measurable. A snapshot can't be
released while any transaction that might still need it's open, so each row
version superseded *after* that transaction began has to be kept.

Picture a table taking a steady 1,000 updates a second. Each update leaves a dead
version behind. A reporting transaction that opens and then sits idle &mdash; a
link returned to a pool without a commit, a debugger stopped at a
breakpoint &mdash; pins cleanup for if it stays open:

|idle for|dead versions pinned|
|---|---|
|1 minute|60,000|
|10 minutes|600,000|
|1 hour|3,600,000|

The live row count never moved. But the table now holds millions of dead
versions the vacuum can't touch, each scan reads the pages they sit on, and the
file keeps growing. One forgotten transaction, doing nothing, taxes each query
against that table until it's closed. Which is why "idle in transaction"
is a state worth alerting on, not just avoiding.

## Visibility is one comparison

The claim that visibility turns math rather than a queue is worth making
literal, because it's why reads never wait. A version is visible to a snapshot
`S` just when `created_by <= S AND (deleted_by IS NULL OR deleted_by > S)`.
Take the two versions from earlier. V1 created by 100 and deleted by 142,
v2 created by 142 and still live:

|snapshot|v1 (100&ndash;142)|v2 (142&ndash;)|sees|
|---|---|---|---|
|120|100&le;120 and 142&gt;120 &rarr; **yes**|142&le;120 &rarr; no|v1, balance 1000|
|150|142&gt;150 is false &rarr; no|142&le;150 and live &rarr; **yes**|v2, balance 850|

No lock is consulted and nothing blocks. Each reader checks transaction ids and
picks its version. A snapshot of 120 keeps seeing 1000 no matter how many times
142 commits, because the numbers don't change once fixed. That is the entire
mechanism by which a long report runs undisturbed beside a stream of writes. It's also why the visible version is found without a scan of the history: the
engine keeps versions chained newest-first and walks until the check first
succeeds, which for a recently-read row is often the very first link.

## Questions people ask

<strong>What does MVCC stand for?</strong> Multi-Version Concurrency Control. The database keeps several versions of a row so readers and writers do not block each other.

<strong>Do readers block writers under MVCC?</strong> No. Readers see a snapshot of older versions while writers create new ones, so neither waits for the other.

<strong>Does MVCC remove the need for locks?</strong> No. Two writers changing the same row still conflict, and the second one waits or fails.

<strong>What is VACUUM and why does PostgreSQL need it?</strong> Old row versions pile up after updates and deletes. VACUUM reclaims their space once no transaction can still see them.

<strong>Why can a long-running transaction cause table bloat?</strong> It holds an old snapshot, so the database cannot discard any version that snapshot might need.

<strong>How does a transaction decide which version it can see?</strong> Each version records which transaction created and removed it. A transaction sees the versions committed before its snapshot was taken.

## Where it goes wrong

**Long-running transactions.** They pin versions across the entire DB.
Keep them short, and never leave one open across a user interplay.

**given no waiting at all.** Writers to the same row still contend, and the
error surfaces as a lock wait or a serialisation failure.

**Treating table bloat as a disk problem.** It's a symptom of vacuum not
keeping up, and adding disk hides it rather than fixing it.

**Counting rows to check for bloat.** The row count is right. The file size is
the thing that grew. Compare `pg_total_relation_size` before and after vacuum to
see whether the cleanup actually freed space.
""",
    [
        {"q": "What does a write do under MVCC?",
         "options": ["Overwrites the row in place and takes a lock",
                     "Creates a new version, leaving the old one for transactions still reading it",
                     "Blocks all readers until it commits",
                     "Copies the whole table"],
         "answer": 1,
         "why": "Nothing is destroyed while a live snapshot might still need it, which is exactly why a reader that began earlier never has to wait."},
        {"q": "Which conflict does MVCC NOT remove?",
         "options": ["Reader against writer", "Writer against reader",
                     "Two writers updating the same row", "Two readers"],
         "answer": 2,
         "why": "Both would produce a new version from the same old one and one update would be lost. The second waits, or fails at commit with a serialisation error."},
        {"q": "Why does an idle-in-transaction connection cause table bloat?",
         "options": ["It holds an exclusive lock",
                     "Its snapshot pins every version created since it began, so cleanup cannot reclaim them",
                     "It writes new versions continuously",
                     "It disables autovacuum"],
         "answer": 1,
         "why": "Vacuum can only reclaim a version no live snapshot can still see. One old open transaction holds back cleanup for the whole database."},
    ],
    timeline={
        "a": "Transaction A (a long report)",
        "b": "Transaction B (a payment)",
        "intro": "Step through and watch what A sees. Under MVCC it never waits, "
                 "and it never sees B's change - because A's snapshot predates it.",
        "levels": [
            {"value": "mvcc", "label": "MVCC (snapshot)"},
            {"value": "lock", "label": "Two-phase locking"},
        ],
        "steps": [
            {"who": "a", "sql": "BEGIN;",
             "says": {"mvcc": "A takes a snapshot. Everything committed before this instant is visible to A for its whole run.",
                      "lock": "A opens a transaction. No locks held yet."}},
            {"who": "a", "sql": "SELECT balance FROM accounts WHERE id = 7;  -- 1000",
             "says": {"mvcc": "A reads 1000. No lock is taken - MVCC reads do not lock.",
                      "lock": "A reads 1000 and takes a shared lock on row 7, which it will hold until commit."}},
            {"who": "b", "sql": "BEGIN;",
             "says": {"*": "B opens its own transaction."}},
            {"who": "b", "sql": "UPDATE accounts SET balance = 850 WHERE id = 7;",
             "says": {"mvcc": "B writes a NEW version of row 7. The old version stays, because A's snapshot still needs it. B does not wait.",
                      "lock": "B needs an exclusive lock, but A holds a shared lock on row 7. B BLOCKS here until A commits."}},
            {"who": "b", "sql": "COMMIT;",
             "says": {"mvcc": "B commits. The new version is now the current one for anyone starting after this point.",
                      "lock": "Still blocked. B cannot reach its COMMIT until A releases."}},
            {"who": "a", "sql": "SELECT balance FROM accounts WHERE id = 7;  -- ?",
             "says": {"mvcc": "A reads 1000 again - the old version. Its snapshot predates B's commit, so B's write is invisible to it. A is consistent with itself.",
                      "lock": "A reads 1000, because B has been waiting this whole time and has not written anything yet."}},
            {"who": "a", "sql": "COMMIT;",
             "says": {"mvcc": "A finishes. Now that no snapshot needs the old version of row 7, cleanup can reclaim it - VACUUM in PostgreSQL, purge in InnoDB.",
                      "lock": "A releases its locks. Only now can B proceed - it has been idle for the entire length of A's report."}},
        ],
    },
)


# ---------------------------------------------------------------------------
# 12. Partitioning
# ---------------------------------------------------------------------------
topic(
    "partitioning_in_databases",
    "Partitioning by Range and Hash",
    "Scale",
    "One logical table, several physical pieces. The query planner skips the "
    "pieces it can prove are irrelevant.",
    _svg(_box(12, 24, 40, 42, fill=S, stroke=A) + _txt(32, 78, "2024", M, 7)
         + _box(60, 24, 40, 42, fill=S) + _txt(80, 78, "2025", M, 7)
         + _box(108, 24, 40, 42, fill=S) + _txt(128, 78, "2026", M, 7)
         + _txt(80, 16, "one table, three files", M, 7)),
    [
        "Partitioning splits one table into pieces by a rule on a column. The "
        "table still looks like one table.",
        "<strong>Range</strong> partitions by an ordered value, usually a date. "
        "<strong>Hash</strong> spreads rows evenly by hashing a key.",
        "The win is <strong>partition pruning</strong>: a query with a predicate "
        "on the partition key touches only the partitions that can match.",
        "Dropping a partition is instant. Deleting the equivalent rows is not, "
        "which is why time-series data is almost always range-partitioned.",
    ],
    """
title: Partitioning by Range and Hash
intro: Cutting one table into pieces the planner can skip. The choice of where to cut.

## One table, several files

Splitting splits a table into physical pieces by a rule on one or more
columns. uses keep querying the single logical table. The engine decides
which pieces are involved.

This is **not** sharding. each split lives in the same DB on the same
server. [Sharding](sharding_in_databases.html) spreads data across separate
machines and is a much larger commitment.

The query above builds three range splits and a view that unions them, which
is the shape a split table has underneath. Run the variants to see what
each strategy costs.

## Range partitioning

Pick an sorted column &mdash; almost always a timestamp &mdash; and give each
split a bounded interval.

```
orders_2024  :  order_date >= '2024-01-01' AND < '2025-01-01'
orders_2025  :  order_date >= '2025-01-01' AND < '2026-01-01'
orders_2026  :  order_date >= '2026-01-01' AND < '2027-01-01'
```

A query with `WHERE order_date >= '2026-01-01'` can be proved to need only the
last split, so the engine reads one file instead of three. That proof is
**split pruning**, and it's where nearly all the gain is.

The second gain is admin and, for time-series data, often the bigger
one. Deleting a year of orders with `DELETE` writes a row version per deleted
row, makes huge WAL traffic, and leaves the table bloated. `DROP TABLE
orders_2024` unlinks a file. Retention policies are the standard reason to
split.

## Hash partitioning

Hash the key, take the remainder modulo the split count, and store the row
there. Rows spread evenly even so of what the values look like.

This is the right choice when there's no natural sorting to exploit and the
goal is to spread contention. Many concurrent writers hitting one hot
page, say.

The trade-off is that **hash splitting prunes only on equality**. A query for
one `customer_id` reaches one split. A query for a *range* of customer ids
reaches all of them, because hashing destroys order. Range splitting is the
opposite: it prunes ranges beautifully and can leave you with one very hot
split if recent data is where all the traffic goes.

| | Range | Hash |
|---|---|---|
| Prunes equality | yes | yes |
| Prunes ranges | yes | **no** |
| Even distribution | no | yes |
| Drop old data instantly | yes | no |
| Typical key | timestamp | id |

## Choosing the key

The split key must appear in the `WHERE` clause of the queries you care
about. This is the whole game, and it's where splitting schemes go wrong.

Split by `order_date` and then run reports by `customer_id`, and each report
reads each split &mdash; you've added cost and gained nothing. Worse
than nothing: each split has its own indexes. So A query that scans them all
does more index work than it would have on a single table.

A second constraint follows: a unique constraint has to include the split
key, because the engine can't cheaply enforce uniqueness across pieces it's
trying not to read.

## What pruning is worth, and what caps it

The payoff scales with how much the query skips, and that is just math.
Take 120 million orders over five years, split by month &mdash; 60
splits of two million rows each. A report over a single month, filtering on
the split key, prunes to one split:

|query| rows the engine must touch |fraction of the table|
|---|---|---|
|one month|2,000,000|1.7% (1/60)|
|one quarter|6,000,000|5.0% (3/60)|
|no partition-key filter|120,000,000|100%|

The single-month query does **60&times; less scanning**. And the number is
just the split count, because pruning reads one of 60 equal pieces. Finer
splits prune harder: weekly splits would make that same month prune to a
quarter of the rows again.

## Sizing

So why not split into thousands of tiny pieces? Because pruning saves scan
work and the planner spends it back. The planner tests each split when it
builds the plan, so planning cost grows roughly linearly with the split count
&mdash; a fixed cost paid on each query whether or not pruning helps it:

|partitions|rough planning overhead|
|---|---|
|60|small, negligible next to the scan|
|500|starting to matter for short queries|
|5,000|can exceed the query's own runtime|

For a lookup that executes in a couple of milliseconds, planning across thousands
of splits is the dominant cost, and the splitting has made the query
slower. That is the ceiling the two forces set between them: too few splits
and pruning barely helps. Too many and planning overwhelms the saving. a place
between a few dozen and a few hundred is the usual advice, and monthly splits
over a couple of years land on its own in that band.

Splits can also be **subpartitioned**. Range by month, then hash by
customer within each month &mdash; when both access patterns matter.

## Joins get a second, quieter benefit

Pruning is the gain everyone knows. The other one shows up when two tables are
split on the *same* key. Orders and order-items both by `customer_id`,
say. A row in bucket `i` of one table can only match rows in bucket `i` of the
other, so the engine performs a **split-wise join**: 60 small joins of
aligned buckets, rather than one join over the whole product.

The math is the same shape as pruning. With 60 buckets a side, matched
splitting means 60 aligned split-joins. Unmatched, any bucket of one table
could hold a match for any bucket of the other. This Is 60 &times; 60 = 3,600
split-pairs to consider. And each aligned join is small enough that its hash
table &mdash; two million rows, not 120 million &mdash; fits in memory instead of
spilling to disk. This is why data warehouses split fact and dim tables
on the join key: the join, not just the scan, gets cut into pieces the engine can
hold.

## Questions people ask

<strong>What is partitioning?</strong> Splitting one large table into smaller pieces, called partitions, that are stored separately but queried as one table.

<strong>What is the difference between range and hash partitioning?</strong> Range splits by value ranges such as dates. Hash spreads rows evenly using a hash of the key.

<strong>What is partition pruning?</strong> The planner skips partitions that cannot contain matching rows. It only works when the query filters on the partition key.

<strong>Is partitioning the same as sharding?</strong> No. Partitioning splits a table inside one database server. Sharding spreads data across several servers.

<strong>How do I choose a partition key?</strong> Pick the column most queries filter on, such as a date for time-series data. A poor choice leaves queries touching every partition.

<strong>Does partitioning always make queries faster?</strong> No. It helps when queries prune partitions or when old data is dropped by detaching a partition. Otherwise it adds overhead.

## Where it goes wrong

**Splitting a small table.** Under a few million rows, a good index is
simpler and often faster.

**A split key the queries don't filter on.** No pruning, more index
cost.

**Hash splitting then querying ranges.** each split, each time.

**Losing the default split.** A row that matches no split is an error
unless a catch-all exists, and a data-loading job that fails at midnight on New
Year's Day is the classic version of this.
""",
    [
        {"q": "What is partition pruning?",
         "options": ["Deleting old partitions automatically",
                     "The planner proving a query cannot match certain partitions and skipping them",
                     "Compressing partitions that are rarely read",
                     "Merging small partitions"],
         "answer": 1,
         "why": "It requires the partition key in the WHERE clause. Without it every partition is read, and the scheme costs more than it saves."},
        {"q": "Why can hash partitioning not prune a range query?",
         "options": ["Hashes are too slow",
                     "Hashing destroys order, so adjacent key values land in unrelated partitions",
                     "Ranges are not supported",
                     "It has too few partitions"],
         "answer": 1,
         "why": "That is the trade for even distribution. Range partitioning prunes ranges well but can leave one partition hot when recent data gets all the traffic."},
        {"q": "Why is time-series data almost always range-partitioned?",
         "options": ["Timestamps hash badly",
                     "Dropping an old partition is instant, while deleting the equivalent rows writes a version each and bloats the table",
                     "Range partitions compress better",
                     "Hash partitioning cannot use timestamps"],
         "answer": 1,
         "why": "Retention is usually the bigger win over pruning. DROP TABLE unlinks a file; DELETE generates enormous WAL traffic and leaves bloat behind."},
    ],
    seed="""CREATE TABLE orders_2024 (id INTEGER, order_date TEXT, customer_id INTEGER, total REAL);
CREATE TABLE orders_2025 (id INTEGER, order_date TEXT, customer_id INTEGER, total REAL);
CREATE TABLE orders_2026 (id INTEGER, order_date TEXT, customer_id INTEGER, total REAL);

INSERT INTO orders_2024 VALUES
  (1,'2024-03-11',101,120.0),(2,'2024-07-02',102,64.5),(3,'2024-11-19',101,310.0);
INSERT INTO orders_2025 VALUES
  (4,'2025-01-08',103,45.0),(5,'2025-06-23',101,220.0),(6,'2025-12-30',104,99.9);
INSERT INTO orders_2026 VALUES
  (7,'2026-02-14',102,150.0),(8,'2026-05-05',103,72.4),(9,'2026-08-01',101,410.0);

CREATE VIEW orders AS
  SELECT * FROM orders_2024
  UNION ALL SELECT * FROM orders_2025
  UNION ALL SELECT * FROM orders_2026;
""",
    starter="""-- The view is the logical table. Underneath are three partitions.
-- This query has a predicate on the partition key, so only one
-- partition can possibly match.
SELECT * FROM orders WHERE order_date >= '2026-01-01';
""",
    variants_label="Compare the access patterns",
    variants=[
        {"label": "Prunes to one partition",
         "sql": "-- order_date is the partition key, so 2024 and 2025 can be\n"
                "-- proved irrelevant. A real partitioned table reads one file.\n"
                "SELECT * FROM orders WHERE order_date >= '2026-01-01';"},
        {"label": "Prunes nothing",
         "sql": "-- customer_id is NOT the partition key. Every partition has to\n"
                "-- be read, and each has its own indexes to work through.\n"
                "SELECT * FROM orders WHERE customer_id = 101;"},
        {"label": "Reading one partition directly",
         "sql": "-- What pruning amounts to: touch one piece, ignore the rest.\n"
                "SELECT COUNT(*), SUM(total) FROM orders_2026;"},
        {"label": "Dropping a year",
         "sql": "-- Retention on a partitioned table. Instant, and it leaves no\n"
                "-- bloat behind. Compare with DELETE FROM orders WHERE ...\n"
                "DROP TABLE orders_2024;\n"
                "SELECT COUNT(*) AS rows_left FROM orders_2025;"},
    ],
)


# ---------------------------------------------------------------------------
# 13. Sharding
# ---------------------------------------------------------------------------
topic(
    "sharding_in_databases",
    "Sharding",
    "Scale",
    "Splitting one dataset across separate machines, and the queries that stop "
    "being possible once you do.",
    _svg(_box(10, 30, 34, 34, fill=S, stroke=A) + _txt(27, 76, "node 1", M, 7)
         + _box(58, 30, 34, 34, fill=S, stroke=A) + _txt(75, 76, "node 2", M, 7)
         + _box(106, 30, 34, 34, fill=S, stroke=A) + _txt(123, 76, "node 3", M, 7)
         + _txt(80, 20, "one dataset, three servers", M, 7)),
    [
        "Partitioning splits a table across files on one server. Sharding "
        "splits it across <em>servers</em>, each with its own copy of the engine.",
        "A <strong>shard key</strong> decides which server holds a row. Every "
        "query that names it goes to one node; every query that does not fans out.",
        "Joins across shards, global unique constraints and cross-shard "
        "transactions all become hard or impossible.",
        "Shard last. Indexes, read replicas, caching and partitioning are all "
        "cheaper and reversible; sharding is neither.",
    ],
    """
title: Sharding
intro: The last resort of scaling, what it buys. The four things it takes away.

## What it is

Sharding splits a dataset across free DB servers. Each **shard**
holds a subset of the rows and knows nothing about the others.

The gap from [splitting](partitioning_in_databases.html) is the
machine boundary, and it's the whole trouble. Splits share a query
planner, a transaction manager and a lock table. Shards share nothing, so
any of it that needed a global view has to be rebuilt in the use or given
up.

## The shard key

One column decides where a row lives. often the key is hashed and the remainder
taken modulo the shard count, so a routing rule might be
`shard = hash(customer_id) % 4`.

The query above finds just that for a set of customers, and the variants
show what different access patterns cost.

The consequence is stark and worth stating as a rule:

**A query that names the shard key touches one node. A query that doesn't
touches all of them.**

A lookup by `customer_id` is a single-node request and stays fast as the fleet
grows. A report grouped by `product_id` has to be sent to each shard and the
partial results merged &mdash; a *scatter-gather*, whose latency is the slowest
shard's, not the mean.

So the shard key isn't a schema detail. It's a choice about which queries
stay cheap forever and which never will, and it's extremely costly to change
afterwards.

## What you give up

**Cross-shard joins.** Customers on shard 1, orders on shard 3, and no engine can
join them. Either the join moves into the use, or related data is
on purpose placed together &mdash; sharding orders by `customer_id` so a
customer's orders live beside them.

**Global uniqueness.** `UNIQUE(email)` can't be enforced across free
servers. The usual answers are a separate lookup service that owns emails, or
making ids that are unique by build &mdash; UUIDs, or Snowflake-style
ids with a shard number embedded.

**Cross-shard transactions.** ACID stops at the shard boundary. Spanning shards
means two-phase commit, which is slow and adds a coordinator that can fail
mid-protocol, or sagas, which are eventually steady with clear
compensation. Most teams design so that transactions never span shards.

**`AUTO_INCREMENT`.** each shard would start at 1. Ids must come from elsewhere.

## Rebalancing

Adding a shard when the rule is `hash(key) % 4` changes it to `% 5`, and almost
each row's destination moves. Migrating the whole dataset while serving traffic
is the single worst part of operating a sharded system.

Two designs avoid it. **Steady hashing** places shards on a ring so adding
one moves only the keys in its arc, rather than reshuffling all.
**Virtual buckets** hash keys into a fixed large number of buckets &mdash; say
1024 &mdash; and map buckets to physical shards. Adding a shard moves a few
buckets and the hash rule never changes. The bucket approach is what most modern
systems use, because moving is then a matter of copying a bucket and updating a
map.

## Do the cheaper things first

Sharding is close to irreversible and touches each part of the use.
Before it:

1. **Index properly.** A great many "we need to shard" conversations end at a
   missing [composite index](composite_and_covering_indexes.html).
2. **Read replicas**, if reads dominate. Cheap, and reversible.
3. **Caching**, for the hot small set.
4. **Splitting**, if one table is the problem.
5. **A bigger machine.** Unglamorous, and modern hardware goes a very long way.

Shard when writes exceed what one machine can take, or the working set no longer
fits in memory anywhere, and not before.

## Why naive rebalancing is the nightmare

"Almost each row's destination moves" isn't hyperbole, and the number is the
reason steady hashing and virtual buckets exist. With the rule
`hash(key) % N`, adding one shard changes the divisor, and a key moves when
`hash % N` differs from `hash % (N+1)`. Which is almost always:

|change|keys that must move|
|---|---|
|`% 4` &rarr; `% 5`|~80%|
|`% 100` &rarr; `% 101`|~99%|

Measured over two hundred thousand random keys, the `% 4` to `% 5` change relocated
79.8% of them, and it only gets worse as the fleet grows. Steady hashing and
virtual buckets bring that down to roughly `1/(N+1)`. About 20% and 1% for
the two rows above &mdash; because a new shard takes a slice from its neighbours
instead of forcing each key to recompute against a new divisor. Moving 1% of the
data to add a machine is an afternoon. Moving 99% while serving traffic is the
project everyone dreads.

## The slowest shard sets the latency

"Scatter-gather latency is the slowest shard's, not the mean" is a statement
about tail chance, and the math is unforgiving. If each shard answers
within its target 99% of the time, a query that must wait for *all* of them is
fast only if *each* shard was fast. And that chance falls as the
fan-out grows:

|shards in the fan-out|each 99% fast|chance the query hits a slow shard|
|---|---|---|
|10|0.99|9.6%|
|100|0.99|**63.4%**|
|100|0.999|9.5%|

A hundred-shard query with per-shard 99% latency is slow *most of the time*,
because 0.99&#8313;&#8304. Is only 0.366. The fan-out has turned a rare per-shard
event into the common case, and the only cures are to make each shard far more
solid (the third row) or to avoid the fan-out by putting the shard key in the
query. This is why a single degraded node makes an entire sharded tier feel slow,
and why "the mean shard is fast" is the wrong thing to measure.

## Questions people ask

<strong>What is sharding?</strong> Splitting data across multiple database servers, so each holds only part of it. Each part is called a shard.

<strong>When should I shard?</strong> Only after cheaper options fail: better indexes, read replicas, caching and a bigger machine. Sharding adds a lot of complexity.

<strong>What makes a good shard key?</strong> One that spreads data and traffic evenly and appears in most queries. A bad key creates a hot shard that takes most of the load.

<strong>Why are cross-shard joins hard?</strong> The rows live on different servers, so the join has to move data over the network or be done in application code.

<strong>What is rebalancing?</strong> Moving data between shards when you add or remove servers. Consistent hashing reduces how much data has to move.

<strong>Why does the slowest shard set the latency?</strong> A query that fans out to every shard must wait for all of them. One slow shard delays the whole answer.

## Where it goes wrong

**A shard key with skew.** Sharding by country puts most of the traffic on one
node. Check the distribution of real values.

**Sharding by a key the queries don't use.** each query turns
scatter-gather, and you've bought spread-systems problems for no
throughput.

**given transactions still work.** They work within a shard. Across shards
they don't, and code written before sharding often assumes or else.

**Losing the slowest shard sets the latency.** One degraded node makes each
fan-out query slow.
""",
    [
        {"q": "What is the difference between partitioning and sharding?",
         "options": ["Sharding uses hashing, partitioning uses ranges",
                     "Partitions live in one database; shards live on separate servers that share no planner, lock table or transaction manager",
                     "Sharding is for reads only",
                     "Partitioning requires a shard key"],
         "answer": 1,
         "why": "The machine boundary is the whole difficulty. Anything that needed a global view - joins, unique constraints, transactions - has to be rebuilt or given up."},
        {"q": "What happens to a query that does not name the shard key?",
         "options": ["It fails",
                     "It is sent to every shard and the results merged, with latency set by the slowest one",
                     "It is routed to shard 0",
                     "It runs on a replica"],
         "answer": 1,
         "why": "Scatter-gather. This is why the shard key is a decision about which queries stay cheap forever, not a schema detail."},
        {"q": "Why do virtual buckets make rebalancing easier?",
         "options": ["They compress the data",
                     "Keys hash to a fixed large number of buckets, so adding a shard moves a few buckets rather than changing the hash rule for every row",
                     "They remove the need for a shard key",
                     "They allow cross-shard joins"],
         "answer": 1,
         "why": "With a plain hash(key) % N rule, adding a shard changes almost every row's destination. Consistent hashing solves the same problem by moving only one arc of the ring."},
    ],
    seed="""CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, country TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, total REAL);

INSERT INTO customers VALUES
  (101,'Ada','UK'),(102,'Bo','US'),(103,'Cy','US'),(104,'Di','IN'),
  (105,'Ed','US'),(106,'Fi','UK'),(107,'Gu','US'),(108,'Hal','DE');

INSERT INTO orders VALUES
  (1,101,900,120.0),(2,102,901,64.5),(3,101,902,310.0),(4,103,900,45.0),
  (5,105,901,220.0),(6,104,900,99.9),(7,102,903,150.0),(8,107,902,72.4),
  (9,101,900,410.0),(10,108,901,58.0),(11,106,903,131.0),(12,103,900,26.5);
""",
    starter="""-- The routing rule, made visible. In a real sharded system this
-- arithmetic happens in the application or a proxy, and decides which
-- SERVER the query is sent to.
SELECT id, name, country, id % 4 AS shard
FROM   customers
ORDER  BY shard, id;
""",
    variants_label="What each access pattern costs",
    variants=[
        {"label": "Single-shard lookup",
         "sql": "-- The query names the shard key, so the router knows the answer\n"
                "-- lives on one node. This stays fast however many shards exist.\n"
                "SELECT id % 4 AS shard, id, name FROM customers WHERE id = 103;"},
        {"label": "Scatter-gather",
         "sql": "-- No shard key. Every node has to be asked and the partial\n"
                "-- results merged. Latency is the SLOWEST shard's, not the mean.\n"
                "SELECT product_id, COUNT(*) AS orders, SUM(total) AS revenue\n"
                "FROM   orders\n"
                "GROUP  BY product_id\n"
                "ORDER  BY revenue DESC;"},
        {"label": "Co-located join",
         "sql": "-- Sharding orders by customer_id puts a customer's orders on the\n"
                "-- same node as the customer, so this join never crosses a shard.\n"
                "SELECT c.id % 4 AS shard, c.name, COUNT(o.id) AS orders\n"
                "FROM   customers c JOIN orders o ON o.customer_id = c.id\n"
                "GROUP  BY c.id\n"
                "ORDER  BY shard, c.id;"},
        {"label": "A skewed shard key",
         "sql": "-- Sharding by country looks reasonable and is not: the load\n"
                "-- follows the data, and the data is not evenly spread.\n"
                "SELECT country, COUNT(*) AS customers\n"
                "FROM   customers GROUP BY country ORDER BY customers DESC;"},
    ],
)


# ---------------------------------------------------------------------------
# 14. Replication and replication lag
# ---------------------------------------------------------------------------
topic(
    "replication_and_lag",
    "Replication, Read Replicas and Lag",
    "Scale",
    "Copies of the database that serve reads, and the window in which they are "
    "wrong.",
    _svg(_box(16, 20, 42, 22, fill=S, stroke=A) + _txt(37, 34, "primary", A, 7)
         + _line(58, 31, 96, 31, B, 1.2) + _line(58, 31, 96, 58, B, 1.2)
         + _box(100, 20, 42, 22, fill=S) + _txt(121, 34, "replica", M, 7)
         + _box(100, 48, 42, 22, fill=S) + _txt(121, 62, "replica", M, 7)
         + _txt(80, 82, "reads scale, freshness does not", M, 7)),
    [
        "One primary takes the writes and streams its log to replicas, which "
        "apply it and serve reads.",
        "<strong>Replication lag</strong> is the delay between a commit on the "
        "primary and its arrival on a replica. It is never zero.",
        "The classic bug: write, redirect, read from a replica, and the user "
        "does not see their own change.",
        "Synchronous replication removes the lag and adds a network round trip "
        "to every commit. That is the trade, and it cannot be avoided.",
    ],
    """
title: Replication, Read Replicas and Lag
intro: How to serve more reads than one machine can. The staleness that comes with it.

## The arrangement

One server &mdash; the **main** &mdash; accepts each write. It records each
change in a log, and streams that log to one or more **replicas**, which apply
the changes to their own copies and serve read queries.

The appeal is that most workloads are overwhelmingly reads. Adding replicas
times read room without any change to the data model, and unlike
[sharding](sharding_in_databases.html) it's reversible: a replica that isn't
helping can simply be removed.

Replicas also serve as warm standbys. If the main fails, one is promoted.

## How far reads actually scale

"Times read room" has a limit, and the limit is worth seeing because it
decides when replicas stop being the answer. each replica serves reads *and*
must apply each write the main takes. The write load isn't shared out,
it's copied to all of them. So if one machine handles 10,000 ops a second,
a replica taking `W` writes per second has only `10,000 - W` left for reads, and
`N` replicas serve `N &times; (10,000 - W)`:

|write rate|1 replica|3 replicas|10 replicas|
|---|---|---|---|
|500/s (5%)|9,500|28,500|95,000|
|2,000/s (20%)|8,000|24,000|80,000|
|5,000/s (50%)|5,000|15,000|50,000|

At a light write rate reads scale almost linearly. Ten replicas give nearly
ten times the read throughput. This Is why read replicas are the standard answer
for read-heavy workloads. But look down the columns rather than across: as writes
climb, each replica loses that room to apply work, and the whole fleet's
read ceiling drops with it. Once writes alone approach what one machine can do,
`10,000 - W` heads toward zero and adding replicas buys almost nothing &mdash;
each new machine spends all its room just keeping up with the write stream.

That is the wall replicas hit and [sharding](sharding_in_databases.html) is built
to get past: sharding splits the writes across machines. It's the tool for a
write-bound system just where more replicas is the tool for a read-bound one.

## Lag

A change committed on the main isn't instantly present on a replica. It has
to be written to the log, sent over a network, received, and applied. The gap is
**replication lag**, and it's never zero.

Under normal rules it's milliseconds. Under load it isn't, and the reasons
matter:

**A large write.** A single statement updating a million rows makes a great
deal of log to ship and apply.

**Single-threaded apply.** Some engines apply the log serially though the
main made it with many concurrent links. The replica simply can't
keep up with a busy main.

**A long query on the replica.** Applying a change that conflicts with a running
read forces a choice between cancelling the query and pausing replication. Both
happen, based on configuration.

**Network.** A cross-region replica has a floor set by the speed of light.

## The bug this causes

The failure mode is exact and extremely common:

```
1. User updates their profile        -> primary
2. Application redirects to profile  ->
3. Profile page reads                -> replica, 200ms behind
4. User sees their OLD profile
```

Nothing errored. The user changed a thing, was shown the previous value, and
fairly concluded the save failed.

The standard fixes, in rough order of preference:

**Read-your-writes routing.** After a write, send that user's reads to the
main for a short window. Simple and effective.

**Route by criticality.** any of it the user just affected reads from the main;
dashboards and search read from replicas.

**Wait for the log spot.** Record the main's log spot at commit and
have the replica wait until it has applied at least that far. Correct, and
needs engine support.

**Don't redirect to a read.** Render the result from what was just written.

## Synchronous replication

The lag can be removed. `synchronous_commit` in PostgreSQL, semi-sync in MySQL:
the main doesn't confirm a commit until at least one replica confirms it
has the change.

The cost is unavoidable and appears on each write: a commit now includes a
network round trip. Throughput falls, and latency rises by the distance to the
replica. If the synchronous replica turns unreachable, writes stall fully
unless a fallback is configured.

That "distance to the replica" isn't a figure of speech. It has a floor set
by physics, and the floor is worth knowing before choosing where a synchronous
replica lives. Light in fibre travels at about two-thirds of `c`, so the
round-trip *can't* be faster than twice the distance over that speed:

|synchronous replica|round-trip floor|added to every commit|
|---|---|---|
|same datacentre|~0 ms|negligible|
|same region (~100 km)|~1 ms|tolerable|
|across a continent (~5,500 km)|~56 ms|every write waits 56 ms+|

Real fibre paths run about half again longer than the straight-line distance, so
the cross-continent figure is nearer 70&nbsp;ms . That is per commit, and
no amount of hardware drops it. It's the reason a synchronous replica is
kept nearby and durability across regions is bought with asynchronous copies plus
the accepted risk of the section above.

This is a direct instance of the [CAP](cap_theorem.html) trade: agreement
across replicas costs uptime and latency, and no configuration escapes it.
The usual compromise is one synchronous replica nearby for durability, and
asynchronous replicas further away for read room.

## Failover and lost writes

If the main fails while a replica is 200ms behind, promoting that replica
loses 200ms of committed writes. They were confirmed to clients and are gone.

Which is why durability needs and replication mode are the same choice.
Asynchronous replication means accepting that a failover can lose the most recent
writes.

## Questions people ask

<strong>What is replication lag?</strong> The delay between a write on the primary and that write appearing on a replica. It can be milliseconds or much longer under load.

<strong>What is a read-your-writes problem?</strong> A user writes data, then reads from a replica that has not caught up and does not see their own change. Route that read to the primary.

<strong>What is the difference between synchronous and asynchronous replication?</strong> Synchronous waits for a replica to confirm before the write returns. Asynchronous returns right away, which is faster but can lose recent writes on failover.

<strong>Do read replicas help with write load?</strong> No. Every replica must apply every write, so replicas scale reads only.

<strong>What happens to writes during failover?</strong> If replication was asynchronous, writes the replica had not received are lost when it is promoted.

<strong>How can I measure lag?</strong> Compare the primary's log position with the replica's, or use the lag figure your database exposes. Alert when it passes your tolerance.

## Where it goes wrong

**given replicas are current.** They aren't, and the window is where the bugs
live.

**Sending a write to a replica.** It's read-only. The error is confusing when
routing is silent.

**Monitoring lag in bytes only.** Bytes behind doesn't translate to seconds
behind. Track both.

**Using replicas for locking or counters.** any of it read-then-write must go to
the main, or two clients read the same stale value.

**No read-your-writes routing.** After a user writes, their next read should go to
the main for a few seconds, or they see stale data and file a bug that is
hard to trace.
""",
    [
        {"q": "Why does a user sometimes not see their own change after saving?",
         "options": ["The write failed silently",
                     "The read went to a replica that has not yet applied the change",
                     "The cache was stale",
                     "The transaction rolled back"],
         "answer": 1,
         "why": "Nothing errored. Read-your-writes routing - sending that user's reads to the primary briefly after a write - is the usual fix."},
        {"q": "What does synchronous replication cost?",
         "options": ["Extra disk on the replica",
                     "A network round trip on every commit, so writes get slower and stall if the replica is unreachable",
                     "The ability to add more replicas",
                     "Read capacity"],
         "answer": 1,
         "why": "It is a direct instance of the CAP trade: consistency across replicas costs availability and latency, and no configuration escapes it."},
        {"q": "What happens if a primary fails while a replica is 200ms behind?",
         "options": ["The replica catches up first",
                     "Promoting it loses 200ms of writes that were already acknowledged to clients",
                     "Writes are replayed from the client",
                     "The failover is rejected"],
         "answer": 1,
         "why": "Those writes were confirmed and are gone. Durability requirements and replication mode are therefore the same decision."},
    ],
    timeline={
        "a": "Primary (takes the write)",
        "b": "Replica (serves the read)",
        "intro": "Step through a save-then-view. Choose the routing strategy and "
                 "watch whether the user sees their own change.",
        "levels": [
            {"value": "async", "label": "Async replica, read from replica"},
            {"value": "sticky", "label": "Async replica, read-your-writes"},
            {"value": "sync", "label": "Synchronous replication"},
        ],
        "steps": [
            {"who": "a", "sql": "UPDATE profiles SET bio = 'new bio' WHERE id = 7;",
             "says": {"*": "The write lands on the primary. Replicas know nothing about it yet."}},
            {"who": "a", "sql": "COMMIT;",
             "says": {"async": "The primary acknowledges immediately. The change is queued for shipping to the replica.",
                      "sticky": "The primary acknowledges immediately, and the application notes that this user just wrote.",
                      "sync": "The primary does NOT acknowledge yet. It waits for a replica to confirm - this is the round trip synchronous commit adds to every write."}},
            {"who": "b", "sql": "-- replication stream in flight --",
             "says": {"async": "The change is travelling. The replica is currently behind by however long this takes.",
                      "sticky": "The change is travelling, and the replica is behind - but the application is not going to ask it yet.",
                      "sync": "The replica applies the change and confirms. Only now does the primary tell the client the commit succeeded."}},
            {"who": "b", "sql": "SELECT bio FROM profiles WHERE id = 7;",
             "says": {"async": "The read goes to the replica, which has not applied the change yet. It returns the OLD bio. The user thinks the save failed.",
                      "sticky": "The application routes this read to the PRIMARY, because this user wrote recently. The new bio comes back. The replica is still behind - it just is not being asked.",
                      "sync": "The replica already has the change, because the commit did not complete until it did. The new bio comes back."}},
            {"who": "b", "sql": "-- a few hundred milliseconds later --",
             "says": {"async": "The replica catches up. A refresh now shows the new bio - which is why this bug is so often dismissed as unreproducible.",
                      "sticky": "The replica catches up, and the sticky window expires. Reads for this user go back to the replica safely.",
                      "sync": "Nothing to catch up on. The cost was paid at commit time instead, on every write whether it mattered or not."}},
        ],
    },
)


# ---------------------------------------------------------------------------
# 15. CAP theorem
# ---------------------------------------------------------------------------
topic(
    "cap_theorem",
    "The CAP Theorem",
    "Distributed",
    "When the network splits, a distributed store can stay correct or stay "
    "answering. It cannot do both.",
    _svg('<circle cx="52" cy="40" r="24" fill="none" stroke="%s" stroke-width="1.6"/>' % B
         + '<circle cx="84" cy="40" r="24" fill="none" stroke="%s" stroke-width="1.6"/>' % B
         + '<circle cx="68" cy="62" r="24" fill="none" stroke="%s" stroke-width="1.6"/>' % A
         + _txt(38, 32, "C", M, 9) + _txt(100, 32, "A", M, 9) + _txt(68, 80, "P", A, 9)
         + _txt(130, 44, "pick 2", M, 8)),
    [
        "The theorem is about what happens <em>during a network partition</em>. "
        "With no partition there is no trade to make.",
        "<strong>CP</strong>: refuse to answer rather than answer wrongly. "
        "<strong>AP</strong>: answer from what this node knows and reconcile later.",
        "'Pick two of three' is the famous phrasing and a misleading one. "
        "Partitions are not optional, so the real choice is C or A.",
        "PACELC extends it: <em>else</em>, when there is no partition, the trade "
        "is latency against consistency &mdash; and that one is always live.",
    ],
    """
title: The CAP Theorem
intro: The most quoted and most misquoted result in spread data, and what it really constrains.

## What the three letters mean

**Agreement** here means *linearisability*: each read sees the most recent
write, as if there were one copy. It isn't the C in ACID, which is about
constraints being met. Two different ideas, one letter, endless confusion.

**Uptime** means each request to a non-failed node gets a non-error
response. Not "mostly up" &mdash; each request, each working node.

**Split handling** means the system keeps operating when the network drops
or delays messages between nodes.

## The theorem, stated properly

The common phrasing &mdash; "pick two of three" &mdash; is catchy and wrong
in a way that matters.

Splits aren't a design choice. Networks fail: cables are cut, switches
reboot, a cloud uptime zone turns unreachable. Any system spanning more
than one machine will be split eventually, so **P isn't optional**.

What the theorem really says is narrower and more handy:

> When a split occurs, you must choose between agreement and uptime.

That is it. When the network is healthy, a system can be both steady and
available, and most are. The theorem constrains action during a exact,
temporary failure.

## The choice, concretely

Two nodes can no longer talk. A write arrives at one of them.

**CP &mdash; refuse.** Return an error, because confirming a write the other
side can't see risks two different answers to the same question. Correct, and
temporarily down to whoever can't reach a quorum.

Choose this when a wrong answer is worse than no answer: account weighs,
inventory that must not oversell, any of it involving money or safety.

**AP &mdash; accept.** Take the write locally, serve reads from local state, and
merge when the split heals. Always answering, and during the split
two clients can see different values.

Choose this when an answer now is worth more than a just right current one: a
shopping cart, a social feed, a view counter, a DNS record. Amazon's first
Dynamo paper made this arg for carts by name &mdash; a cart that
at times resurrects a deleted item is better business than a cart that is
at times down.

Step the timeline above through both settings and the difference is one choice
made at one moment.

## Reconciling afterwards

An AP system must resolve conflicting versions once the network returns.
**Last-write-wins** is simple and silently discards data when clocks disagree.
**Vector clocks** detect concurrent writes and hand the conflict to the
use. **CRDTs** are data types designed so concurrent updates merge
deterministically &mdash; which is why counters, sets and collaborative text
editors are the AP success stories.

## PACELC, which is the more useful version

CAP only shows splits, and splits are rare. Daniel Abadi's extension
covers the rest of the time:

> **if P**artition then **A**vailability or **C**onsistency, **E**lse
> **L**atency or **C**onsistency.

The second half is the one engineers meet daily. With the network healthy, a
system can still choose to confirm each write with remote replicas &mdash;
steady and slower &mdash; or confirm locally and replicate afterwards
&mdash; faster and briefly stale.

That is just the [synchronous versus asynchronous replication
choice](replication_and_lag.html), and unlike CAP's trade it's live on each
request.

That "live on each request" is the whole reason the extension earns its keep. A
split is a rare event. The network between healthy nodes works the vast
majority of the time &mdash; so CAP's agreement-or-uptime choice is one you
really pay only during those rare failures. The latency-or-agreement choice,
by contrast, is paid on *each single request* the system ever serves. PACELC is
"the more handy version" just because it names the trade you make billions
of times a day rather than the one you make on the bad afternoon a cable is cut.

## The tunable, made concrete: R + W > N

The last "where it goes wrong" note below says the labels are tunable per query.
That tuning is one inequality, and it's worth seeing because it's how a single
system offers both answers.

Keep `N` copies of each row. Let a write wait for `W` of them to confirm, and
a read collect answers from `R` of them and take the newest. The read is
ensured to see the latest write when the read set and the write set must
share &mdash; which is just when **R + W > N**. Below that they can miss each
other, and a read can come back stale.

On `N = 3`:

|W|R|R + W > N|what you get|
|---|---|---|---|
|1|1|no|fastest reads and writes, but reads can be stale|
|2|2|yes|**quorum**: strong, and survives one node down either way|
|3|1|yes|strong, instant reads, but a write needs all three up|
|1|3|yes|strong, instant writes, but a read needs all three up|

Read the `W=1, R=1` row against the `W=2, R=2` row: same three machines, and the
choice between a possibly-stale answer and a ensured-current one is nothing but
how many replicas each op waits for. That is the AP/CP dial from earlier,
turned per request instead of per system.

Quorum &mdash; `W = R = 2` &mdash; is the common default because 2 + 2 = 4 > 3
shares by one replica *and* still ends with a single node down, where the
`R = 1` and `R = 3` rows each give up uptime on one side. This is just
what Cassandra's `ONE` / `QUORUM` / `ALL` levels and DynamoDB's strongly-steady
reads are selecting.

## Questions people ask

<strong>What do the letters in CAP stand for?</strong> Consistency, Availability and Partition tolerance.

<strong>Can I really only pick two of the three?</strong> Not quite. Partitions happen on real networks, so the choice is what to give up during a partition: consistency or availability.

<strong>What does a CP system do during a partition?</strong> It refuses some requests, or returns errors, to avoid serving inconsistent data.

<strong>What does an AP system do during a partition?</strong> It keeps answering from each side, accepting that replicas may disagree until they can be reconciled later.

<strong>What is PACELC?</strong> It extends CAP: if there is a Partition, choose Availability or Consistency; Else, choose Latency or Consistency. It covers the normal case too.

<strong>What does R + W > N mean?</strong> With N replicas, reading from R and writing to W of them such that R + W exceeds N guarantees every read overlaps the latest write.

## Where it goes wrong

**"We chose AP, so we gave up agreement."** You gave up linearisability during
splits. Most of the time the system is steady.

**Confusing CAP's C with ACID's C.** Different properties.

**Calling a single-node DB CP.** With one node there's no split and
the theorem doesn't apply.

**Treating the labels as fixed.** Many systems are tunable per query &mdash;
Cassandra's agreement levels, DynamoDB's strongly steady reads &mdash; so
the choice belongs to the op, not the product.
""",
    [
        {"q": "What is wrong with 'pick two of three'?",
         "options": ["There are actually four properties",
                     "Partitions are not optional, so the real choice is between C and A when one occurs",
                     "Consistency and availability are the same thing",
                     "It only applies to SQL databases"],
         "answer": 1,
         "why": "Networks fail eventually, so P must be tolerated. The theorem constrains behaviour during that specific temporary failure, not design in general."},
        {"q": "A CP system during a partition will:",
         "options": ["Answer from local state and reconcile later",
                     "Return an error rather than risk two different answers to the same question",
                     "Elect a new primary",
                     "Queue writes indefinitely"],
         "answer": 1,
         "why": "Correct, and temporarily unavailable to anyone who cannot reach a quorum. The right choice when a wrong answer is worse than no answer."},
        {"q": "What does the 'ELC' half of PACELC describe?",
         "options": ["Error handling during partitions",
                     "The latency-against-consistency trade when the network is healthy, which is live on every request",
                     "Eventual consistency guarantees",
                     "Leader election"],
         "answer": 1,
         "why": "Confirm every write with remote replicas and be slower, or acknowledge locally and be briefly stale. It is the synchronous-versus-asynchronous replication choice."},
    ],
    timeline={
        "a": "Node A (client 1 writes here)",
        "b": "Node B (client 2 reads here)",
        "intro": "The network between the two nodes is about to fail. Pick a "
                 "strategy and step through to see what each client experiences.",
        "levels": [
            {"value": "cp", "label": "CP - refuse rather than diverge"},
            {"value": "ap", "label": "AP - answer and reconcile later"},
        ],
        "steps": [
            {"who": "a", "sql": "SELECT stock FROM items WHERE id = 1;  -- 5",
             "says": {"*": "Network healthy. Both nodes agree: 5 in stock. With no partition, the system is consistent AND available."}},
            {"who": "b", "sql": "-- network partition begins --",
             "says": {"*": "A and B can no longer reach each other. Neither has failed; they simply cannot talk. Every message between them is lost."}},
            {"who": "a", "sql": "UPDATE items SET stock = 4 WHERE id = 1;",
             "says": {"cp": "Node A cannot reach a quorum, so it REFUSES the write and returns an error. The client is told the system is unavailable - which is true, and better than a lie.",
                      "ap": "Node A accepts the write locally. Its stock is now 4. It has no way to tell B, and it proceeds anyway."}},
            {"who": "b", "sql": "SELECT stock FROM items WHERE id = 1;",
             "says": {"cp": "Node B also cannot reach a quorum. It refuses the read too. Nobody gets a wrong answer, and nobody gets an answer.",
                      "ap": "Node B answers from what it knows: 5. This is now WRONG - A has it at 4 - and B has no way to find that out. Two clients, two truths."}},
            {"who": "b", "sql": "-- partition heals --",
             "says": {"cp": "The nodes reconnect. There is nothing to reconcile, because nothing was written during the split. The system becomes available again, still correct.",
                      "ap": "The nodes reconnect and discover they disagree. Something must resolve it: last-write-wins (which can silently discard data), vector clocks, or a CRDT designed to merge deterministically."}},
            {"who": "a", "sql": "SELECT stock FROM items WHERE id = 1;",
             "says": {"cp": "5 - and the update never happened, so the client must retry. Consistency was preserved by refusing service for the duration.",
                      "ap": "4, once reconciliation picks a winner. The system never stopped answering; it was briefly wrong instead. For a shopping cart that is the right trade. For a bank balance it is not."}},
        ],
    },
)


# ---------------------------------------------------------------------------
# 16. Document model
# ---------------------------------------------------------------------------
topic(
    "document_model_vs_rows",
    "The Document Model against Rows",
    "Data Models",
    "The same data as normalised tables and as nested documents, and what each "
    "shape makes easy.",
    _svg(_table_icon(12, 24, 42) + _txt(33, 76, "rows", M, 7)
         + _txt(66, 46, "vs", M, 8)
         + _box(84, 22, 58, 46, fill=S, stroke=A)
         + _txt(113, 36, "{ order:", A, 7) + _txt(113, 48, "  items:[..]", M, 7)
         + _txt(113, 60, "}", A, 7)),
    [
        "A document stores related data together, nested. A relational schema "
        "stores it apart and joins on demand.",
        "Documents win when the access pattern is 'give me this whole thing' "
        "&mdash; one read, no joins.",
        "Rows win when the data is queried from several directions, or when the "
        "same fact appears in many documents and has to stay consistent.",
        "SQLite, PostgreSQL and MySQL all have JSON columns, so the choice is "
        "per-column now rather than per-database.",
    ],
    """
title: The Document Model against Rows
intro: One order, stored two ways. An honest account of which questions each shape answers well.

## The same order, two shapes

Run the query above and then the variants. The the same order is stored as
normed rows and as a single JSON doc, and both are queried in the same
session &mdash; because modern SQL engines support both.

**Relational**: an `orders` row, several `order_items` rows referring back to it,
a `customers` row. Each fact recorded once, joined when needed.

**Document**: one record containing the order, its items nested inside it, and
the customer details copied in.

## What documents make easy

**One read for one thing.** Fetching an order means pulling one doc.
No joins, no round trips, and the data is contiguous on disk. For a
read-this-whole-object access pattern, this is truly faster and the gap
widens as the object gets more parts.

**A shape that matches the code.** The doc deserialises straight into an
object. No object-relational mapping layer reassembling a graph from five result
sets.

**Schema flexibility.** Adding a field to some docs and not others needs
no migration. For truly heterogeneous data &mdash; product catalogues where
a book and a fridge share almost no fields. This is a real edge
rather than laziness.

## What rows make easy

**Querying from any direction.** "Which customers bought product 902" is
straightforward relationally and awkward in a doc store, because the data
is organised around orders, not products. docs optimise one access path and
make the others harder.

**Updating a shared fact once.** If the customer's address is copied into each
order doc, changing it means finding and rewriting each one. Relationally
it's a single `UPDATE`. This is the classic norming arg and it has
not stopped being true.

**Integrity the DB enforces.** Foreign keys, uniqueness and check
constraints are declared once and can't be bypassed. In a doc store these
often become use code. This Means they hold until some other code
path forgets.

**Ad-hoc analysis.** Aggregating across docs means either a scan or a
purpose-built index, and the queries are harder to write.

## Denormalisation is the actual trade

Nesting the items inside the order is fine. An order item belongs to
just one order and is never queried on its own. That isn't duplication,
just co-location.

Copying the customer's name and address into each order is duplication, and it
buys read speed at the cost of update cost and the risk of divergence. at times
that is right: an invoice arguably *should* record the address as it was at the
time, in which case it isn't duplication at all but a historical fact.

The question is always whether the copies must agree. If they must, storing them
apart means keeping them in sync forever.

## The distinction has mostly dissolved

PostgreSQL's `jsonb` is indexable, queryable and transactional. MySQL and SQLite
have JSON functions &mdash; the queries on this page use SQLite's, in the same
session as plain tables.

So the modern answer is often neither purely one nor the other: relational
tables for the entities that are queried from a few directions and must stay
steady, and a JSON column for the parts that are truly variable and only
ever read alongside their parent.

What a dedicated doc DB still offers is flat scaling and
operational tooling built around that model from the start. What it gives up is
joins and multi-doc transactions &mdash; though MongoDB has had the latter
since 4.0, which narrowed the gap a lot.

## The number behind the update argument

"Rewriting each one" is the whole cost of copying a shared fact, and it's worth
seeing at scale. Suppose the customer's address is denormalised into each of
their order docs. Changing it isn't one write:

|orders holding the copy|document store: rewrites|relational: rows changed|
|---|---|---|
|100|100|1|
|10,000|10,000|1|
|1,000,000|1,000,000|1|

Relationally the address lives in one `customers` row and one `UPDATE` changes it;
each order simply keeps pointing at it. The doc shape trades that single
write for one per copy, and while the copies are being rewritten the DB
briefly disagrees with itself about where the customer lives. That is the exact
trade: the doc read is faster because the join was done once at write time,
and each later change to a shared fact pays it back in full.

## The read the document shape wins

The mirror image of the update cost is the read. It's why the trade exists
at all. Assembling one order. The order, its five line items, the customer
&mdash; from normed tables means touching three tables, and an ORM that loads
them naively issues one query for the order and then one per related set:

|shape|reads to assemble one order|
|---|---|
|document|**1** (the whole object, contiguous)|
|relational, one join query|3 tables joined|
|relational, naive ORM|1 + N round trips (the N+1 problem)|

The doc was written with the join already done. So The read is a single
contiguous fetch with no reassembly. That is a real edge for a
read-this-whole-object access pattern, and it grows as the object gains parts. It
is the same coin as the update cost: the doc pays once at write time to make
this read cheap, and the relational shape pays a little at read time to keep each
fact in one place. Which way that trade should fall is a property of the workload, not of the
DB &mdash; read-mostly and object-shaped leans doc, write-shared and
queried-many-ways leans relational.

## Questions people ask

<strong>When is a document database a better fit than rows?</strong> When records are read and written whole, vary in shape, and are rarely joined to other records.

<strong>What is denormalisation?</strong> Storing related data together, even if it repeats, so reads need no joins. It speeds reads and complicates updates.

<strong>Can a relational database store JSON?</strong> Yes. PostgreSQL, MySQL and others have JSON column types with indexing, so the line between the models has blurred.

<strong>Why are updates harder in documents?</strong> A repeated value, such as a customer name, must be changed in every document that copies it.

<strong>Do document databases support joins?</strong> Some offer lookup operations, but they are not as flexible or fast as relational joins. Design documents around the queries you run.

<strong>How do I choose between them?</strong> Look at your access pattern. Many cross-entity queries and strict integrity favour rows. Self-contained records read as a unit favour documents.

## Where it goes wrong

**Choosing docs to avoid schema design.** The schema still exists. It has
moved into the use, where nothing enforces it.

**Unbounded arrays.** A doc that grows without limit &mdash; each event
appended to one record &mdash; eventually exceeds the size limit and rewrites
the whole thing on each append.

**Duplicating a fact that must stay steady.** Fine for a historical snapshot,
a slow disaster for live data.

**Using JSON columns for well-structured data.** If each row has the same
fields, they're columns. Putting them in JSON gives up type checking and
constraints for nothing.
""",
    [
        {"q": "When does the document model genuinely beat normalised rows?",
         "options": ["Always, for reads",
                     "When the access pattern is fetching one whole object, since it is a single read with no joins",
                     "When data must be strongly consistent",
                     "When the same fact appears in many places"],
         "answer": 1,
         "why": "The data is contiguous and deserialises straight into an object. The gap widens as the object gains parts - and closes when queries come from other directions."},
        {"q": "What is the real cost of copying a customer's address into every order document?",
         "options": ["Disk space",
                     "Every change means finding and rewriting every copy, and any missed copy diverges",
                     "Slower reads",
                     "It breaks JSON indexing"],
         "answer": 1,
         "why": "The question is whether the copies must agree. On an invoice the address arguably should be a historical fact, in which case it is not duplication at all."},
        {"q": "Why has the relational/document distinction largely dissolved?",
         "options": ["Document stores added SQL",
                     "PostgreSQL, MySQL and SQLite all have indexable, queryable, transactional JSON columns, so the choice is per-column",
                     "Documents turned out to be slower",
                     "Normalisation was abandoned"],
         "answer": 1,
         "why": "Tables for entities queried from several directions, a JSON column for genuinely variable parts read only alongside their parent - in one database, in one transaction."},
    ],
    seed="""CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, placed TEXT);
CREATE TABLE order_items (order_id INTEGER, product TEXT, qty INTEGER, price REAL);

INSERT INTO customers VALUES (101,'Ada','Leeds'),(102,'Bo','Bristol');
INSERT INTO orders VALUES (1,101,'2026-08-01'),(2,102,'2026-08-03');
INSERT INTO order_items VALUES
  (1,'keyboard',1,45.0),(1,'cable',2,6.5),(1,'mouse',1,22.0),
  (2,'monitor',1,180.0),(2,'cable',1,6.5);

CREATE TABLE order_docs (id INTEGER PRIMARY KEY, doc TEXT);
INSERT INTO order_docs VALUES
 (1,'{"id":1,"placed":"2026-08-01","customer":{"id":101,"name":"Ada","city":"Leeds"},"items":[{"product":"keyboard","qty":1,"price":45.0},{"product":"cable","qty":2,"price":6.5},{"product":"mouse","qty":1,"price":22.0}]}'),
 (2,'{"id":2,"placed":"2026-08-03","customer":{"id":102,"name":"Bo","city":"Bristol"},"items":[{"product":"monitor","qty":1,"price":180.0},{"product":"cable","qty":1,"price":6.5}]}');
""",
    starter="""-- The relational shape: three tables, joined on demand.
SELECT c.name, o.id AS order_id, i.product, i.qty, i.price
FROM   orders o
JOIN   customers   c ON c.id = o.customer_id
JOIN   order_items i ON i.order_id = o.id
ORDER  BY o.id, i.product;
""",
    variants_label="The same data, both ways",
    variants=[
        {"label": "Relational: join three tables",
         "sql": "-- Each fact stored once. Reassembled at query time.\n"
                "SELECT c.name, o.id AS order_id, i.product, i.qty, i.price\n"
                "FROM   orders o\n"
                "JOIN   customers   c ON c.id = o.customer_id\n"
                "JOIN   order_items i ON i.order_id = o.id\n"
                "ORDER  BY o.id, i.product;"},
        {"label": "Document: one read, no joins",
         "sql": "-- The whole order in one row. This is the access pattern\n"
                "-- documents are good at.\n"
                "SELECT json_extract(doc,'$.customer.name') AS customer,\n"
                "       json_extract(doc,'$.id')            AS order_id,\n"
                "       json_extract(value,'$.product')     AS product,\n"
                "       json_extract(value,'$.qty')         AS qty\n"
                "FROM   order_docs, json_each(order_docs.doc,'$.items')\n"
                "ORDER  BY order_id, product;"},
        {"label": "Querying the other way round",
         "sql": "-- 'Who bought a cable?' is natural relationally...\n"
                "SELECT c.name, i.qty\n"
                "FROM   order_items i\n"
                "JOIN   orders o    ON o.id = i.order_id\n"
                "JOIN   customers c ON c.id = o.customer_id\n"
                "WHERE  i.product = 'cable';"},
        {"label": "...and awkward as documents",
         "sql": "-- ...but the documents are organised around orders, so this has\n"
                "-- to unnest every one of them to find the same answer.\n"
                "SELECT json_extract(d.doc,'$.customer.name') AS name,\n"
                "       json_extract(value,'$.qty')           AS qty\n"
                "FROM   order_docs d, json_each(d.doc,'$.items')\n"
                "WHERE  json_extract(value,'$.product') = 'cable';"},
        {"label": "The duplicated fact",
         "sql": "-- Ada moves to York. Relationally that is one row. In the\n"
                "-- documents her city is copied into every order she ever placed.\n"
                "UPDATE customers SET city = 'York' WHERE id = 101;\n"
                "SELECT (SELECT city FROM customers WHERE id=101)          AS relational,\n"
                "       json_extract(doc,'$.customer.city')                AS in_document\n"
                "FROM   order_docs WHERE id = 1;"},
    ],
)


# ---------------------------------------------------------------------------
# 17. Key-value and graph models
# ---------------------------------------------------------------------------
topic(
    "key_value_and_graph_models",
    "Key-Value and Graph Models",
    "Data Models",
    "Two models at opposite ends: one that does almost nothing very fast, and "
    "one built entirely around following relationships.",
    _svg(_box(10, 28, 46, 18, fill=S) + _txt(33, 40, "key &#8594; value", M, 7)
         + _txt(33, 60, "no queries", M, 7)
         + '<circle cx="92" cy="30" r="6" fill="none" stroke="%s" stroke-width="1.4"/>' % A
         + '<circle cx="122" cy="46" r="6" fill="none" stroke="%s" stroke-width="1.4"/>' % A
         + '<circle cx="92" cy="62" r="6" fill="none" stroke="%s" stroke-width="1.4"/>' % A
         + _line(98, 33, 116, 43, B, 1) + _line(98, 59, 116, 50, B, 1)
         + _txt(107, 80, "edges are the point", M, 7)),
    [
        "A key-value store supports get, put and delete on an opaque value. "
        "That is the entire interface.",
        "The narrowness is the feature: no query planner, no joins, and a "
        "lookup that is a hash away.",
        "A graph model makes relationships first-class. Traversing them costs "
        "the same whether the graph is small or huge.",
        "In SQL, a graph traversal is a recursive CTE &mdash; possible, and "
        "verbose enough to show why a dedicated model exists.",
    ],
    """
title: Key-Value and Graph Models
intro: The simplest data model and the most tie-centred one. When each is worth leaving SQL for.

## Key-value: doing less on purpose

The interface is three ops:

```
get(key)  ->  value
put(key, value)
delete(key)
```

The value is opaque &mdash; a blob the store doesn't read. You can't query
by its contents, sort by it, or join on it. There's no schema and no query
language.

That poverty is the point. With no query planner, no join methods and no
secondary indexes to maintain, a lookup is a hash and a read. Redis, Memcached,
DynamoDB in its simplest mode and etcd all live here. They're fast in a way
a all-round DB can't match, because they've far less to do.

The cost is that each access path must be designed in advance, coded in the
key. Fetching a user by id means `user:1234`. Fetching them by email means
keeping a second key, `email:ada@example.com -> 1234`, and keeping the two in
step yourself &mdash; there's no unique constraint and no transaction spanning
them.

The first variant above shows the shape: a two-column table used as nothing but a
key lookup.

**Where it fits.** Caches, sessions, feature flags, rate limiters, leaderboards,
service find. any of it with one obvious access path and a strong preference
for speed.

**Where it doesn't.** any of it needing an ad-hoc question. "How many active
sessions are from Leeds" isn't answerable without scanning each key, which the
model isn't built for.

## Graph: relationships as the primary thing

A graph model stores **nodes** and **edges**, and both can carry properties. The
edges aren't derived from matching values, as a foreign key is. They're stored
objects, and traversing one is following a pointer.

The difference shows up in queries about *paths*. "Who reports to Ada, right
or indirectly, to any depth" is one traversal in a graph and a recursive CTE in
SQL &mdash; run the variant and compare it against the plain join beside it.

The gap widens with depth. Each level of a relational traversal is another join,
and the planner's guesses degrade as they compound. A graph engine follows
edges right, and cost scales with the number of edges really visited rather
than with the size of the tables.

**Where it fits.** Social networks, org charts, fraud rings, dependency graphs,
recommendation paths, network topology, knowledge graphs. The test is whether
your notable questions are about links rather than about fields.

**Where it doesn't.** Aggregating over millions of rows. A graph engine is
often worse at "total revenue by month" than any relational DB.

## The honest comparison

| | Key-value | Relational | Graph |
|---|---|---|---|
| Lookup by id | fastest | fast | fast |
| Ad-hoc queries | no | yes | limited |
| Joins | no | yes | native, as traversal |
| Variable-depth paths | no | recursive CTE | native |
| Aggregation | no | yes | weak |
| Schema enforcement | none | strong | usually light |

## Do you need to leave SQL?

Often not, and the variants above are the arg.

A key-value table in Postgres. A main key and a `jsonb` column &mdash;
gets you most of the model with transactions and the option of querying the
value later. Redis wins on raw latency. If that isn't the binding constraint,
the simpler operational story often is.

Recursive CTEs handle graph traversal, and for a few hundred thousand edges at
modest depth they're just right good. Dedicated graph engines start winning at
deep traversals over large graphs, and at query *expressibility* &mdash; Cypher
and Gremlin say in one line what a recursive CTE says in fifteen.

The strong arg for a separate store is when the workload is
overwhelmingly of one shape. The weak arg is that the model is fashionable.

## Why traversal depth is where graphs win

The graph edge isn't vague. It scales with depth, and the math shows
where the crossover is. "Friends of friends of friends" over a social graph with
an mean of 100 links per person touches, level by level, roughly 100 then
10,000 then 1,000,000 people. A relational engine reaches each level with another
join, and the planner's row guesses degrade as they times:

|depth|people reached (branching ~100)|relational cost|
|---|---|---|
|1|100|one join|
|2|10,000|join of a join|
|3|1,000,000|three joins, estimates compounding|

A graph engine follows stored edges right. So Its cost tracks *edges really
visited* rather than the product of table sizes, and it doesn't re-guess a
join at each level. At depth one or two a recursive CTE is just right good. By
depth three or four over a large graph the relational plan is doing work
proportional to the tables while the graph is doing work proportional to the
answer. That divergence &mdash; not lookup speed &mdash; is the real reason to
reach for a graph.

## The lookup, and why it is O(1)

The reason a key-value store outruns a general DB on its one job is the
lack of a tree. A relational main-key lookup descends a B-tree &mdash; about
`log2(n)` steps &mdash; while a hash-based key-value `get` finds one hash and
does one read, even so of size:

|keys stored|B-tree lookup|hash lookup|
|---|---|---|
|1,000,000|~20 steps|~1 probe|
|1,000,000,000|~30 steps|~1 probe|

The B-tree's cost grows, slowly, forever. The hash's doesn't grow at all. That
flat line is the whole value proposition, and it's bought by giving up
all a tree enables &mdash; sorted scans, range queries, "the next key
after this one" &mdash; none of which a hash can answer. So the choice isn't
"key-value is faster" but "key-value is faster at point lookups and can't do
ranges at all", which is just the trade to weigh before moving a workload off
SQL for speed.

## Questions people ask

<strong>What is a key-value store good for?</strong> Fast lookups by a known key, such as sessions, caches and counters. It does one thing and does it quickly.

<strong>Why is a key-value lookup O(1)?</strong> The key is hashed to find where the value is stored, so lookup time does not grow with the number of entries.

<strong>What is a graph database?</strong> A database that stores nodes and the relationships between them, and makes following those links a primary operation.

<strong>When does a graph beat SQL joins?</strong> When queries follow connections several hops deep, such as friends of friends. Each hop in SQL adds a join, while a graph follows stored links.

<strong>Can I query a key-value store by value?</strong> Not directly. You can only look up by key unless the store adds secondary indexes, so design keys around your queries.

<strong>Do I need to leave SQL for these workloads?</strong> Often not. Recursive CTEs handle many graph questions, and a table with a key column works as a simple key-value store. Switch when scale or traversal depth demands it.

## Where it goes wrong

**Using a key-value store as the system of record without a plan for secondary
access.** The second access path is your problem, forever.

**given a graph DB is faster at all.** It's faster at
traversals and often slower at aggregates.

**Recursive CTEs without a depth limit.** A cycle in the data is an infinite
loop. The variant here carries a guard for just that reason.

**Modelling all as a graph.** If the questions are about fields rather
than links, a table is the better graph.
""",
    [
        {"q": "Why is a key-value store fast?",
         "options": ["It keeps everything in memory",
                     "It has no query planner, joins or secondary indexes to maintain, so a lookup is a hash and a read",
                     "It compresses values",
                     "It skips durability"],
         "answer": 1,
         "why": "The narrow interface is the feature. The cost is that every access path must be designed in advance and encoded in the key."},
        {"q": "How does a graph edge differ from a SQL foreign key?",
         "options": ["It is faster to write",
                     "It is a stored object followed like a pointer, rather than a value matched at query time",
                     "It can only connect two node types",
                     "It cannot carry properties"],
         "answer": 1,
         "why": "This is why traversal cost scales with edges visited rather than table size, and why the gap against joins widens with depth."},
        {"q": "What is a graph database usually worse at than a relational one?",
         "options": ["Variable-depth traversal",
                     "Aggregating over millions of rows, such as total revenue by month",
                     "Storing properties on relationships",
                     "Finding shortest paths"],
         "answer": 1,
         "why": "The test for reaching for a graph model is whether your interesting questions are about connections rather than about attributes."},
    ],
    seed="""CREATE TABLE kv (key TEXT PRIMARY KEY, value TEXT);
INSERT INTO kv VALUES
  ('user:1234','{"name":"Ada","email":"ada@example.com"}'),
  ('user:1235','{"name":"Bo","email":"bo@example.com"}'),
  ('email:ada@example.com','1234'),
  ('email:bo@example.com','1235'),
  ('session:abc','{"user":1234,"expires":"2026-08-25T10:00:00"}');

CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT, role TEXT);
CREATE TABLE reports_to (person INTEGER, manager INTEGER);

INSERT INTO people VALUES
  (1,'Ada','CTO'),(2,'Bo','Eng Manager'),(3,'Cy','Eng Manager'),
  (4,'Di','Engineer'),(5,'Ed','Engineer'),(6,'Fi','Engineer'),
  (7,'Gu','Intern'),(8,'Hal','Engineer');

INSERT INTO reports_to VALUES
  (2,1),(3,1),(4,2),(5,2),(6,3),(7,4),(8,3);
""",
    starter="""-- The key-value model, in its entirety: get by key.
-- No query language, no joins, no way to ask about the value.
SELECT value FROM kv WHERE key = 'user:1234';
""",
    variants_label="Both models, and the SQL equivalents",
    variants=[
        {"label": "Key-value: get",
         "sql": "-- The whole interface. Fast because there is nothing to plan.\n"
                "SELECT value FROM kv WHERE key = 'user:1234';"},
        {"label": "Key-value: the second access path",
         "sql": "-- Wanting users by email means maintaining a SECOND key yourself,\n"
                "-- and keeping the two in step without a constraint to help.\n"
                "SELECT k2.value AS user_json\n"
                "FROM   kv k1\n"
                "JOIN   kv k2 ON k2.key = 'user:' || k1.value\n"
                "WHERE  k1.key = 'email:ada@example.com';"},
        {"label": "Graph: one hop",
         "sql": "-- Direct reports. A single join - relational SQL is fine here.\n"
                "SELECT m.name AS manager, p.name AS reports\n"
                "FROM   reports_to r\n"
                "JOIN   people p ON p.id = r.person\n"
                "JOIN   people m ON m.id = r.manager\n"
                "WHERE  m.name = 'Ada';"},
        {"label": "Graph: any depth",
         "sql": "-- Everyone under Ada, however deep. In Cypher this is one line.\n"
                "-- The depth guard is not decoration: a cycle in the data would\n"
                "-- otherwise loop forever.\n"
                "WITH RECURSIVE chain(id, name, depth) AS (\n"
                "    SELECT id, name, 0 FROM people WHERE name = 'Ada'\n"
                "  UNION ALL\n"
                "    SELECT p.id, p.name, c.depth + 1\n"
                "    FROM   chain c\n"
                "    JOIN   reports_to r ON r.manager = c.id\n"
                "    JOIN   people p     ON p.id = r.person\n"
                "    WHERE  c.depth < 10\n"
                ")\n"
                "SELECT depth, name FROM chain WHERE depth > 0 ORDER BY depth, name;"},
        {"label": "Graph: path to the top",
         "sql": "-- The other direction: the chain of command above one person.\n"
                "WITH RECURSIVE up(id, name, depth) AS (\n"
                "    SELECT id, name, 0 FROM people WHERE name = 'Gu'\n"
                "  UNION ALL\n"
                "    SELECT m.id, m.name, u.depth + 1\n"
                "    FROM   up u\n"
                "    JOIN   reports_to r ON r.person = u.id\n"
                "    JOIN   people m     ON m.id = r.manager\n"
                "    WHERE  u.depth < 10\n"
                ")\n"
                "SELECT depth, name FROM up ORDER BY depth;"},
    ],
)


# ---------------------------------------------------------------------------
# 18. OLTP vs OLAP and columnar storage
# ---------------------------------------------------------------------------
topic(
    "oltp_vs_olap_columnar",
    "OLTP, OLAP and Columnar Storage",
    "Analytics",
    "Two workloads that want opposite things from disk, and the storage layout "
    "that serves each.",
    _svg(_grid_rows(12, 24, 44, 12, 3, A) + _txt(34, 78, "row store", M, 7)
         + _grid_cols(94, 24, 12, 36, 3, A) + _txt(116, 78, "column store", M, 7)),
    [
        "<strong>OLTP</strong>: many small transactions touching whole rows. "
        "<strong>OLAP</strong>: few huge queries touching a few columns.",
        "A row store keeps a row's fields together, so reading one row is one "
        "page read. Reading one column reads every page.",
        "A column store keeps each column together, so an aggregate reads only "
        "the columns it names.",
        "Columns of one type compress far better than mixed rows &mdash; often "
        "ten times &mdash; and less data read is the actual speed-up.",
    ],
    """
title: OLTP, OLAP and Columnar Storage
intro: Why the DB that runs your use is the wrong one for your dashboards.

## Two workloads

**OLTP** &mdash; online transaction processing &mdash; is the use
DB. Many concurrent links, each doing a thing small: fetch this
order, insert this payment, update this status. Queries touch few rows and
often want all of a row's columns. Latency per query matters enormously.

**OLAP** &mdash; online analytical processing &mdash; is the reporting workload.
Few concurrent users, each asking a thing huge: revenue by region by month
for three years. Queries touch millions of rows and often want three or four
columns out of fifty. Throughput matters. A query taking two seconds instead of
two hundred milliseconds is fine.

These want opposite things, and the disagreement is about physical layout.

## How rows are stored

A **row store** keeps each row's fields contiguously:

```
[1|Ada|Leeds|2026-08-01|120.00][2|Bo|Bristol|2026-08-03|64.50]...
```

Fetching order 2 is a single page read, and all needed is there. Perfect
for OLTP.

Now find the mean of `total` over ten million orders. each page has to be
read, because the totals are scattered one per row, separated by all the other
columns. To read 8 bytes of interest you read a 200-byte row, and 96% of the I/O
is waste.

## How columns are stored

A **column store** keeps each column contiguously:

```
ids:     [1][2][3][4]...
names:   [Ada][Bo][Cy][Di]...
totals:  [120.00][64.50][45.00][220.00]...
```

That mean now reads only the `totals` region. Reading a fiftieth of the data
is roughly a fiftieth of the time. The edge grows with the width of the
table.

Two further wins follow from the layout rather than being added to it.

**Compression.** A column holds one type, and often few distinct values. A
`country` column across ten million rows compresses to almost nothing with
dict encoding. A sorted date column run-length codes brilliantly. Mixed
row data does none of this. Ten-times ratios are plain, and the speed-up is
mostly the reduced I/O.

**Vectorised run.** Values of one type packed contiguously can be processed
in batches with SIMD instructions, instead of one row at a time through a tuple
interface.

The cost is the mirror image: fetching one whole row means one read per column
and reassembly, and inserting a row means writing into fifty places. Columnar
stores are so often append-oriented and batch-loaded, not
update-in-place.

## Choosing

| | Row store | Column store |
|---|---|---|
| Fetch a whole row | fast | slow |
| Aggregate one column | slow | fast |
| Insert or update one row | fast | slow |
| Bulk load | fine | ideal |
| Compression | poor | excellent |
| Examples | PostgreSQL, MySQL | ClickHouse, BigQuery, DuckDB, Snowflake |

## Do not run both on one database

The usual mistake is analytics against the production OLTP DB. A report
scanning ten million rows evicts the working set from the buffer cache, and each
use query afterwards goes to disk. The dashboard is slow *and* the
checkout is slow.

The standard setup separates them: OLTP handles the use, data is
copied into an analytical store on a schedule or a stream, and reports run there
with a [star schema](star_schema.html) shaped for them. The copy is stale by
minutes or hours, which is almost always acceptable for reporting and is the
price of not having the two workloads fight.

The variants above make the difference concrete: the same table queried the OLTP
way and the OLAP way, with a note on how much of each row each one really
needs.

## Where the line has blurred

**DuckDB** is columnar, embedded and single-file &mdash; analytical power with no
cluster. **Postgres** has columnar extensions and can query Parquet through
foreign data wrappers. **Parquet** itself has made columnar a file format rather
than a DB, so the same data can be read by many engines.

The result is that "we need a data warehouse" is a much bigger claim than it was.
For datasets under a few hundred gigabytes, DuckDB over Parquet on one machine
often beats a cluster.

## The I/O gap, in bytes

"A fiftieth of the data" deserves a concrete figure, because it's the whole
arg for columnar. Take ten million orders, fifty columns, eight bytes each,
and mean one column:

|layout|bytes read for `AVG(total)`|
|---|---|
|row store|10M &times; 50 &times; 8 = **4.0 GB**|
|column store|10M &times; 8 = **80 MB**|

The row store must pass over each column of each row to reach the one it needs,
so it reads the whole four gigabytes to sum eighty megabytes of actual interest.
The column store reads only the `total` region. Fifty times less &mdash; and
that ratio is why an aggregate that takes seconds on a row store returns in
milliseconds on a columnar one. It also compounds with compression: that single
column, being one type with few distinct values, often compresses a few-fold
again, so the real read is smaller still. The wider the table, the larger the
gap, which is just backwards from what OLTP wants.

## Where the ten-times compression comes from

"Ten-times ratios are plain" isn't a hope. It falls out of a column holding
one type with few distinct values. A `country` column over ten million rows has
maybe 200 distinct values, so dict encoding stores a one-byte code per row
plus a tiny lookup, instead of the full string each time:

|encoding|size of the country column|
|---|---|
|raw text (~10 bytes/value)|~100 MB|
|dictionary (1 byte/row + dict)|~10 MB|

Ten to one, and a sorted or slowly-changing column run-length codes even harder
&mdash; a date column that repeats each value for a day's worth of rows stores a
value and a count rather than the value a million times. A row store can't do any
of this, because each value sits between bytes of other columns of other types,
with nothing to compress against. The compression isn't a feature bolted on. It
is a consequence of putting like values next to like, and most of the resulting
speed-up is simply that there's less to read.

## Questions people ask

<strong>What is the difference between OLTP and OLAP?</strong> OLTP handles many small reads and writes, such as orders. OLAP runs large analytical queries over many rows.

<strong>Why are columnar stores faster for analytics?</strong> They read only the columns a query needs, and similar values stored together compress well.

<strong>Why are row stores better for OLTP?</strong> A row is stored together, so reading or writing one whole record touches a single place on disk.

<strong>Can I run analytics on my production database?</strong> You can for small data, but long scans compete with transactions for resources. Use a replica or a separate warehouse.

<strong>What is ETL?</strong> Extract, transform, load: copying data from the transactional system into an analytical store, reshaping it on the way.

<strong>Are the two types converging?</strong> Partly. Some systems offer hybrid storage or columnar extensions, but each design still favours one workload.

## Where it goes wrong

**Reporting off the main.** Cache eviction makes the use slow, and the
cause isn't obvious from the use's own metrics.

**Row-by-row inserts into a columnar store.** They're built for batches. Single
inserts are pathologically slow.

**`SELECT *` on a column store.** It gives up the entire edge.

**given you need a cluster.** Measure on one machine first.
""",
    [
        {"q": "Why is a row store slow at averaging one column over ten million rows?",
         "options": ["It cannot use indexes",
                     "The values are scattered one per row, so every page must be read to collect a small fraction of each",
                     "Averages require a full sort",
                     "Row stores do not compress"],
         "answer": 1,
         "why": "To read 8 bytes of interest you read the whole 200-byte row. A column store reads only the region holding that column."},
        {"q": "Why do column stores compress so much better?",
         "options": ["They use a stronger algorithm",
                     "A column holds one type and often few distinct values, so dictionary and run-length encoding work extremely well",
                     "They discard nulls",
                     "They store less data"],
         "answer": 1,
         "why": "Ten-times ratios are ordinary, and since the bottleneck is I/O, less data read is most of the speed-up."},
        {"q": "What goes wrong when reports run against the production OLTP database?",
         "options": ["The reports return stale data",
                     "A large scan evicts the working set from the buffer cache, so application queries afterwards go to disk",
                     "The reports lock the tables",
                     "Transactions fail"],
         "answer": 1,
         "why": "The dashboard is slow and the checkout is slow, and the cause is not visible in the application's own metrics."},
    ],
    seed="""CREATE TABLE orders (
  id INTEGER PRIMARY KEY, customer TEXT, country TEXT, region TEXT,
  placed TEXT, channel TEXT, status TEXT, total REAL, tax REAL, shipping REAL);

INSERT INTO orders VALUES
 (1,'Ada','UK','EMEA','2026-01-14','web','shipped',120.0,24.0,4.5),
 (2,'Bo','US','AMER','2026-01-22','app','shipped',64.5,5.2,3.0),
 (3,'Cy','US','AMER','2026-02-03','web','shipped',45.0,3.6,3.0),
 (4,'Di','IN','APAC','2026-02-18','app','returned',220.0,39.6,6.0),
 (5,'Ed','US','AMER','2026-03-07','web','shipped',99.9,8.0,3.0),
 (6,'Fi','UK','EMEA','2026-03-29','web','shipped',150.0,30.0,4.5),
 (7,'Gu','DE','EMEA','2026-04-11','app','shipped',72.4,13.8,4.5),
 (8,'Hal','US','AMER','2026-05-02','web','cancelled',410.0,32.8,3.0),
 (9,'Ada','UK','EMEA','2026-06-19','app','shipped',58.0,11.6,4.5),
 (10,'Bo','US','AMER','2026-07-25','web','shipped',131.0,10.5,3.0);
""",
    starter="""-- OLTP: fetch one whole order. A row store has every field of this
-- row on one page, so this is a single read.
SELECT * FROM orders WHERE id = 4;
""",
    variants_label="The two workloads on one table",
    variants=[
        {"label": "OLTP: one row, all columns",
         "sql": "-- What the application does thousands of times a second.\n"
                "-- Row storage is exactly right for this.\n"
                "SELECT * FROM orders WHERE id = 4;"},
        {"label": "OLAP: all rows, three columns",
         "sql": "-- What a dashboard does. Ten of the table's columns are\n"
                "-- irrelevant, and a row store reads them anyway.\n"
                "SELECT region, COUNT(*) AS orders, ROUND(SUM(total),2) AS revenue\n"
                "FROM   orders\n"
                "WHERE  status = 'shipped'\n"
                "GROUP  BY region\n"
                "ORDER  BY revenue DESC;"},
        {"label": "How much of each row is wasted",
         "sql": "-- The aggregate above names 3 of 10 columns. On a row store the\n"
                "-- other 7 are read from disk regardless; a column store skips them.\n"
                "SELECT 10 AS columns_in_table,\n"
                "        3 AS columns_the_query_needs,\n"
                "       '70%' AS io_a_row_store_wastes;"},
        {"label": "Why a column compresses",
         "sql": "-- One column, one type, few distinct values. This is what\n"
                "-- dictionary encoding exploits, and why columnar files are small.\n"
                "SELECT COUNT(*) AS rows,\n"
                "       COUNT(DISTINCT region)  AS distinct_regions,\n"
                "       COUNT(DISTINCT channel) AS distinct_channels,\n"
                "       COUNT(DISTINCT total)   AS distinct_totals\n"
                "FROM   orders;"},
    ],
)


# ---------------------------------------------------------------------------
# 19. Star schema
# ---------------------------------------------------------------------------
topic(
    "star_schema",
    "Star Schema: Facts and Dimensions",
    "Analytics",
    "One narrow table of things that happened, surrounded by wide tables "
    "describing them. The shape warehouses are built in.",
    _svg(_box(58, 34, 44, 22, fill=S, stroke=A) + _txt(80, 48, "facts", A, 8)
         + _box(10, 12, 34, 16, fill=S) + _txt(27, 23, "date", M, 7)
         + _box(116, 12, 34, 16, fill=S) + _txt(133, 23, "product", M, 7)
         + _box(10, 62, 34, 16, fill=S) + _txt(27, 73, "store", M, 7)
         + _box(116, 62, 34, 16, fill=S) + _txt(133, 73, "customer", M, 7)
         + _line(44, 24, 62, 36, B, 1) + _line(116, 24, 98, 36, B, 1)
         + _line(44, 66, 62, 54, B, 1) + _line(116, 66, 98, 54, B, 1)),
    [
        "The <strong>fact</strong> table holds measurements &mdash; one row per "
        "event, mostly numbers and foreign keys. It is long and narrow.",
        "<strong>Dimension</strong> tables describe the context &mdash; dates, "
        "products, stores. Short and wide, full of text.",
        "Every query is the same shape: join the fact table to whichever "
        "dimensions the question mentions, group, aggregate.",
        "It is deliberately denormalised. A snowflake schema normalises the "
        "dimensions and trades query simplicity for tidiness.",
    ],
    """
title: Star Schema: Facts and Dimensions
intro: The one schema design that analytical DBs are really optimised for.

## Two kinds of table

A star schema splits all into facts and dims, and the split is
sharper than it first sounds.

A **fact** is a reading of a thing that happened. One row per sale, per
click, per sensor reading. It holds numbers you want to aggregate &mdash;
quantity, amount, duration &mdash; and foreign keys pointing at the dims.
Almost nothing else. Fact tables are huge and narrow.

A **dim** shows the context of a fact. The product dim holds the
name, category, brand, supplier. The date dim holds the day, month,
quarter, day of week, whether it was a holiday. dim tables are small and
wide, and mostly text.

Drawn out, the fact table sits in the middle with dims radiating from it,
which is where the name comes from.

## Why it is shaped that way

each analytical question has the same form: *aggregate some measure, sliced by
some fields, filtered by others*. Revenue by category by month for one
region. Units sold by store by weekday.

In a star schema each such query is the same join: fact table to the dims
the question mentions, group by their fields, aggregate the fact's measures.
Run the variants above and they're all that shape.

That uniformity has three consequences worth having.

**Query planners handle it well.** The pattern is recognisable enough that
analytical engines have a dedicated *star join* optimisation: filter the small
dims first, use the result to restrict the fact-table scan, and never
materialise a large mid.

**Analysts can write the queries.** Adding a slice means adding a join and a
group-by column. No investigation of a normed graph is needed.

**BI tools make them.** Tableau, Looker and Power BI all assume this model,
and give good SQL against it and poor SQL against any of it else.

## The date dimension

A table of dates looks redundant. A DB has date functions. It earns
its place anyway, because it holds things no function knows: your fiscal
calendar, public holidays in the markets you sell in. This Weeks were promotion
periods, whether a day was a weekday in the local sense.

`WHERE d.is_holiday` and `GROUP BY d.fiscal_quarter` are then plain joins
rather than a growing pile of `CASE` expressions.

## Grain

The most consequential choice is the **grain**: what just one fact row
shows.

"One row per order line" and "one row per order" are different grains, and mixing
them corrupts each aggregate &mdash; sum a per-order total across order lines
and you've times'd the revenue by the number of lines. This is the most
common defect in real warehouses, and it's silent.

State the grain in one sentence before creating the table, and make each measure
steady with it.

## Slowly changing dimensions

A product moves category. Do historical facts belong to the old category or the
new one?

**Type 1**: overwrite. Simple, and history is rewritten &mdash; last year's
report changes.

**Type 2**: add a new dimension row with validity dates and point new facts at
it. History is preserved and the dim grows. This is the usual choice, and
it's why dim tables have surrogate keys rather than using the natural
business key.

**Type 3**: keep a `previous_category` column. Enough for one level of history,
rarely enough .

## Star against snowflake

Norming the dims &mdash; splitting `product` into product, category and
supplier tables &mdash; gives a **snowflake schema**. It drops redundancy and
adds joins.

For warehouses the star is often preferred, because dims are small
enough that the redundancy costs little, the extra joins cost real query time,
and the denormalised version is far easier to read. The exception is a truly
large dim &mdash; tens of millions of customers &mdash; where the
duplication starts to matter.

## Mixed grain, shown inflating a total

"Times'd the revenue by the number of lines" is the most costly silent bug
in warehousing, so it's worth watching happen. Three orders of $100 each, with
3, 2 and 1 line items, joined fact-to-lines and summed the wrong way:

|query|result|
|---|---|
|`SUM(total)` over orders|**$300** (correct)|
|`SUM(total)` after joining order lines|**$600** (wrong)|

The join repeats each order's total once per line. So The three-line order counts
its $100 three times, and the total comes out just doubled &mdash; here 2&times;,
but the factor is the mean number of lines per order, what that happens to
be. Nothing errors, the number is plausible, and it's wrong on each run. This is
what "state the grain in one sentence" blocks: a measure at order grain must be
summed at order grain, and mixing it with a per-line join silently times it.

## Text belongs in the dimension, and here is the cost

"Text in the fact table" sounds harmless until you note which table is
huge. The fact table has one row per event. Hundreds of millions of
them &mdash; while dims are small. Storing a 20-byte product name on each
fact row, instead of a 4-byte key pointing at the product dim, widens the
largest table in the warehouse:

|on a 100M-row fact table|storage|
|---|---|
|a 20-byte text column|~2.0 GB|
|a 4-byte foreign key to a dimension|~0.4 GB|

Five times the space, on the table each analytical scan has to read, for data
that is duplicated millions of times. The same product name written on
each one of its sales. The dim stores it once. And because columnar
warehouses scan the columns a query touches, a bloated fact table isn't just disk;
it's read on each query that goes near it. Narrow facts, wide dims isn't
an aesthetic preference &mdash; it's keeping the big table small and the
redundancy in the place where it's cheap.

## Questions people ask

<strong>What is a star schema?</strong> A central fact table of measurable events surrounded by dimension tables that describe them, such as product, customer and date.

<strong>What is the grain of a fact table?</strong> What one row represents, for example one line item on one order. Settle it first, and keep it consistent.

<strong>What is the difference between a fact and a dimension?</strong> Facts are numbers you add up. Dimensions are the descriptive attributes you filter and group by.

<strong>Star schema or snowflake schema?</strong> A star keeps dimensions flat, with fewer joins. A snowflake normalises them, saving space but adding joins. Star is the usual default.

<strong>What is a slowly changing dimension?</strong> A dimension whose attributes change over time, such as a customer's city. You choose whether to overwrite, or keep history with new rows.

<strong>Why have a date dimension?</strong> It lets you group by week, quarter or holiday without computing them in every query, and it keeps date logic in one place.

## Where it goes wrong

**Mixed grain.** Silent, and it inflates each total.

**Text in the fact table.** It belongs in a dim. It makes the largest table
wider for no gain.

**No date dim.** Fiscal calendars and holidays end up as `CASE`
expressions copied between queries.

**Type 1 all over.** History quietly rewrites itself, and last quarter's report
no longer copies.
""",
    [
        {"q": "What does a fact table contain?",
         "options": ["Descriptive attributes like product names and categories",
                     "One row per event: numeric measures plus foreign keys to the dimensions",
                     "One row per customer",
                     "Aggregated totals"],
         "answer": 1,
         "why": "Long and narrow. The descriptive text lives in the dimensions, which are short and wide - putting it in the fact table widens the largest table for nothing."},
        {"q": "Why is mixing grain in a fact table so dangerous?",
         "options": ["It breaks foreign keys",
                     "Summing a per-order total across order lines multiplies revenue by the number of lines, and nothing errors",
                     "It prevents indexing",
                     "It makes joins ambiguous"],
         "answer": 1,
         "why": "It is the most common defect in real warehouses precisely because it is silent. State the grain in one sentence before creating the table."},
        {"q": "Why do star schemas usually beat snowflake schemas in a warehouse?",
         "options": ["They use less storage",
                     "Dimensions are small enough that the redundancy costs little, while the extra joins cost real query time",
                     "Snowflake schemas cannot be indexed",
                     "BI tools cannot read snowflakes"],
         "answer": 1,
         "why": "The exception is a genuinely large dimension - tens of millions of customers - where duplication starts to matter more than the joins."},
    ],
    seed="""CREATE TABLE dim_date (date_key INTEGER PRIMARY KEY, day TEXT, month TEXT,
                       quarter TEXT, weekday TEXT, is_holiday INTEGER);
CREATE TABLE dim_product (product_key INTEGER PRIMARY KEY, name TEXT,
                          category TEXT, brand TEXT);
CREATE TABLE dim_store (store_key INTEGER PRIMARY KEY, store TEXT,
                        city TEXT, region TEXT);
CREATE TABLE fact_sales (date_key INTEGER, product_key INTEGER, store_key INTEGER,
                         units INTEGER, revenue REAL);

INSERT INTO dim_date VALUES
 (1,'2026-01-05','January','Q1','Monday',0),(2,'2026-01-06','January','Q1','Tuesday',0),
 (3,'2026-02-16','February','Q1','Monday',1),(4,'2026-04-09','April','Q2','Thursday',0),
 (5,'2026-04-10','April','Q2','Friday',0),(6,'2026-07-20','July','Q3','Monday',0);

INSERT INTO dim_product VALUES
 (1,'Keyboard','Peripherals','Acme'),(2,'Monitor','Displays','Acme'),
 (3,'Cable','Peripherals','Genco'),(4,'Laptop','Computers','Genco');

INSERT INTO dim_store VALUES
 (1,'Leeds Central','Leeds','North'),(2,'Bristol Quay','Bristol','South'),
 (3,'Online','-','Online');

INSERT INTO fact_sales VALUES
 (1,1,1,3,135.0),(1,3,1,10,65.0),(2,2,3,2,360.0),(2,1,2,1,45.0),
 (3,4,3,1,899.0),(3,3,2,4,26.0),(4,2,1,1,180.0),(4,1,3,5,225.0),
 (5,4,2,2,1798.0),(5,3,3,20,130.0),(6,2,2,3,540.0),(6,1,1,2,90.0);
""",
    starter="""-- Every analytical query is this shape: the fact table joined to
-- whichever dimensions the question mentions, grouped by their
-- attributes, aggregating the fact's measures.
SELECT p.category, SUM(f.units) AS units, ROUND(SUM(f.revenue),2) AS revenue
FROM   fact_sales f
JOIN   dim_product p ON p.product_key = f.product_key
GROUP  BY p.category
ORDER  BY revenue DESC;
""",
    variants_label="Same shape, different slices",
    variants=[
        {"label": "Slice by one dimension",
         "sql": "SELECT p.category, SUM(f.units) AS units,\n"
                "       ROUND(SUM(f.revenue),2) AS revenue\n"
                "FROM   fact_sales f\n"
                "JOIN   dim_product p ON p.product_key = f.product_key\n"
                "GROUP  BY p.category\n"
                "ORDER  BY revenue DESC;"},
        {"label": "Add a second dimension",
         "sql": "-- Adding a slice is adding a join and a group-by column.\n"
                "-- Nothing else about the query changes.\n"
                "SELECT d.quarter, s.region, ROUND(SUM(f.revenue),2) AS revenue\n"
                "FROM   fact_sales f\n"
                "JOIN   dim_date  d ON d.date_key  = f.date_key\n"
                "JOIN   dim_store s ON s.store_key = f.store_key\n"
                "GROUP  BY d.quarter, s.region\n"
                "ORDER  BY d.quarter, revenue DESC;"},
        {"label": "What the date dimension is for",
         "sql": "-- No date function knows your holidays or your fiscal calendar.\n"
                "-- A dimension does, and the filter is an ordinary join.\n"
                "SELECT d.day, d.weekday, ROUND(SUM(f.revenue),2) AS revenue\n"
                "FROM   fact_sales f\n"
                "JOIN   dim_date d ON d.date_key = f.date_key\n"
                "WHERE  d.is_holiday = 1\n"
                "GROUP  BY d.day, d.weekday;"},
        {"label": "Three dimensions at once",
         "sql": "-- The star join: filter the small dimensions, use the result to\n"
                "-- restrict the large fact scan.\n"
                "SELECT d.month, p.brand, s.region,\n"
                "       SUM(f.units) AS units, ROUND(SUM(f.revenue),2) AS revenue\n"
                "FROM   fact_sales f\n"
                "JOIN   dim_date    d ON d.date_key    = f.date_key\n"
                "JOIN   dim_product p ON p.product_key = f.product_key\n"
                "JOIN   dim_store   s ON s.store_key   = f.store_key\n"
                "WHERE  p.brand = 'Acme'\n"
                "GROUP  BY d.month, p.brand, s.region\n"
                "ORDER  BY revenue DESC;"},
    ],
)


# ---------------------------------------------------------------------------
# 20. SQL injection and parameterised queries
# ---------------------------------------------------------------------------
topic(
    "sql_injection_and_parameters",
    "SQL Injection and Parameterised Queries",
    "Safety",
    "What goes wrong when data is pasted into a query string, and the one fix "
    "that actually works.",
    _svg(_box(12, 26, 62, 20, fill=S) + _txt(43, 39, "' OR 1=1 --", A, 7)
         + _txt(43, 60, "input", M, 7)
         + _line(78, 36, 96, 36, B, 1.2)
         + _box(100, 26, 48, 20, fill="none", stroke=A) + _txt(124, 39, "query", A, 7)
         + _txt(124, 60, "now different", M, 7)),
    [
        "Injection happens when input is <em>concatenated</em> into SQL, so the "
        "database cannot tell data from instructions.",
        "A parameterised query sends the SQL and the values separately. The "
        "value can never become syntax, whatever it contains.",
        "Escaping is not the fix. It is a blacklist, it varies by engine and "
        "charset, and it fails on numeric contexts entirely.",
        "Identifiers &mdash; table and column names &mdash; cannot be "
        "parameterised. Those need an allowlist.",
    ],
    """
title: SQL Injection and Parameterised Queries
intro: The oldest widespread vulnerability in web software, why it happens, and the single correct fix.

## The mechanism

Build a query by pasting user input into a string:

```
"SELECT * FROM users WHERE name = '" + name + "'"
```

With `name = "Ada"` this makes a sensible query. With
`name = "' OR '1'='1"` it makes:

```
SELECT * FROM users WHERE name = '' OR '1'='1'
```

The quote closed the string early, and all after it became **syntax**
rather than data. The DB isn't confused or exploited &mdash; it's
right running the query it was given. The bug happened before it arrived.

Run the variants above to see it: the same lookup, safe and unsafe, with a normal
value and then a crafted one.

## What can be done through it

A closed quote gives an attacker the whole language.

**Authentication bypass.** `' OR '1'='1` as a password makes the `WHERE` clause
true for each row.

**Reading other tables.** A `UNION SELECT` appends results from anywhere the
DB user can read.

**Writing.** If the driver allows multiple statements, a semicolon starts a new
one.

**Blind extraction.** Even with no output at all, a rule that changes
whether the page errors, or how long it takes, leaks one bit per request &mdash;
and one bit per request is enough to read a password hash.

That last one is worth costing out. "one bit per request" sounds slow
and isn't. Ask a yes/no question the query answers through its action &mdash;
*is the first character of the admin's hash greater than `m`?* &mdash; and binary
search finds each character in `ceil(log2(95)) = 7` requests across the printable
ASCII range. A bcrypt hash is 60 characters. So The whole thing comes out in
about 60 &times; 7 = **420 requests**, plus a handful to find the length first.
At a modest 100 requests a second that is **four seconds**, and it's fully
automated &mdash; the attacker writes none of it by hand. The naive
character-by-character guess would take 2,850 requests. Binary search is what
makes a channel that leaks one bit at a time truly fast.

## The fix

Send the query and the values apart:

```
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

The `?` is a **placeholder**. The DB receives the query text and the value
through different channels, parses the statement first, and then binds the value
into an already-parsed plan.

The value so can't alter the structure of the query, because parsing has
already finished by the time it arrives. `' OR '1'='1` turns a search for a
user whose name is truly `' OR '1'='1`, which finds nothing.

This isn't a filter that might miss a thing. It's a structural ensure:
there's no input for which a bound param turns syntax.

## The same property also makes it faster

The security comes from one fact: the query text is fixed and the values arrive
apart. That same fact is a speed win, and the two aren't a
coincidence &mdash; they're the same mechanism seen from two sides.

A DB parses a query string, plans it. Only then runs it. When the text
is fixed, that parse-and-plan happens once and the plan is cached and reused for
each later run with different bound values. When the query is built by
concatenation, each call is a *different* string &mdash; `name = 'user1'`,
`name = 'user2'` &mdash; so the cache never hits and the planner runs each time.

Measured in the SQLite this page runs, reusing one prepared statement against
re-parsing a fresh query string each time is about **1.8&times; faster** (7.5 vs
13.3 microseconds per query), and the gap widens for more complex queries where
planning is the larger share. So the concatenation habit is slower *and* unsafe,
and the fix for one is the fix for the other: the fixed query string that denies
an attacker a foothold is the same fixed string the planner can cache.

## Why escaping is not the fix

Escaping tries to neutralise dangerous characters in the input. It fails for
reasons that aren't obvious in advance:

**Numeric contexts have no quotes.** `WHERE id = " + id` needs no quote to
escape, and `1 OR 1=1` needs no special characters at all.

**Character sets.** Multi-byte encodings have once allowed a byte
sequence that turns a quote after the escaping function has run.

**It's a blacklist.** each blacklist is a claim to have thought of all.

**It's per-engine.** Rules differ between MySQL, PostgreSQL and SQLite, and code
that moves between them silently stops being correct.

Parameterisation avoids all of this by never putting the value in the query text
at all.

## Identifiers cannot be parameterised

This is the real limitation. A placeholder can stand for a *value*, not for a
table or column name:

```
"ORDER BY " + column      -- cannot be parameterised
```

The correct approach is an **allowlist**: map the user's input to a known-good
identifier and reject any of it unrecognised.

```
allowed = {"name": "name", "date": "created_at"}
column = allowed.get(user_input)
if column is None: reject()
```

Never sanitise an identifier by escaping. Choose it from a fixed set.

There's one more case that sends people back to concatenation, and it should
not: a variable-length `IN` list. `WHERE id IN (?)` does **not** bind a list to
the single placeholder &mdash; it binds one value. The correct move is to make
*one placeholder per element* and bind them positionally:

```
ids = [4, 7, 12]
marks = ",".join("?" for _ in ids)      # "?,?,?"
cursor.execute("... WHERE id IN (%s)" % marks, ids)
```

The `%` here builds only punctuation. Commas and question marks, never the
values &mdash; so nothing user-controlled reaches the query text. each id is still
bound. It looks like string-building, and the thing being built holds no data,
which is just the line that keeps it safe.

## The other layers

Parameterise all over, and then:

**Least privilege.** The use's DB user shouldn't own the schema or
be able to `DROP`. It limits the damage of any bug, not just this one.

**Don't show DB errors.** Error text is how blind extraction is made
fast.

**ORMs help but don't immunise.** Their query builders parameterise by default,
and each one of them has a raw-SQL escape hatch that doesn't. The escape hatch
is where the vulnerabilities are.

## Questions people ask

<strong>What is SQL injection?</strong> An attack where user input is treated as SQL code, letting the attacker change what a query does.

<strong>How do parameterised queries prevent it?</strong> The query text and the values are sent separately, so input is always treated as data and never parsed as SQL.

<strong>Is escaping input enough?</strong> No. Escaping is easy to get wrong across encodings and contexts. Parameters are the reliable fix.

<strong>Can I parameterise table or column names?</strong> No. Identifiers cannot be bound as parameters. Check them against an allowed list instead.

<strong>Do ORMs protect me from injection?</strong> Mostly, but raw query helpers and string-built filters can still be injectable. Check that values go through parameters.

<strong>What other defences should I add?</strong> Give the application account the fewest privileges it needs, validate input, and log failed queries. They limit damage if one slips through.

## Where it goes wrong

**"It's an inner tool."** inner input is still input, and inner tools
get exposed.

**Parameterising most of a query.** One concatenated fragment is enough.

**Trusting a value because it came from a dropdown.** The dropdown is in the
client. The request isn't.

**Escaping instead of binding.** Even when correct today, it's one encoding
change from not being.
""",
    [
        {"q": "Why does a parameterised query prevent injection?",
         "options": ["It escapes dangerous characters",
                     "The statement is parsed before the value arrives, so the value can never become syntax",
                     "It validates input types",
                     "It runs with fewer privileges"],
         "answer": 1,
         "why": "It is a structural guarantee rather than a filter: there is no input for which a bound parameter turns into query structure."},
        {"q": "Why is escaping an inadequate defence?",
         "options": ["It is slow",
                     "Numeric contexts have no quotes to escape, character sets can defeat it, and it is a per-engine blacklist",
                     "It breaks Unicode",
                     "It only works on SELECT"],
         "answer": 1,
         "why": "WHERE id = 1 OR 1=1 contains no special characters at all. Parameterisation avoids the whole class by never putting the value in the query text."},
        {"q": "How should a user-supplied ORDER BY column be handled?",
         "options": ["Parameterise it with a placeholder",
                     "Map it through an allowlist of known-good identifiers and reject anything else",
                     "Escape it",
                     "Wrap it in quotes"],
         "answer": 1,
         "why": "Placeholders stand for values, not identifiers. Identifiers must be chosen from a fixed set rather than sanitised."},
    ],
    seed="""CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, role TEXT);
INSERT INTO users VALUES
  (1,'Ada','ada@example.com','admin'),
  (2,'Bo','bo@example.com','user'),
  (3,'Cy','cy@example.com','user'),
  (4,'Di','di@example.com','user');

CREATE TABLE password_resets (user_id INTEGER, token TEXT);
INSERT INTO password_resets VALUES (1,'a1b2-secret-token'),(2,'c3d4-secret-token');
""",
    starter="""-- The intended query, with an ordinary value concatenated in.
-- Nothing looks wrong yet.
SELECT id, name, role FROM users WHERE name = 'Ada';
""",
    variants_label="The same lookup, four ways",
    variants=[
        {"label": "Normal input, concatenated",
         "sql": "-- name = \"Ada\". Looks fine, and the bug is already present.\n"
                "SELECT id, name, role FROM users WHERE name = 'Ada';"},
        {"label": "Crafted input: bypass",
         "sql": "-- name = \"' OR '1'='1\". The quote closed the string early and\n"
                "-- the rest became syntax. Every row comes back.\n"
                "SELECT id, name, role FROM users WHERE name = '' OR '1'='1';"},
        {"label": "Crafted input: read another table",
         "sql": "-- A UNION appends results from anywhere this database user can\n"
                "-- read. Nothing about the original query intended this.\n"
                "SELECT id, name, role FROM users WHERE name = ''\n"
                "UNION SELECT user_id, token, 'leaked' FROM password_resets;"},
        {"label": "Parameterised: the fix",
         "sql": "-- In application code this is  WHERE name = ?  with the value\n"
                "-- passed separately. The lab has no driver to bind through, so\n"
                "-- this is what binding AMOUNTS to: the crafted string arriving\n"
                "-- as a VALUE rather than as syntax. The statement is parsed\n"
                "-- first, so this searches for a user literally named\n"
                "--     ' OR '1'='1\n"
                "-- and nobody is. Zero rows - the payload is inert.\n"
                "SELECT id, name, role FROM users WHERE name = ''' OR ''1''=''1';"},
        {"label": "Why escaping is not enough",
         "sql": "-- A numeric context has no quotes to escape, and this payload\n"
                "-- contains no special characters for an escaper to catch.\n"
                "SELECT id, name, role FROM users WHERE id = 1 OR 1=1;"},
    ],
)

CHECKS = {"database/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS}
